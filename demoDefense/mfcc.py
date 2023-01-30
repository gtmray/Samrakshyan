import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

def mfcc_features(audio_file_path):

    signal, sr = librosa.load(audio_file_path, duration=10) # sr = sampling rate

    # Plot MFCCs
    mfccs = librosa.feature.mfcc(y=signal, n_mfcc=13, sr=sr) 
    # del_mfccs = librosa.feature.delta(mfccs)
    # del2_mfccs = librosa.feature.delta(mfccs, order=2)
    # mfccs_feat = np.concatenate((mfccs, del_mfccs, del2_mfccs))

    fig = plt.figure(figsize=(10, 5))
    librosa.display.specshow(mfccs, 
                            x_axis="time", 
                            sr=sr)
    plt.axis(False)
    plt.tight_layout()
    plt.savefig(f'tmp/mfcc.jpg')
    plt.show()
    plt.close(fig)
    
audio_file_path = 'largebilled.mp3'
mfcc_features(audio_file_path)