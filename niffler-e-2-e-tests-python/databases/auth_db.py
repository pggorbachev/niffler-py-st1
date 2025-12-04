from sqlalchemy import create_engine, Engine, event
from sqlmodel import Session, select
from models.auth import User
import allure
from allure_commons.types import AttachmentType

from models.config import Envs


class UserDb:
    engine: Engine

    def __init__(self, envs: Envs):
        self.engine = create_engine(envs.auth_db_url)
        event.listen(self.engine, "do_execute", fn=self.attach_sql)

    @staticmethod
    @allure.step('DB: attach sql')
    def attach_sql(cursor, statement, parameters, context):
        statement_with_params = statement % parameters
        name = statement.split(" ")[0] + " " + context.engine.url.database
        allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)

    def get_user_by_username(self, username: str) -> User | None:
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            try:
                user = session.exec(statement).one()
            except Exception:
                user = None
            return user