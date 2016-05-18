import pandas as pd
import numpy as np

counter = 0
def tick():
	counter += 1
	print('tick {0}'.format(counter))

music_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

tick()

df = pd.read_csv('chromagram3.csv')

tick()

probs = []
for k in music_notes:
    s = df[k].value_counts()
    prob = s.get(1)
#     prob = df[k].sum()
    print('{0}: {1}'.format(k, prob))
    probs.append(prob)

tick()


def getLargestIndex(numbers):
    return numbers.index(max(numbers))

def getSecondLargest(numbers):
    count = 0
    m1 = m2 = float('-inf')
    for x in numbers:
        count += 1
        if x > m2:
            if x >= m1:
                m1, m2 = x, m1            
            else:
                m2 = x
    return m2 if count >= 2 else None

def getSecondLargestIndex(numbers):
    return numbers.index(getSecondLargest(numbers))



def getLargestKey(all_prob):
    tonic = getLargestIndex(all_prob)
    return getKey(tonic, all_prob)

def getSecondLargestKey(all_prob):
    tonic = getSecondLargestIndex(all_prob)
    return getKey(tonic, all_prob)

def getSum(arr, indices):
    sum = 0
    for k in indices:
        sum += arr[k]
    return sum

minor_scale = [2, 3, 5, 7, 8, 10]
major_scale = [2, 4, 5, 7, 9, 11]

def isMinor(tonic, all_prob):
#     all_prob[minorIndex] > all_prob[majorIndex]
    minor_indices = [((k + tonic) % 12) for k in minor_scale]
    minor_sum = getSum(all_prob, minor_indices)
                       
                       
    major_indices = [((k + tonic) % 12) for k in major_scale]
    major_sum = getSum(all_prob, major_indices)
    print('Minor {0}'.format(minor_sum))
    print('Major {0}'.format(major_sum))
    return minor_sum > major_sum
    
def getKey(tonic, all_prob):
    minorIndex = (tonic + 3) % 12
    majorIndex = (tonic + 4) % 12
    third = 3 if isMinor(tonic, all_prob) else 4
    return tonic, third



def getKeyNameAndProb(tonic, third):
    tonic_name = music_notes[tonic]
    feel = 'Minor' if third == 3 else 'Major'
    combo = '{0} {1}'.format(tonic_name, feel)
    print(combo)
    x = probs[tonic]
    y = probs[(tonic + third) % 12]
    total_prob = x * y
    print(total_prob)
    return combo, total_prob



def isSad(x1, x2):
    temp = x1 if x1[1] > x2[1] else x2
    print(temp[0])
    return 'Minor' in temp[0]


tick()

tup1 = getLargestKey(probs)

tick()

x1 = getKeyNameAndProb(tup1[0], tup1[1])
print('-' * 10)
tup2 = getSecondLargestKey(probs)

tick()

x2 = getKeyNameAndProb(tup2[0], tup2[1])
print('-' * 10)
sad = isSad(x1, x2)
result = 'Sad' if sad else 'Not Sad'
print(result)











