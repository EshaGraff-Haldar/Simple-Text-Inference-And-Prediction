import json
import os

cwd = os.getcwd()

with open(cwd + "/dictionary.txt", "r") as fp:
    data = json.load(fp)

mono_dict = data["mono"]
bi_dict = data["bi"]
tri_dict = data["tri"]


# text-inference
def text_inference(sentence, model_dict):
    s_list = sentence.split(" ")
    i = s_list.index("-")

    left_context = s_list[i-2] + " " + s_list[i-1]
    right_context = s_list[i+1]
    _, _, last_word = left_context.partition(" ")
    
    trial, word, probs = "", "", {}

    # retrieving and normalising the left_context transition probabilities
    probs_left_context = model_dict[left_context]
    total = sum(dict.values(probs_left_context))
    if total!=1:
        for k in probs_left_context.keys():
            probs_left_context[k] = probs_left_context[k] / total
        model_dict[left_context] = probs_left_context

    # finding right context transition probabilities
    for candidate in probs_left_context:
        trial = last_word +" " + candidate
        probs_right_context = model_dict[trial]
        #normalising the last_word + candidate transition probabilities
        total = sum(dict.values(probs_right_context))
        if total!=1:
            for k in probs_right_context.keys():
                probs_right_context[k] = probs_right_context[k] / total
            model_dict[trial] = probs_right_context

        #finding probablitity of transitioning to right_context
        try: probs[candidate] = probs_right_context[right_context]
        except: probs[candidate] = 0

    # multiplying probabilities for left_context and right_context
    for candidate in probs.keys(): probs[candidate] = probs[candidate] * probs_left_context[candidate]

    #normalising probabilities for candidates
    total = sum(probs.values())
    for candidate in probs.keys():
        if probs[candidate] !=0: probs[candidate] = probs[candidate] / total 
    probs = dict(sorted(probs.items(), key=lambda item: item[1],reverse = True))
    print(probs)

    word = max(probs, key=probs.get)
    sentence = sentence.replace("-", word)
    print(sentence)

text_inference("He knows - about", bi_dict)
