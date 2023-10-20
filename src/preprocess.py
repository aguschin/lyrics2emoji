import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import DistilBertTokenizer, DistilBertModel


nlp = spacy.load("en_core_web_sm")
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertModel.from_pretrained("distilbert-base-uncased")
EMBEDDING_DIMENSION = 1536


def clean_text(text):
    doc = nlp(text)
    words = [
        token.text
        for token in doc
        if token.pos_ not in ["ADP", "CCONJ", "DET", "PUNCT"]
    ]
    text = " ".join(words)
    return text


def uni_to_emo(unicodes):
    """
    turn list of x-bit unicode of 1 emoji, for example [2F1K0, 0102], to emoji corressponding to concatenation of such code

    args:
        unicode: list of x-bit unicode of 1 emoji
    return:
        emoji corressponding to such code
    """
    emoji_str = ""
    for uni in unicodes:
        uni_hex = uni.zfill(8)
        uni_int = int(uni_hex, 16)
        emoji = chr(uni_int)
        emoji_str += emoji
    return emoji_str


def embed(value: str):
    encoded_input = tokenizer(value, return_tensors="pt")
    output = model(**encoded_input)
    return output.last_hidden_state.squeeze(0)[-1].detach().numpy().reshape(1, -1)


def get_lyrics_first_line(lyrics: str):
    return lyrics.split("\n")[0].replace("\r", "")


def get_lyrics_n_line(lyrics: str, n=1):
    return " ".join(lyrics.split("\n")[0:n]).replace("\r", "")
