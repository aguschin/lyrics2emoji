import transformers
import numpy as np
import pandas as pd
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from transformers import DistilBertTokenizer, DistilBertModel

"""
Usage:
from text_to_emoji import translate_text
translate_text(TXT)

Output:
strings of emojis
"""


# emoji source and column of emoji
df = pd.read_csv('emoji.csv')
emo_col = 'emojis'

# embedding of each emoji name
vectorized_name = np.load('emoji_name_vectorized.npy')

# parser, model, tokenizer
nlp = spacy.load("en_core_web_sm")
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained("distilbert-base-uncased")

def clean_text(text):
    doc = nlp(text)
    words = [
      token.text for token in doc
      if token.pos_ not in ['ADP', 'CCONJ', 'DET', 'PUNCT']
    ]
    text = ' '.join(words)
    return text

def pre_process(value: str):
    encoded_input = tokenizer(value, return_tensors='pt')
    output = model(**encoded_input)
    return output.last_hidden_state.squeeze(0)[-1].detach().numpy().reshape(1, -1)

def find_closest(word, n=1):
    vector = pre_process(word)
    similarities = cosine_similarity(vectorized_name, vector)# * 0.95 + 0.05 * cosine_similarity(vectorized3, vector)
    if n == 1:
        return df[emo_col].iloc[np.argmax(similarities)]
    return list(df[emo_col].iloc[similarities.ravel().argsort()[-n:][::-1]])

def translate_text(text, k=1):
    translated = ""
    for word in clean_text(text).split():
        closest = find_closest(word, n=k)
        translated += closest[-1] if isinstance(closest, list) else closest
    return translated