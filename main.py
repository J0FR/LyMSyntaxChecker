filename = 'files/test.txt'

rules = {}

with open(filename) as f:
    lines = f.read().splitlines()

for i in lines:
    if(len(i)==0):
        lines.remove(i)

for line in lines:
    pass

print(lines)