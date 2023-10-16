import numpy as np
import pandas as pd
from annoy import AnnoyIndex
from preprocess import embed, EMBEDDING_DIMENSION


# lyrics source and column of song name
df = pd.read_json('../data/sample_data/top_10_spotify_translated.json')
song_col = 'song_name'

# parser, model, tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained("distilbert-base-uncased")
embedding_dimension = model.config.hidden_size

def get_sub_lyrics(lyrics):
    return lyrics[:min(800, len(lyrics))].strip().replace('\r', '').replace('\n', ' ')

def embed(value: str):
    encoded_input = tokenizer(value, return_tensors='pt')
    output = model(**encoded_input)
    res = output.last_hidden_state.squeeze(0)[-1].detach().numpy().reshape(1, -1)

    res = res / np.linalg.norm(res)
    return res

df['lyrics'] = df['lyrics'].apply(get_sub_lyrics)

vectorized_lyrics = []
for text in df['lyrics'].values:
    vectorized_lyrics.append(embed(text))


# create annoy index for faster search
annoy_index = AnnoyIndex(EMBEDDING_DIMENSION, 'euclidean')
for i, vectorized_lyric in enumerate(vectorized_lyrics):
    annoy_index.add_item(i, vectorized_lyric)
annoy_index.build(10)
annoy_index = AnnoyIndex(embedding_dimension, 'dot')
for i, vector in enumerate(vectorized_lyrics):
    vector = vector.squeeze()
    vector = vector / np.linalg.norm(vector)
    annoy_index.add_item(i, vector)
annoy_index.build(20)

def lyrics_pre_process(lyrics: str):
    return lyrics.split('\n')[0].replace('\r', '')

def find_nearest_song_annoy(emojis, n=1):
    """
    args:
        emojis : string of lyrics or emojis
    return:
        list of first n songs with closest embeddings to the input
    """
    idx = annoy_index.get_nns_by_vector(embed(emojis).reshape(-1,1), n)
    return list(df[song_col].iloc[idx])