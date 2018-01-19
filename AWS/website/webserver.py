# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
import markovify

with open("../../markov_with_overtime.json", "r") as f:
    data = f.read()
    print("Loaded the chain")

app = Flask(__name__)

text_model = None

def load_model():
    global text_model

    # Attempt to use 'spaCy' to create more
    # natural language-esque sentences.
    # If the import fails use the default Markovify
    # class.
    # This is a hacky way to run the same code on Ubuntu
    # and Windows as spaCy fails Windows installations.
    try:
        # Source documentation:
        # https://github.com/jsvine/markovify#extending-markovifytext
        import spacy
        import json
        nlp = spacy.load('en_core_web_sm')

        class POSifiedText(markovify.NewlineText):
            def word_split(self, sentence):
                return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

            def word_join(self, words):
                SPEC_CHARS = list("'!@#$%^&*(),./’?’“") + ["\"", "n't", "n’t", "nt"]
                sentence = " ".join(word.split("::")[0] for word in words)
                for char in SPEC_CHARS:
                    sentence = sentence.replace(" {}".format(char), char)
                return sentence

        text_model = POSifiedText.from_json(data)
        print("Running off of POS Markov chain")
    except Exception as e:
        text_model = markovify.NewlineText.from_json(data)
        print("Running off of non-POS Markov chain")

# After the server starts up, but before any request has been 
# sent to it.
@app.before_first_request
def before_first_request():
    load_model()

@app.route("/", methods=["POST", "GET"])
def index():
    sentences = []
    # Attempt to get a start word from either POST or GET, doesn't matter
    start_word = request.values.get("start", "")
    if start_word:
        try:
            sentences = [text_model.make_sentence_with_start(start_word) for _ in range(5)]
        except Exception as e:
            # start_word is not a valid seed
            pass
    else:
        sentences = [text_model.make_short_sentence(140) for _ in range(5)]
    # Send it to the template
    return render_template("index.html", sentences=sentences, start_word=start_word)