import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

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

def mel_features(audio_file_path):

    signal, sr = librosa.load(audio_file_path,duration=10) # sr = sampling rate

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
    librosa.display.specshow(mel_spec, fmin=FMIN,y_axis='linear')
    plt.axis(False)
    plt.tight_layout()
    plt.savefig(f'tmp/melspec.jpg')
    plt.show()
    plt.close(fig)
    
audio_file_path = 'largebilled.mp3'
mel_features(audio_file_path)