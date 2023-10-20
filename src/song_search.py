import numpy as np
import pandas as pd
from annoy import AnnoyIndex
from preprocess import embed, EMBEDDING_DIMENSION
import spacy
from spacymoji import Emoji


# lyrics source and column of song name
df = pd.read_json("../data/sample_data/top_300_spotify_with_embeddings.json")
song_col = "song_name"
vectorized_lyrics = df["lyrics_embedding"].values

# create annoy index for faster search
annoy_index = AnnoyIndex(EMBEDDING_DIMENSION, "dot")
for i, vector in enumerate(vectorized_lyrics):
    annoy_index.add_item(i, vector)
annoy_index.build(10)


def find_nearest_song_annoy(emojis, n=1):
    """
    args:
        emojis : string of lyrics or emojis
    return:
        index of first n songs with closest embeddings to the input
    """
    idx = annoy_index.get_nns_by_vector(emojis, n)
    return idx


def index_post_process(df, input_emojis, idx, len_diff_threshold=2):
    new_idx = []
    nlp = spacy.load("en_core_web_sm")
    emoji = Emoji(nlp)
    nlp.add_pipe("emoji", first=True)

    # list of input_emojis by line: ['\u1566\u8112', '\u4781']
    emojis = input_emojis.split("\n")

    # get count of emojis in each line
    count_emojis = []
    for em in emojis:
        count = 0
        for token in nlp(em):
            if token._.is_emoji:
                count += 1
        count_emojis.append(count)
    print("emoji count", count_emojis)

    for id in idx:
        lyrics = clean_text(df["lyrics"].iloc[id]).split("\n")
        count_words = list(map(lambda x: len(x.split()), lyrics))
        if all(
            list(
                map(
                    lambda x: abs(x[0] - x[1]) <= len_diff_threshold,
                    zip(count_words, count_emojis),
                )
            )
        ):
            new_idx.append(id)

    return new_idx


def clean_text(lyric):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(lyric)
    pos_tags = ["AUX", "INTJ", "PROPN", "PUNCT", "SCONJ", "SYM", "X"]
    words = [token.text for token in doc if token.pos_ not in pos_tags]  # filter words
    lyric = " ".join(words).split("\n")  # make full string
    lyric = [i.strip() for i in lyric if len(i) > 15]  # clear small lines
    lyric = "\n".join(lyric).split("\n")[:4]  # get the first 4 lines only
    lyric = "\n".join(lyric)  # completed string
    return lyric


if __name__ == "__main__":

    df = pd.read_json("../data/sample_data/top_300_spotify_with_embeddings.json")
    emojis_emb = df["translated_lyrics_embedding"].values

    matched = []
    # use first 10 emojis to search with annoy
    for i in range(10):
        input_emoji = emojis_emb[i]
        guess = find_nearest_song_annoy(input_emoji, 10000)
        new_index = index_post_process(df, df.iloc[i]["translated_lyrics"], guess, 4)

        print("------------------------------")
        print(
            "word count ",
            list(
                map(
                    lambda x: len(x.replace("\r", "").split()),
                    df["lyrics"][i].split("\n")[0:4],
                )
            ),
        )
        print("init annoy position:", guess.index(i))
        if i in new_index:
            print("post annoy position:", new_index.index(i))
        else:
            print("post annoy position: FAIL")
        print("actual data:")
        print(df["translated_lyrics"][i])
        print(" \n".join(df["lyrics"][i].split("\n")[0:4]).replace("\r", ""))
