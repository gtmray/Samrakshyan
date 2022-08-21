from pydub import AudioSegment
import math
import os
import numpy as np

validAudio = lambda audio, amp_threshold: True if audio.max > amp_threshold else False
def splitAudio(audio_file, export_category, sec_to_split=10):
    global temp_n
    temp_n = 0
    mili=1000
    export_folder = f'/content/splitted10Audio/{export_category}/'
    export_name = audio_file[:9]
    exportFormat = 'mp3'
    try:
        audio = AudioSegment.from_mp3(audio_file)
    except:
        print("File handled: ", audio_file)
        audio = AudioSegment.from_wav(audio_file)
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

                        # extraAudio = audio[splits[n+2]*mili:duration]
            # if validAudio(extraAudio, th):
            #     extraAudio.export(f'{export_folder}/{export_name}Extra.{exportFormat}', format=exportFormat)

os.chdir('/content')
export_folder = '/content/splitted10Audio/'
os.mkdir(export_folder)

DATA_PATH = '/content/drive/MyDrive/MajorProjectDataset'
BIRDS = os.listdir(DATA_PATH)

for bird in BIRDS:
    os.mkdir(os.path.join(export_folder, bird))
    for audio_file in os.listdir(os.path.join(DATA_PATH, bird)):
        os.chdir(os.path.join(DATA_PATH, bird))
        splitAudio(audio_file, export_category=bird)