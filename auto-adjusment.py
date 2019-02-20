import json
import sys

print(sys.argv[1])

with open(sys.argv[1]) as f:
    data = json.load(f)

prevEnd = 0
# totalDuration = 9000

for i, w in enumerate(data['words']):
    if w['case'] == 'success':
        prevEnd = w['end']
    # try to automatically adjust times by looking at adjacent words start and end times.
    if w['case'] == 'not-found-in-audio':
        # modify data
        data['words'][i]['case'] = 'auto-adjusted'
        data['words'][i]['start'] = prevEnd
        nextStart = -1
        for j, v in enumerate(data['words'][i + 1:]):
            if v['case'] == 'success':
                nextStart = v['start']
                # successFound = True
                break
        data['words'][i]['end'] = nextStart

with open("time-auto-adjusted_" + sys.argv[1], 'w') as f:
    json.dump(data, f, indent=4, sort_keys=True)
