import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import embed, clean_text

"""
Usage:
from text_to_emoji import translate_text
translate_text(TXT)

Output:
strings of emojis
"""

# emoji source and column of emoji
df = pd.read_csv('../data/emoji.csv')
emo_col = 'emoji'

# embedding of each emoji name
vectorized_name = np.load('../data/emoji_name_vectorized.npy')


def find_closest(word, n=1):
    vector = embed(word)
    similarities = cosine_similarity(vectorized_name, vector) 
    if n == 1:
        return df[emo_col].iloc[np.argmax(similarities)]
    return list(df[emo_col].iloc[similarities.ravel().argsort()[-n:][::-1]])


def translate_text(text, k=1):
    translated = ""
    for word in clean_text(text).split():
        closest = find_closest(word, n=k)
        translated += closest[-1] if isinstance(closest, list) else closest
    return translated
