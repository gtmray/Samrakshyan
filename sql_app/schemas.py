from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    imageUrl: str
    description: Optional[str] = None
    audioUrl: str


# inherit from ItemBase
# have all the attributes of the Parent class
#  plus any additional data (attributes) needed for creation
class ItemCreate(ItemBase):
    pass


# read the data from the database and returning it from the API
class Item(ItemBase):
    id: str

    class Config:
        orm_mode = True
