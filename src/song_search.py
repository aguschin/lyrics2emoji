import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from transformers import DistilBertTokenizer, DistilBertModel
from annoy import AnnoyIndex

"""
Usage:
from song_search import find_nearest_song_annoy
find_nearest_song_annoy(INPUT, n)

Input:
string of lyrics or emojis

Output:
list of first n songs with closest embeddings to the input
"""

# lyrics source and column of song name
df = pd.read_csv('../data/sample_data/top_10_artists_songs.csv')
song_col = 'song_name'
vectorized_lyrics = np.load('../data/sample_data/lyrics_vectorized.npy')

# parser, model, tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained("distilbert-base-uncased")
embedding_dimension = model.config.hidden_size

# create annoy index for faster search
annoy_index = AnnoyIndex(embedding_dimension, 'dot')
for i, vector in enumerate(vectorized_lyrics):
    vector = vector.squeeze()
    vector = vector / np.linalg.norm(vector)
    annoy_index.add_item(i, vector)
annoy_index.build(20)

def lyrics_pre_process(lyrics: str):
    return lyrics.split('\n')[0].replace('\r', '')

def embed(value: str):
    encoded_input = tokenizer(value, return_tensors='pt')
    output = model(**encoded_input)
    res = output.last_hidden_state.squeeze(0)[-1].detach().numpy().reshape(1, -1)

    res = res / np.linalg.norm(res)
    return res

def find_nearest_song_annoy(emojis, n=1):
    idx, dist = annoy_index.get_nns_by_vector(embed(emojis).reshape(-1,1), n, include_distances=True)
    return list(df[song_col].iloc[idx])