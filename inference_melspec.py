# Inference

# !pip install pydub
import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

from pydub import AudioSegment
import math
import shutil

import warnings
warnings.filterwarnings("ignore")

# # Turn interactive plotting off
# import matplotlib
# matplotlib.use('Agg')
# plt.ioff()

# Variables for feature extraction
SAMPLE_RATE = 32000
SPEC_SHAPE = (48, 128) # height x width
SIGNAL_LENGTH = 10
N_FFT = 1024         
HOP_SIZE =  int(SIGNAL_LENGTH * SAMPLE_RATE / (SPEC_SHAPE[1] - 1))      
N_MELS = SPEC_SHAPE[0]   
WIN_SIZE = 1024      
WINDOW_TYPE = 'hann' 
FEATURE = 'mel'      
FMIN = 500
FMAX = 12500

DATA_PATH = 'charaNet'
BIRDS = os.listdir(f'{DATA_PATH}/train')

def SplitAudio(audio_file, sec_to_split=10):
    
    validAudio = lambda audio, amp_threshold: True if audio.max > amp_threshold else False
    
    global temp_n
    temp_n = 0
    mili=1000
    export_folder = f'tmp/inference/'
    export_name = audio_file.split('/')[-1]
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
    th = audio.max//2
 
    duration = math.floor(audio.duration_seconds)
    splits = np.arange(0, duration, sec_to_split)

    if duration > sec_to_split:
        rem = duration % sec_to_split
        n_splits = round(duration / sec_to_split)
        for n in range(n_splits-1): # Except last splitted file
            newAudio = audio[splits[n]*mili:splits[n+1]*mili]
            temp_n = n
            if validAudio(newAudio, th):
                newAudio.export(f'{export_folder}/{export_name}{n}.{exportFormat}', format=exportFormat)
        
        # For the last splitted file
        if rem <= sec_to_split//2:
            n = temp_n
            # If remaining  audio is small enough, don't separate
            newAudio = audio[splits[n+1]*mili:duration*mili]
            if validAudio(newAudio, th):
                newAudio.export(f'{export_folder}/{export_name}{n+1}.{exportFormat}', format=exportFormat)

        else:
            n = temp_n
            # If remaining audio is big enough, make it separate file
            newAudio = audio[splits[n+1]*mili:duration*mili]
            if validAudio(newAudio, th):
                newAudio.export(f'{export_folder}/{export_name}{n+1}.{exportFormat}', format=exportFormat)

    else:
        if validAudio(audio, th):
            audio.export(f'{export_folder}/{export_name}original.{exportFormat}', format=exportFormat)

def create_features(inference_data_path):
    
    # Find the list of all 10 sec splitted audio files
    audio_files = [f for f in os.listdir(inference_data_path) if f.split('.')[-1]=='mp3']
    count = 0
    for aud in audio_files:

        signal, sr = librosa.load(os.path.join(inference_data_path, aud),duration=10) # sr = sampling rate
        # Plot mel-spectrogram
        S = librosa.feature.melspectrogram(y=signal,
                                           sr=SAMPLE_RATE,
                                            n_fft=N_FFT,
                                            hop_length=HOP_SIZE, 
                                            n_mels=N_MELS, 
                                            fmin=FMIN, 
                                            fmax=FMAX) 

        fig = plt.figure(figsize=(10, 4))
        librosa.display.specshow(librosa.power_to_db(S**2,ref=np.max), fmin=FMIN,y_axis='linear')
        # plt.colorbar(format='%+2.0f dB')
        plt.axis(False)
        plt.tight_layout()
        # plt.show()
        count += 1
        plt.savefig(f'{inference_data_path}/inf{count}.jpg')
        plt.close(fig)
        
def preprocess_img(image_dir, img_size):
    img_width, img_height = img_size[0], img_size[1]
    img = image.load_img(image_dir, target_size = (img_width, img_height))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis = 0)
    img = preprocess_input(img) 
    return img

def prediction(model_dir, inference_data_path, img_size):
    # List of feature images
    feat = [os.path.join(inference_data_path, f) for f in os.listdir(inference_data_path) if f.split('.')[-1]=='jpg']
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

model_dir = 'model/CNMelSpec_Model'
inference_data_path = 'tmp/inference/'
raw_data_path = 'audio/XC98609 -original.mp3aug.wav'

img_size = (128, 128)

if 'tmp' not in os.listdir('./'):
    os.makedirs(inference_data_path)

SplitAudio(raw_data_path)
create_features(inference_data_path)
result = prediction(model_dir, inference_data_path, img_size)

print(f"The predicted audio is of: {max(result)}")
