# Feature extraction example
import numpy as np
import librosa
import csv

print('1')
# Load the example clip
# filename = librosa.util.example_audio_file()
filename = '6.wav'
y, sr = librosa.load(filename)
print('2')
# Separate harmonics and percussives into two waveforms
y_harmonic, y_percussive = librosa.effects.hpss(y)
print('3')
# Beat track on the percussive signal
tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,
                                             sr=sr)
print('4')
# Compute MFCC features from the raw signal
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
print('5')
# And the first-order differences (delta features)
mfcc_delta = librosa.feature.delta(mfcc)
print('6')
# Stack and synchronize between beat events
# This time, we'll use the mean value (default) instead of median
beat_mfcc_delta = librosa.feature.sync(np.vstack([mfcc, mfcc_delta]),
                                       beat_frames)
print('7')
# Compute chroma features from the harmonic signal
chromagram = librosa.feature.chroma_cqt(y=y_harmonic,
                                        sr=sr)
print('8')
# Aggregate chroma features between beat events
# We'll use the median value of each feature between beat frames
beat_chroma = librosa.feature.sync(chromagram,
                                   beat_frames,
                                   aggregate=np.median)
print('9')
# Finally, stack all beat-synchronous features together
beat_features = np.vstack([beat_chroma, beat_mfcc_delta])
print('10')

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

