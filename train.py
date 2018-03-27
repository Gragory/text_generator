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
    with open(arg.direct, "r") as f:
        text = f.read()
else:
    re_ad = input()
    while ord(re_ad) != 26:
        text += re_ad
        re_ad = input()
if low:
    text = text.lower()
list_of_words = re.findall(r"[\w']+", text)
probability_dict = {}
count_dict = {}
for i in range(len(list_of_words)-2):
    if not list_of_words[i + 1] in count_dict.keys():
        count_dict.update({list_of_words[i + 1]: {list_of_words[i + 2]: 1}})
    else:
        r = False
        if list_of_words[i + 2] in count_dict[list_of_words[i + 1]].keys():
            count_dict[list_of_words[i + 1]][list_of_words[i + 2]] += 1
        else:
            count_dict[list_of_words[i + 1]].update({list_of_words[i + 2]: 1})
for i in count_dict.keys():
    sum_of_counts = 0
    second = list(count_dict[i].keys())
    for i2 in range(len(second) - 1):
        count_dict[i][second[i2 + 1]] += count_dict[i][second[i2]]
        if i2 == len(second) - 2:
            sum_of_counts = count_dict[i][second[i2 + 1]]
    if sum_of_counts == 0:
        sum_of_counts = count_dict[i][second[-1]]
    additional_dict = {}
    for i2 in count_dict[i].keys():
        additional_dict.update({count_dict[i][i2]/sum_of_counts: i2})
    probability_dict.update({i: additional_dict})
with open(model, 'wb') as f:
    pickle.dump(probability_dict, f)
