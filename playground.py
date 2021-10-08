import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a sentence.")
words = [t.text for t in doc]
print(words)