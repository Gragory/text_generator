import pickle
import random
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--model', dest='model', type=str, help='адрес изъятия модели')
parser.add_argument('--seed', dest='seed', type=str, default="", help='начальное слово (default= случайное)')
parser.add_argument('--length', dest='length', type=int, help='длина генерируемый последовательности')
parser.add_argument('--output', dest='out', type=str, default="", help='адрес вывода (default= stdout)')
arg = parser.parse_args()
model = arg.model
seed = arg.seed
lth = arg.length
out = arg.out

f = open(model, "rb")
d = pickle.load(f)
f.close()

if seed != "":
    first = seed
else:
    first = random.choice(list(d.keys()))

gen = first
for i in range(lth):
    if not (first in d.keys()):
        first = random.choice(list(d.keys()))
    else:
        x = random.random()
        l_first = list(d[first].keys())
        z_f = True
        for i2 in range(len(l_first) - 1):
            if (l_first[i2 + 1] >= x) and (l_first[i2] < x):
                first = d[first][l_first[i2]]
                z_f = False
                break
        if z_f:
            first = d[first][l_first[0]]
    gen = "{} {}".format(gen, first)
if out != "":
    f = open(out, "w")
    f.write(gen)
    f.close()
else:
    print(gen)
