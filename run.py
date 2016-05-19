import numpy as np
import librosa
import csv

import sys

print 'Argument List:', str(sys.argv)
filename = sys.argv[1]
songname = filename[:-4]


# filename = '6.wav'

steps = 0
def tick():
  steps += 1
  print('tick {0}'.format(steps))

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

outfile = '{0}_chromagram.csv'.format(songname)
chroma2 = np.transpose(chromagram)
with open(outfile, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(chroma2)

outfile = '{0}_beat_chroma.csv'.format(songname)
beatchroma2 = np.transpose(beat_chroma)
with open(outfile, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(beatchroma2)
 
outfile = '{0}_beat_features.csv'.format(songname)
beatfeatures2 = np.transpose(beat_features)
with open(outfile, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(beatfeatures2)

