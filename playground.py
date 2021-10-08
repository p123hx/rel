import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Adherens junctions sdf dfdf R")
words = [t.lemma_.lower().strip() for t in doc]
print(words)