from typing import List
import uvicorn as uvicorn
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from uuid import uuid4
import os
from fastapi.encoders import jsonable_encoder
from db import get_db, engine
from sql_app.repositories import ItemRepo
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import engine
from sql_app import models, schemas

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# import sys
import numpy as np
import io
import librosa
import librosa.display
import matplotlib.pyplot as plt
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Rescaling

from pydub import AudioSegment
import math

import warnings

warnings.filterwarnings("ignore")

img_size = (128, 128)

DATA_PATH = 'charaNet'
with open('birds.txt') as f:
    BIRDS = f.read()
BIRDS = BIRDS.split(',')
model_dir = 'model/CNMelSpec_Model'
# model_dir = sys.argv[1]
inference_data_path = 'tmp/inference/'
# raw_data_path = 'audio/XC98609 -original.mp3aug.wav'

# Variables for feature extraction
SAMPLE_RATE = 32000
SPEC_SHAPE = (48, 128)  # height x width
SIGNAL_LENGTH = 10
N_FFT = 1024
HOP_SIZE = int(SIGNAL_LENGTH * SAMPLE_RATE / (SPEC_SHAPE[1] - 1))
N_MELS = SPEC_SHAPE[0]
WIN_SIZE = 1024
WINDOW_TYPE = 'hann'
FEATURE = 'mel'
FMIN = 500
FMAX = 12500


def SplitAudio(audio_file, sec_to_split=10):
    validAudio = lambda audio, amp_threshold: True if audio.max > amp_threshold else False

    global temp_n
    temp_n = 0
    mili = 1000
    export_folder = f'tmp/inference/'
    # export_name = audio_file.split('/')[-1]
    export_name = 'inf_file'
    exportFormat = 'mp3'
    try:
        audio = AudioSegment.from_mp3(audio_file)
    except:
        print("File handled: ", audio_file)
        extension = audio_file.split('.')[-1]
        if extension == 'wav':
            audio = AudioSegment.from_wav(audio_file)
        elif extension == 'ogg':
            audio = AudioSegment.from_ogg(audio_file)
    th = audio.max // 2

    duration = math.floor(audio.duration_seconds)
    splits = np.arange(0, duration, sec_to_split)

    if duration > sec_to_split:
        rem = duration % sec_to_split
        n_splits = round(duration / sec_to_split)
        for n in range(n_splits - 1):  # Except last splitted file
            newAudio = audio[splits[n] * mili:splits[n + 1] * mili]
            temp_n = n
            if validAudio(newAudio, th):
                newAudio.export(f'{export_folder}/{export_name}{n}.{exportFormat}', format=exportFormat)

        # For the last splitted file
        if rem <= sec_to_split // 2:
            n = temp_n
            # If remaining  audio is small enough, don't separate
            newAudio = audio[splits[n + 1] * mili:duration * mili]
            if validAudio(newAudio, th):
                newAudio.export(f'{export_folder}/{export_name}{n + 1}.{exportFormat}', format=exportFormat)

        else:
            n = temp_n
            # If remaining audio is big enough, make it separate file
            newAudio = audio[splits[n + 1] * mili:duration * mili]
            if validAudio(newAudio, th):
                newAudio.export(f'{export_folder}/{export_name}{n + 1}.{exportFormat}', format=exportFormat)

    else:
        if validAudio(audio, th):
            audio.export(f'{export_folder}/{export_name}original.{exportFormat}', format=exportFormat)


def create_features(inference_data_path):
    # Find the list of all 10 sec splitted audio files
    audio_files = [f for f in os.listdir(inference_data_path) if f.split('.')[-1] == 'mp3']
    count = 0
    for aud in audio_files:
        signal, sr = librosa.load(os.path.join(inference_data_path, aud), duration=10)  # sr = sampling rate
        # Plot mel-spectrogram
        S = librosa.feature.melspectrogram(y=signal,
                                           sr=SAMPLE_RATE,
                                           n_fft=N_FFT,
                                           hop_length=HOP_SIZE,
                                           n_mels=N_MELS,
                                           fmin=FMIN,
                                           fmax=FMAX)

        fig = plt.figure(figsize=(10, 4))
        mel_spec = librosa.power_to_db(S, ref=np.max)
        librosa.display.specshow(mel_spec, fmin=FMIN, y_axis='linear')
        plt.axis(False)
        plt.tight_layout()
        # plt.show()
        count += 1
        plt.savefig(f'{inference_data_path}/inf{count}.jpg')
        plt.close(fig)


