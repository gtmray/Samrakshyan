import pywt
import librosa
import numpy as np
import matplotlib.pyplot as plt

filename = 'spiny.mp3'
sampling_rate = 500
x, sr = librosa.load(filename, sr=sampling_rate)

scale_size = 100 + 1
wavelet = 'morl'
scales = np.arange(1, scale_size, 1) 
coef_range = 1000

coef, freqs = pywt.cwt(x, scales, wavelet) # Finding CWT with morlet wavelet

# Scalogram plot

plt.figure(figsize=(20, 10))
plt.imshow(abs(coef[:, :coef_range]), cmap='coolwarm', aspect='auto')
# plt.axis(False)

# Turn off tick labels
plt.xticks([])
plt.yticks([])
plt.xlabel('Time', fontsize=20)
plt.ylabel('Scales', fontsize=20)
plt.colorbar()
plt.tight_layout()
plt.savefig(f'tmp/scalogram.jpg', bbox_inches='tight', pad_inches=0.0)
plt.show()