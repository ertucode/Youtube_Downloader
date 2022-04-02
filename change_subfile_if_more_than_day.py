import math

with open("after1day.txt", mode='r') as f:
    updated_content = f.read()

def changeNumbers(instr):
    f2 = str(int(instr[0] + instr[1]) + 24)
    s2 = str(int(instr[17] + instr[18]) + 24)
    newstr = f"{f2}{instr[2:17]}{s2}{instr[19:]}"
    return newstr

lines = updated_content.split("\n")

for i in range(math.ceil(len(lines)/4)):
    lines[i*4+1] = changeNumbers(lines[i*4+1])

output = "\n".join(lines)

with open("after3day.txt", mode='w') as f:
    f.write(output)

