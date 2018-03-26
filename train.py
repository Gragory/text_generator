import re
import pickle
import argparse

text = ""

parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', dest='direct', type=str, default="", help='адрес файла с текстом (default= stdin)')
parser.add_argument('--model', dest='model', type=str, help='адрес сохранения модели')
parser.add_argument('--lc', action='store_true', default='store_false', dest='lc', help='приведение букв к строчным')
arg = parser.parse_args()
model = arg.model
low = arg.lc

if arg.direct != "":
    f = open(arg.direct, "r")
    text = f.read()
    f.close()
else:
    r_ad = input()
    while ord(r_ad) != 26:
        text += r_ad
if low:
    text = text.lower()
l_st = re.findall(r"[\w']+", text)
d = {}
d_2 = {}
for i in range(len(l_st)-2):
    if not l_st[i + 1] in d_2.keys():
        d_2.update({l_st[i + 1]: {l_st[i + 2]: 1}})
    else:
        r = False
        if l_st[i + 2] in d_2[l_st[i + 1]].keys():
            d_2[l_st[i + 1]][l_st[i + 2]] += 1
        else:
            d_2[l_st[i + 1]].update({l_st[i + 2]: 1})
for i in d_2.keys():
    su_m = 0
    second = list(d_2[i].keys())
    for i2 in range(len(second) - 1):
        d_2[i][second[i2 + 1]] += d_2[i][second[i2]]
        if i2 == len(second) - 2:
            su_m = d_2[i][second[i2 + 1]]
    if su_m == 0:
        su_m = d_2[i][second[-1]]
    d_1 = {}
    for i2 in d_2[i].keys():
        d_1.update({d_2[i][i2]/su_m: i2})
    d.update({i: d_1})
f = open(model, 'wb')
pickle.dump(d, f)
f.close()
