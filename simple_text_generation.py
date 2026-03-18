import random
import json

with open("dictionary.txt", "r") as fp:
    data = json.load(fp)

mono_dict = data["mono"]
bi_dict = data["bi"]
tri_dict = data["tri"]


#Generating output
def generate(model_dict, prompt, length):
    next_word, prompt = "", prompt.lower()
    sentence = prompt
    for i in range(length):
        if prompt in model_dict.keys():
            next_word = random.choices(list(model_dict[prompt].keys()), weights=list(model_dict[prompt].values()), k=1)[0]
            prompt = prompt.split(' ', 1)[1] + " " + next_word
            sentence = sentence +" " + next_word
        else:
            next_word = random.choice(list(model_dict.keys()))
            prompt = prompt.split(' ', 1)[1] + " " + next_word
            sentence = sentence + " " + next_word
    print("\n" + sentence)

generate(bi_dict, "He wishes", 300)
