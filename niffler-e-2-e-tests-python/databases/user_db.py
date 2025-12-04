from sqlalchemy import create_engine, Engine, event
from sqlmodel import Session, select
from models.user import User
import allure
from allure_commons.types import AttachmentType

from models.config import Envs
from collections.abc import Sequence

class UserdataDb:
    engine: Engine

    def __init__(self, envs: Envs):
        self.engine = create_engine(envs.userdata_db_url)
        event.listen(self.engine, "do_execute", fn=self.attach_sql)

    @staticmethod
    @allure.step('DB: attach sql')
    def attach_sql(cursor, statement, parameters, context):
        statement_with_params = statement % parameters
        name = statement.split(" ")[0] + " " + context.engine.url.database
        allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)

    def get_user(self, username) -> Sequence[User]:
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            return session.exec(statement).one()