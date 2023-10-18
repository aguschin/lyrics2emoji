import spacy

nlp = spacy.load("en_core_web_sm")


def clean_text(lyric):
    doc = nlp(lyric)
    pos_tags = ['AUX', 'INTJ', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'X']
    words = [token.text for token in doc if token.pos_ not in pos_tags]  # filter words
    lyric = ' '.join(words).split('\n')  # make full string
    lyric = [i.strip() for i in lyric if len(i) > 15]  # clear small lines
    lyric = '\n'.join(lyric).split('\n')[:4]  # get the first 4 lines only
    lyric = '\n'.join(lyric)  # completed string

    return lyric