def preprocess_img(image_dir, img_size):
    img_width, img_height = img_size[0], img_size[1]
    img = image.load_img(image_dir, target_size=(img_width, img_height))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    norm = Rescaling(1. / 255)
    img = norm(img)
    img = preprocess_input(img)
    return img


def prediction(model_dir, inference_data_path, img_size):
    # List of feature images
    feat = [os.path.join(inference_data_path, f) for f in os.listdir(inference_data_path) if f.split('.')[-1] == 'jpg']
    results = []
    for m in feat:
        model_loaded = load_model(model_dir)
        img = preprocess_img(m, img_size)
        output = BIRDS[np.argmax(model_loaded.predict(img), axis=-1)[0]]
        results.append(output)
        print(output)
    result = max(results)

    # Remove the temporary splitted audio and mfcc images
    for i in os.listdir(inference_data_path):
        os.remove(os.path.join(inference_data_path, i))
    return results


if 'tmp' not in os.listdir('./'):
    os.makedirs(inference_data_path)


def predict_bird(byte_audio):
    s = io.BytesIO(byte_audio)
    SplitAudio(s)
    create_features(inference_data_path)
    result = prediction(model_dir, inference_data_path, img_size)

    return max(result)


app = FastAPI()
# create all the tables in the database
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def readroot():
    return {"Mike check": "Mike is okay"}


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/files/", tags=["audioupload"])
async def upload_file(file: UploadFile):
    try:
        result = predict_bird(await file.read())
    except Exception as e:
        print(e)
        result = "Unknown"

    return {"Predicted": result}


@app.get("/uuid", tags=["Token generate"])
def get_token():
    return {
        "token": str(uuid4())
    }


@app.post('/items', tags=["Birds_items"], response_model=schemas.Item, status_code=201)
async def create_item(item_request: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Create an Item and store it in the database
    """

    db_item = ItemRepo.fetch_by_name(db, name=item_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item with given name already exists!")

    return await ItemRepo.create(db=db, item=item_request)


@app.get('/items', tags=["Birds_items"], response_model=List[schemas.Item])
def get_all_items(db: Session = Depends(get_db)):
    """
    Get all the Items stored in database
    """
    return ItemRepo.fetch_all(db)


@app.get('/items/{name}', tags=["Birds_items"], response_model=schemas.Item)
def get_item(item_name: str, db: Session = Depends(get_db)):
    """
    Get the Item with the given name provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_name(db, item_name)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given name")
    return db_item


@app.get('/items/{item_id}', tags=["Birds_items"], response_model=schemas.Item)
def get_item(item_id: str, db: Session = Depends(get_db)):
    """
    Get the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    return db_item


@app.delete('/items/{item_id}', tags=["Birds_items"])
async def delete_item(item_id: str, db: Session = Depends(get_db)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    await ItemRepo.delete(db, item_id)
    return "Item deleted successfully!"


@app.put('/items/{item_id}', tags=["Birds_items"], response_model=schemas.Item)
async def update_item(item_id: str, item_request: schemas.Item, db: Session = Depends(get_db)):
    """
    Update an Item stored in the database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item:
        update_item_encoded = jsonable_encoder(item_request)
        db_item.name = update_item_encoded['name']
        db_item.imageUrl = update_item_encoded['imageUrl']
        db_item.description = update_item_encoded['description']
        db_item.audioUrl = update_item_encoded['audioUrl']
        return await ItemRepo.update(db=db, item_data=db_item)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given ID")


if __name__ == "__main__":
    uvicorn.run(host='0.0.0.0', debug=True)
