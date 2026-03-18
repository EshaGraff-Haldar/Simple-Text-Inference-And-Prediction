import re
import json
import os

cwd = os.getcwd()

#reading input_texts
def read_novels(texts, mono_dict, bi_dict, tri_dict):
    for t in texts:
        compiled_text = ""
        with open(t) as input_text:
            for line in input_text:
                line = line.strip().replace("’", "'")
                line = line.replace("--", "-")
                line = line.replace(". . .", "...")
                line = line.replace("_", "")
                line = line.replace(" \" ", "")
                #line = (re.sub(r'[^\w\d\s\']+', '', line))
        
                if line.lower().startswith("chapter") == False and line.upper()!=line and line!="":
                    compiled_text = compiled_text + " " + line
        text_list = list(compiled_text.split(" "))

        #creating markov chain monogram dictionary
        for word_index in range(len(text_list) - 1):
            word_group = text_list[word_index]
            next_word = text_list[word_index+1]

            if word_group in mono_dict.keys():
                if next_word in (mono_dict[word_group]).keys():
                    mono_dict[word_group][next_word] = mono_dict[word_group][next_word]+1
                else:
                    mono_dict[word_group][next_word] = 1
            else:
                mono_dict[word_group] = { next_word:1 }

        #creating markov chain bigram dictionary
        for word_index in range(len(text_list) - 2):
            word_group = text_list[word_index] + " " + text_list[word_index+1]
            next_word = text_list[word_index+2]

            if word_group in bi_dict.keys():
                if next_word in (bi_dict[word_group]).keys():
                    bi_dict[word_group][next_word] = bi_dict[word_group][next_word]+1
                else:
                    bi_dict[word_group][next_word] = 1
            else:
                bi_dict[word_group] = { next_word:1 }

        #creating markov chain trigram dictionary
        for word_index in range(len(text_list) - 3):
            word_group = text_list[word_index] + " " + text_list[word_index+1] + " " + text_list[word_index+2]
            next_word = text_list[word_index+3]

            if word_group in tri_dict.keys():
                if next_word in (tri_dict[word_group]).keys():
                    tri_dict[word_group][next_word] = tri_dict[word_group][next_word]+1
                else:
                    tri_dict[word_group][next_word] = 1
            else:
                tri_dict[word_group] = { next_word:1 }


# creating word dictionary
mono_dict = {}
bi_dict = {}
tri_dict = {}
texts = ["jane-eyre.txt", "shirley.txt", "harry-potter-1.txt", "harry-potter-2.txt", "harry-potter-3.txt", "harry-potter-4.txt",
         "anne-of-green-gables.txt", "the-call-of-the-wild.txt", "the-jungle-book.txt", "war-and-peace.txt",
         "the-picture-of-dorian-gray.txt", "the-secret-garden.txt", "little-women.txt"]
for t in range(len(texts)):
    texts[t] = cwd +"/" + texts[t]
    
read_novels(texts, mono_dict, bi_dict, tri_dict)


#transferring to dictionary.txt
with open("dictionary.txt", "w") as fp:
    json.dump({
        "mono": mono_dict,
        "bi": bi_dict,
        "tri": tri_dict
    }, fp)