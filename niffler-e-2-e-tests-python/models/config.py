from pydantic import BaseModel


class Envs(BaseModel):
    frontend_url: str
    gateway_url: str
    profile_url: str
    spend_db_url: str
    test_username: str
    test_password: str
    kafka_address: str
    userdata_db_url: str
    auth_db_url: str
    registration_url: str
    auth_url: str
    kafka_bootstrap_servers: str
    auth_secret: str
    logs_file: str