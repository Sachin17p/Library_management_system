import random

with open('copy.txt', 'r+') as f:
    lines = f.readlines()
    f.seek(0)
    for line in lines:
        random_number = str(random.randint(1, 20))
        f.write(line.strip() + ',' + random_number + '\n')
