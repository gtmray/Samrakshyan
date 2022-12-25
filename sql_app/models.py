from sqlalchemy import Column, String

from db import Base

# create table
class Item(Base):
    __tablename__ = "items"

    id = Column(String(80), primary_key=True, unique=True, index=True)
    name = Column(String(80), nullable=False, unique=True, index=True)
    imageUrl = Column(String(100), nullable=False, index=True)
    description = Column(String(1000))
    audioUrl = Column(String(100), nullable=False, index=True)
