import re
import sys

replacementDict = {"_": " ",
                   "ˆ": "",
                   }


with open(sys.argv[1]) as f:
    data = f.read()

for k, v in replacementDict.items():
    data = re.sub(k, v, data)

new_data = ''
for i, l in enumerate(iter(data.splitlines())):
    new_data = ''.join([new_data, str(i), '^', l, '\n'])

name = "preParsed-" + sys.argv[1].split('/')[-1]

with open(name, 'w') as f:
    f.write(new_data)

print(name)
