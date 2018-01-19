import markovify
import re
import spacy
nlp = spacy.load('en_core_web_sm')

class POSifiedText(markovify.NewlineText):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        SPEC_CHARS = list("'!@#$%^&*(),./’?") + ["\""]
        sentence = " ".join(word.split("::")[0] for word in words)
        for char in SPEC_CHARS:
            sentence = sentence.replace(" {}".format(char), char)
        return sentence

with open("comments.txt", encoding="cp1252") as f:
    text = f.read()

text_model = POSifiedText(text)

with open("markov.json", "w") as f:
    f.write(text_model.to_json())