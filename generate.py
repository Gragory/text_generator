import pickle
import random
import argparse


def load_dict(model):
    with open(model, "rb") as f:
        return pickle.load(f)


def give_first(seed, model):
    probability_dict = load_dict(model)
    if seed != "":
        return seed
    else:
        return random.choice(list(probability_dict.keys()))


def find_prob(list_of_going_after_first):
    addition = []
    for i in list_of_going_after_first.keys():
        addition.extend([i] * list_of_going_after_first[i])
    return random.choice(addition)


def step_of_gen(model, first_word):
    probability_dict = load_dict(model)
    if not (first_word in probability_dict.keys()):
        return random.choice(list(probability_dict.keys()))
    else:
        return find_prob(probability_dict[first_word])


def gen_text(model, length_of_text, first_word):
    generated_text = [first_word]
    for i in range(length_of_text - 1):
        first_word = step_of_gen(model, first_word)
        generated_text.append(first_word)
    return ' '.join(generated_text)


def text_output(output_directory, generated_text):
    if output_directory != "":
        with open(output_directory, "w") as f:
            f.write(generated_text)
    else:
        print(generated_text)


def main(arg):
    text_output(arg.out, gen_text(arg.model, arg.length, give_first(arg.seed, arg.model)))


def pars_func():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', dest='model', type=str, help='адрес изъятия модели')
    parser.add_argument('--seed', dest='seed', type=str, default="", help='начальное слово (default= случайное)')
    parser.add_argument('--length', dest='length', type=int, help='длина генерируемый последовательности')
    parser.add_argument('--output', dest='out', type=str, default="", help='адрес вывода (default= stdout)')
    return parser.parse_args()


main(pars_func())
