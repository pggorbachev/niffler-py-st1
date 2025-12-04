from datetime import datetime

from pydantic import BaseModel
from sqlmodel import SQLModel, Field

from models.category import CategoryAdd


class Spend(BaseModel):
    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    category: str
    spendDate: datetime
    currency: str
    username: str

class SpendAdd(BaseModel):
    amount: float
    description: str
    category: str
    spendDate: str
    currency: str

class SpendSQL(SQLModel, table=True):
    __tablename__ = 'spend'
    id: str | None = Field(default=None, primary_key=True)
    username: str
    amount: float
    description: str
    category_id: str = Field(foreign_key="category.id")
    spend_date: datetime
    currency: str