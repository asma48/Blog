from pydantic import BaseModel
from typing import Text


class Create_Post(BaseModel):
    title: str
    discription: Text
