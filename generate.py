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
length_of_text = arg.length
output_directory = arg.out

with open(model, "rb") as f:
    probability_dict = pickle.load(f)

if seed != "":
    first_word = seed
else:
    first_word = random.choice(list(probability_dict.keys()))

generated_text = first_word
for i in range(length_of_text-1):
    if not (first_word in probability_dict.keys()):
        first_word = random.choice(list(probability_dict.keys()))
    else:
        x = random.random()
        list_of_going_after_first = list(probability_dict[first_word].keys())
        the_element_i_need_is_numbered_zero_flag = True
        for i2 in range(len(list_of_going_after_first) - 1):
            if (list_of_going_after_first[i2 + 1] >= x) and (list_of_going_after_first[i2] < x):
                first_word = probability_dict[first_word][list_of_going_after_first[i2]]
                the_element_i_need_is_numbered_zero_flag = False
                break
        if the_element_i_need_is_numbered_zero_flag:
            first_word = probability_dict[first_word][list_of_going_after_first[0]]
    generated_text = "{} {}".format(generated_text, first_word)
if output_directory != "":
    with open(output_directory, "w") as f:
        f.write(generated_text)
else:
    print(generated_text)
