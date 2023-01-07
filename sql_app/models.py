from sqlalchemy import Column, String

from db import Base

# create table
class Item(Base):
    __tablename__ = "items"

    id = Column(String(80), primary_key=True, unique=True, index=True)
    bird_name = Column(String(80), nullable=False, unique=True, index=True)
    image_path = Column(String(100), nullable=False, index=True)
    description = Column(String(1000))
    audio_path = Column(String(100), nullable=False, index=True)
