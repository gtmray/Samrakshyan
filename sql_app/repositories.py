import os
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from . import models


class ItemRepo:

    async def create(db: Session, bird_name: str, image: UploadFile, audio: UploadFile, description: str, ):
        image_directory_path = 's3/image'
        audio_directory_path = 's3/audio'
        if not os.path.exists(image_directory_path):
            os.makedirs(image_directory_path)
        if not os.path.exists(audio_directory_path):
            os.makedirs(audio_directory_path)
        image_file_location = f"s3/image/{image.filename}"
        audio_file_location = f"s3/audio/{audio.filename}"
        with open(image_file_location, "wb+") as file_object:
            file_object.write(image.file.read())
        with open(audio_file_location, "wb+") as file_object:
            file_object.write(audio.file.read())
        image_item = image_file_location
        audio_item = audio_file_location
        db_item = models.Item(bird_name=bird_name.lower(), image_path=image_item, description=description,
                              audio_path=audio_item,
                              id=str(uuid4()))
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def fetch_by_id(db: Session, _id: str):
        print(_id)
        return db.query(models.Item).filter(models.Item.id == _id).first()

    def fetch_by_name(db: Session, bird_name: str):
        return  db.query(models.Item).filter(models.Item.bird_name == bird_name.lower()).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Item).offset(skip).limit(limit).all()

    async def delete(db: Session, item_id):
        db_item = db.query(models.Item).filter_by(id=item_id).first()
        db.delete(db_item)
        db.commit()

    async def update(db: Session, item_data):
        updated_item = db.merge(item_data)
        db.commit()
        return updated_item
