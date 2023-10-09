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
df = pd.read_csv('data/sample_data/top_10_artists_songs.csv')
song_col = 'song_name'
vectorized_lyrics = np.load('data/sample_data/lyrics_vectorized.npy')

# parser, model, tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained("distilbert-base-uncased")
embedding_dimension = model.config.hidden_size

def pre_process(value: str):
    encoded_input = tokenizer(value, return_tensors='pt')
    output = model(**encoded_input)
    return output.last_hidden_state.squeeze(0)[-1].detach().numpy().reshape(1, -1)

def find_nearest_song_annoy(emojis, n=1):
    annoy_index = AnnoyIndex(embedding_dimension, 'euclidean')

    for i, vectorized_lyrics in enumerate(vectorized_lyrics):
        annoy_index.add_item(i, vectorized_lyrics)

    annoy_index.build(10)
    idx = annoy_index.get_nns_by_vector(pre_process(emojis).reshape(-1,1), n)
    return list(df[song_col].iloc[idx])