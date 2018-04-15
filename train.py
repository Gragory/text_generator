import re
import pickle
import argparse


def text_input(low, input_dir):
    if input_dir != "":
        with open(input_dir, "r") as f:
            text = f.read()
    else:
        re_ad = input()
        text = ""
        while ord(re_ad) != 26:
            text += re_ad
            re_ad = input()
    if low:
        text = text.lower()
    return re.findall(r"[\w']+", text)


def count_create(list_of_words):
    count_dict = {}
    for i in range(len(list_of_words) - 2):
        if not list_of_words[i + 1] in count_dict.keys():
            count_dict.update({list_of_words[i + 1]: {list_of_words[i + 2]: 1}})
        else:
            r = False
            if list_of_words[i + 2] in count_dict[list_of_words[i + 1]].keys():
                count_dict[list_of_words[i + 1]][list_of_words[i + 2]] += 1
            else:
                count_dict[list_of_words[i + 1]].update({list_of_words[i + 2]: 1})
    return count_dict


def sum_count(count_subdict):
    second = list(count_subdict.keys())
    for i2 in range(len(second) - 1):
        count_subdict[second[i2 + 1]] += count_subdict[second[i2]]
        if i2 == len(second) - 2:
            return count_subdict[second[i2 + 1]]
    return count_subdict[second[-1]]


def dumper(probability_dict, model):
    with open(model, 'wb') as f:
        pickle.dump(probability_dict, f)


def pars_func():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', dest='direct', type=str, default="", help='адрес файла с текстом (default= stdin)')
    parser.add_argument('--model', dest='model', type=str, help='адрес сохранения модели')
    parser.add_argument('--lc', action='store_true', default='store_false', dest='lc', help='приведение букв к строчным')
    return parser.parse_args()


def main(arg):
    dumper(count_create(text_input(arg.lc, arg.direct)), arg.model)


main(pars_func())
