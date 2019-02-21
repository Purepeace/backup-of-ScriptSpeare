import json
import sys
import re

print(sys.argv[1])

with open(sys.argv[1]) as f:
    data = json.load(f)

prevEnd = 0
removeWords = []

for i, w in enumerate(data['words']):
    if w['case'] == 'success':
        if re.compile(r'\d+').match(w['word']) and w['alignedWord'] == '<unk>' and data['transcript'][w['endOffset']] == '^':
            removeWords.append(i)
            continue
        if 'phones' in w:
            del w['phones']
        # data['words'][i]['source'] = 'gentle'
        prevEnd = w['end']
    # try to automatically adjust times by looking at adjacent words start and end times.
    if w['case'] == 'not-found-in-audio':
        # if a line number was attempted to be adjusted remove it
        if re.compile(r'\d+').match(w['word']):
            removeWords.append(i)
            continue
        # modify data
        # data['words'][i]['source'] = 'auto'
        data['words'][i]['start'] = prevEnd
        nextStart = -1
        for j, v in enumerate(data['words'][i + 1:]):
            if v['case'] == 'success':
                nextStart = v['start']
                break
        data['words'][i]['end'] = nextStart

for i in sorted(removeWords, reverse=True):
    del data['words'][i]

with open("time-auto-adjusted_" + sys.argv[1], 'w') as f:
    json.dump(data, f)
    # json.dump(data, f, indent=4, sort_keys=True)
