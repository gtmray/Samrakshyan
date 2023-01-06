import os
import librosa
import soundfile as sf
import os
from audiomentations import Compose, AddGaussianNoise
from pydub import AudioSegment

data_path = 'largebilled.mp3'

augment_raw_audio = Compose(
    [
        AddGaussianNoise(min_amplitude=0.01, max_amplitude=0.015, p=1)
    ]
)

x, sr = librosa.load(data_path)
augmented_signal = augment_raw_audio(x, sr)
sf.write(f'tmp/{data_path}augsf.wav', augmented_signal, sr, format='wav')


audio_segment = AudioSegment(
    x.astype("float32").tobytes(), 
    frame_rate=sr,
    sample_width=x.dtype.itemsize, 
    channels=1
)

audio_segment.export(f"tmp/{data_path}aug.mp3", format="mp3")