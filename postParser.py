import json
import sys
import re

print(sys.argv[1])

with open(sys.argv[1]) as f:
    data = json.load(f)

outputName = sys.argv[2]

prevEnd = 0
removeWords = []

niaCount = 0
niaCap = 3
niaMode = False

for i, w in enumerate(data['words']):
    if w['case'] == 'success':
        if re.compile(r'\d+').match(w['word']) and w['alignedWord'] == '<unk>' and data['transcript'][w['endOffset']] == '^':
            removeWords.append(i)
            continue
        if 'phones' in w:
            del w['phones']
        prevEnd = w['end']
        data['words'][i]['alligned'] = 'True'
        niaMode = False
    # try to automatically adjust times by looking at adjacent words start and end times.
    if w['case'] == 'not-found-in-audio':
        # if a line number was attempted to be adjusted remove it
        if re.compile(r'\d+').match(w['word']):
            removeWords.append(i)
            continue
        # modify data
        data['words'][i]['start'] = prevEnd
        nextStart = -1
        for j, v in enumerate(data['words'][i + 1:]):
            if v['case'] == 'success':
                nextStart = v['start']
                break
        data['words'][i]['end'] = nextStart
        data['words'][i]['case'] = 'success'
        if not niaMode:
            niaCount += 1
        if niaCount > niaCap:
            niaMode = True
            niaCount = 0
            # backwards tagging
            for j in range(max(i-niaCap, 0), i):
                data['words'][j]['alligned'] = 'False'
                data['words'][j]['case'] = 'not-found-in-audio'
                # if 'start' in data['words'][j]:
                #     del data['words'][j]['start']
                # if 'end' in data['words'][j]:
                #     del data['words'][j]['end']
        if niaMode:
            data['words'][i]['alligned'] = 'False'
            data['words'][i]['case'] = 'not-found-in-audio'
            # if 'start' in data['words'][i]:
            #     del data['words'][i]['start']
            # if 'end' in data['words'][i]:
            #     del data['words'][i]['end']

for i in sorted(removeWords, reverse=True):
    del data['words'][i]

line = []
for i, w in enumerate(data['words']):
    # detect line
    line.append(i)
    tc = w['endOffset']+1
    lineEnd = False
    while(re.compile(r'[^0-9^a-z^A-Z]').match(data['transcript'][tc]) is not None):
        if data['transcript'][tc] == '\n':
            lineEnd = True
            break
        tc += 1

    if lineEnd:
        success = False
        for j in line:
            if data['words'][j]['case'] == 'success':
                success = True
                break
        if success:
            for j in line:
                data['words'][j]['case'] = 'success'
        line = []

for i, w in enumerate(data['words']):
    if w['case'] == 'not-found-in-audio':
        if 'start' in data['words'][i]:
            del data['words'][i]['start']
        if 'end' in data['words'][i]:
            del data['words'][i]['end']

with open(sys.argv[2], 'w') as f:
    json.dump(data, f)
    # json.dump(data, f, indent=4, sort_keys=True)
