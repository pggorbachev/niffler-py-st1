import json
import logging
from confluent_kafka import TopicPartition
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import Consumer, Producer

from utils.waiters import wait_until_timeout


class KafkaClient:
    """Класс для взаимодействия с кафкой"""

    def __init__(
        self,
        kafka_bootstrap_servers: str,
        client_id: str = 'tester',
        group_id: str = 'tester',
    ):
        self.server = kafka_bootstrap_servers

        self.admin = AdminClient(
            {"bootstrap.servers": self.server}
        )
        self.producer = Producer(
            {"bootstrap.servers": self.server}
        )
        self.consumer = Consumer(
            {
                "bootstrap.servers": self.server,
                "group.id": group_id,
                "client.id": client_id,
                "auto.offset.reset": "latest",
                "enable.auto.commit": False,
                "enable.ssl.certificate.verification": False,
            }
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.consumer.close()
        self.producer.flush()

    def list_topics_names(self, attempts: int = 5):
        """Вернуть список доступных топиков"""
        try:
            topics = self.admin.list_topics(timeout=attempts).topics
            return [topics.get(item).topic for item in topics]
        except RuntimeError:
            logging.error("no topics in kafka")
            return []

    @wait_until_timeout
    def consume_message(self, partitions, **kwargs):
        """Вернуть последнее после определенной позиции сообщение"""
        self.consumer.assign(partitions)
        try:
            message = self.consumer.poll(1.0)
            if message is None:
                return None
            if message.error():
                logging.error(f"Kafka message error: {message.error()}")
                return None
            logging.debug(f'{message.value()}')
            return message.value()
        except AttributeError:
            return None

    def get_last_offset(self, topic: str = "", partition_id=0):
        """Вернуть последнюю позицию партиции"""
        partition = TopicPartition(topic, partition_id)
        try:
            low, high = self.consumer.get_watermark_offsets(partition, timeout=10)
            return high
        except Exception as err:
            logging.error("probably no such topic: %s: %s", topic, err)
            return None

    def log_msg_and_json(self, topic_partitions):
        msg = self.consume_message(topic_partitions, timeout=25)
        logging.info(msg)
        return msg

    def subscribe_listen_new_offsets(self, topic):
        self.consumer.subscribe([topic])
        p_ids = self.consumer.list_topics(topic).topics[topic].partitions.keys()
        partitions_offsets_event = {k: self.get_last_offset(topic, k) for k in p_ids}
        logging.info(f'{topic} offsets: {partitions_offsets_event}')
        topic_partitions = [TopicPartition(topic, k, v) for k, v in partitions_offsets_event.items()]
        return topic_partitions

    @staticmethod
    def delivery_report(err, msg):
        """Kafka delivery callback"""
        if err is not None:
            logging.info(f"Message delivery failed: {err}")
            print(f"Message delivery failed: {err}")
        else:
            logging.info(
                f"Message delivered to '{msg.topic()}'"
                f"[partition {msg.partition()}]"
                f"Offset {msg.offset()}")
            print(
                f"Message delivered to '{msg.topic()}'",
                f"Partition [{msg.partition()}]",
                f"Offset {msg.offset()}")

    def sent_event(self, topic: str, username: str):
        self.producer.produce(
            topic,
            json.dumps({"username": str(username)}).encode("utf-8"),
            on_delivery=self.delivery_report,
            headers={"__TypeId__": "guru.qa.niffler.model.UserJson"},
        )
        self.producer.flush()
