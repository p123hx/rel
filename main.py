# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import json
import spacy
from spacy.tokenizer import Tokenizer
from nltk.tokenize import TweetTokenizer
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
nlp = spacy.load("en_core_web_sm")
def tokenize_helper(text):
    tknzr = TweetTokenizer()
    tokenLst = tknzr.tokenize(text)
    return tokenLst
def helper():
    skipped_count = 0
    in_files = ["ori_dev.json", "ori_test.json", "ori_training.json"]
    out_files = ["relations_dev.txt", "relations_test.txt", "relations_training.txt"]
    for i in range(3):
        file = in_files[i]
        out_file = out_files[i]
        f = open(file)
        out_array = []
        data = json.load(f)
        for sentences in data["annotation"]["medlinecitation"]:
            if len(sentences) == 0 or len(sentences["sentence"]) != 2:  # just title and abstract
                skipped_count += 1
                continue
            for sentence in sentences["sentence"]:  # just title and abstract
                dict_tmp = {}
                print("sentence: ", sentence)
                text = sentence["@text"]
                dict_tmp["document"] = text
                dict_tmp["tokens"], dict_tmp["relations"] = [], []
                print("text: ",text)
                # mytokens = nlp(text)
                # tokenLst = [word.lemma_.lower().strip() for word in mytokens]
                tokenLst = tokenize_helper(text)
                print("tokenLst: ",tokenLst)
                # tknzr = TweetTokenizer()
                # tokenLst = tknzr.tokenize(text)
                if "predications" not in sentence:
                    skipped_count += 1
                    continue
                if "predication" not in sentence["predications"]:
                    skipped_count += 1
                    continue
                for token in sentence["predications"]["predication"]:
                    rela_dict = {}
                    if ("subject" not in token) or ("object" not in token):
                        skipped_count += 1
                        continue
                    xjects = [token["subject"], token["object"]]
                    ts = []
                    for xject in xjects:
                        token_dict = {}
                        token_dict["text"], token_dict["start"] = xject["@text"], int(xject["@charoffset"])
                        token_dict["end"] = token_dict["start"] + len(token_dict["text"])
                        # tmp_tockes = tknzr.tokenize(token_dict["text"])
                        # tokenizer = Tokenizer(nlp.vocab)
                        # tmp_tockes = tokenizer(token_dict["text"])
                        tmp_tockes = tokenize_helper(token_dict["text"])
                        print("token_dict[\"text\"]: ",token_dict["text"])
                        # mytokens = nlp(token_dict["text"])
                        # print("mytokens: ",mytokens)
                        # tmp_tockes = [word.lemma_.lower().strip() for word in mytokens]
                        # tmp_tockes = [w.lemma_.lower().strip()  for w in mytokens]
                        print("tmp_tockes[0]: ",tmp_tockes[0])

                        # print("token_dict[\"text\"]: ",token_dict["text"])
                        print("tokenLst: ",tokenLst)
                        #@TODO
                        t_start = tokenLst.index(tmp_tockes[0])
                        token_dict["token_start"] = t_start
                        ts.append(t_start)
                        tLst_tmp = nlp(token_dict["text"])
                        token_dict["token_end"] = token_dict["token_start"] + len(tLst_tmp) - 1
                        token_dict["entityLabel"] = xject["semantictypes"]["semantictype"][0]
                        #
                        dict_tmp["tokens"].append(token_dict)

                    rela_dict["child"] = ts[1]
                    rela_dict["head"] = ts[0]
                    rela_dict["relationLabel"] = token["predicate"]["@type"]
                    #
                    dict_tmp["relations"].append(rela_dict)
                out_array.append(dict_tmp)
        # with open(out_file, 'w') as json_file:
        #     json.dump(out_array, json_file)
        #     input("file written")
        json_object = json.dumps(out_array, indent=4)
        # Writing to sample.json
        with open(out_file, "w") as outfile:
            outfile.write(json_object)
    print("skipped:", skipped_count)
    # @TODO: backup extra lable


def playground():
    text = "Finally, epidural morphine (30 microg/10 microl) in oxytocin-treated rats, although resulting in no change of labor duration, significantly decreased the number of stretches (8 +/- 2 vs. 57 +/- 12 for epidural saline) and the number of c-Fos-positive neurons in the lumbosacral spinal segments (80 +/- 25 vs. 165 +/- 17 for epidural saline)"
    # tknzr = TweetTokenizer()
    # tokenLst = tknzr.tokenize("oxytocin-treated")
    # nlp = English()
    # # Create a blank Tokenizer with just the English vocab
    # tokenizer = Tokenizer(nlp.vocab)
    #
    # # Construction 2
    # from spacy.lang.en import English
    # nlp = English()
    # # Create a Tokenizer with the default settings for English
    # # including punctuation rules and exceptions
    # tokenizer = nlp.tokenizer
    # print(tokenLst)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    helper()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
