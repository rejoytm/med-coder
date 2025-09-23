import re

from models import nlp_model

# Collapses multiple whitespace characters into a single space and removes leading/trailing whitespace
def collapse_and_strip_whitespace(string):
    return re.sub(r'\s+', ' ', string).strip()

# Removes stop words and lemmatizes the text
def remove_stop_words_and_lemmatize(string):
    doc = nlp_model(string)

    tokens = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and not token.is_punct
    ]

    return " ".join(tokens)