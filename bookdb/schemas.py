from datetime import datetime, date
from typing import List, Optional

from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author: str
    published_date: date

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str
    author: str
    published_date: date


class BookUpdate(BaseModel):
    title: Optional[str]
    author:  Optional[str]
    published_date:  Optional[date]
