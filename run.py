import numpy as np
import librosa
import csv

filename = '6.wav'

steps = 0
def tick():
  steps += 1
  print(steps)

tick()

# filename = librosa.util.example_audio_file()

y, sr = librosa.load(filename)
tick()

# separate harmonic and percussive
y_harmonic, y_percussive = librosa.effects.hpss(y)
tick()

# analyze rhythm
tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr)
tick()

mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
tick()
mfcc_delta = librosa.feature.delta(mfcc)
tick()
beat_mfcc_delta = librosa.feature.sync(np.vstack([mfcc, mfcc_delta]), beat_frames)
tick()

# analyze frequencies for every time slice
chromagram = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)
tick()

beat_chroma = librosa.feature.sync(chromagram, beat_frames, aggregate=np.median)
tick()

beat_features = np.vstack([beat_chroma, beat_mfcc_delta])
tick()

outfile = 'chromagram.csv'
chroma2 = np.transpose(chromagram)
with open(outfile, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(chroma2)

outfile = 'beat_chroma.csv'
beatchroma2 = np.transpose(beat_chroma)
with open(outfile, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(beatchroma2)
 
outfile = 'beat_features.csv'
beatfeatures2 = np.transpose(beat_features)
with open(outfile, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(beatfeatures2)

