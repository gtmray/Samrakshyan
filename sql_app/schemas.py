from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    imageUrl: str
    description: Optional[str] = None
    audioUrl: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: str

    class Config:
        orm_mode = True
