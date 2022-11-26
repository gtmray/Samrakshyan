import os
import librosa
import soundfile as sf
import numpy as np
import os
from audiomentations import Compose, AddGaussianNoise

bird_count = {}
DATA_PATH = '/content/drive/MyDrive/10SecSplitMajor'
train_path = '/content/DataSplitted/train'
# BIRDS = os.listdir(DATA_PATH)

# for bird in BIRDS:
#     bird_count[bird] = len(os.listdir(os.path.join(DATA_PATH, bird)))

# birds_to_augment = [k for k, v in bird_count.items() if v<30]

data_path = 'audio/XC98609 -original.mp3'

augment_raw_audio = Compose(
    [
        AddGaussianNoise(min_amplitude=0.01, max_amplitude=0.015, p=1)
    ]
)

# for bird in birds_to_augment:
#     os.chdir(os.path.join(train_path, bird))
#     for filename in os.listdir(os.path.join(train_path, bird)):
#         x, sr = librosa.load(filename)
#         augmented_signal = augment_raw_audio(x, sr)
#         sf.write(f'{filename}aug.wav', augmented_signal, sr, format='wav')
x, sr = librosa.load(data_path)
augmented_signal = augment_raw_audio(x, sr)
sf.write(f'{data_path}aug.wav', augmented_signal, sr, format='wav')
# os.chdir('/content')
