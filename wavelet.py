import warnings
import librosa
import matplotlib.pyplot as plt
import pywt
import numpy as np
import os

warnings.filterwarnings("ignore")

for train_val_test in ['train', 'val', 'test']:
    DATA_PATH = f'/content/drive/MyDrive/DataAugmentedMajor/{train_val_test}'

    BIRDS = os.listdir(DATA_PATH)
    # BIRDS = INCLUDE_BIRDS
    os.chdir('/content')
    os.makedirs(f'DataScalogram/{train_val_test}')
    os.chdir(f'/content/DataScalogram/{train_val_test}')
    sampling_rate = 500
    scale_size = 100 + 1
    wavelet = 'morl'
    scales = np.arange(1, scale_size, 1) 
    coef_range = 1000
    
    for bird in BIRDS:
        count = 0
        os.mkdir(bird)
        os.chdir(f'/content/DataScalogram/{train_val_test}/{bird}')

        # Load the mp3 file
        audio_files = os.listdir(os.path.join(DATA_PATH, bird))
        print(f"{train_val_test}: {bird} Started!!")
        for audio_data in audio_files:
            signal, sr = librosa.load(os.path.join(DATA_PATH, bird, audio_data), sr=sampling_rate) # sr = sampling rate

            coef, freqs = pywt.cwt(signal, scales, wavelet) # Finding CWT with morlet wavelet
            
            plt.figure(figsize=(20, 10))
            plt.imshow(abs(coef[:, :coef_range]), cmap='coolwarm', aspect='auto')
            plt.axis(False)
            plt.tight_layout()
            count += 1
            plt.savefig(f'{bird}{count}.jpg', bbox_inches='tight', pad_inches=0.0)

        print(f"{train_val_test}: {bird} Done!!")
        os.chdir(f'/content/DataScalogram/{train_val_test}')