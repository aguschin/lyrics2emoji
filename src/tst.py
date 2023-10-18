import text_to_emoji
i = input('')
def texttoemoji(i):
    return text_to_emoji.translate_text(i)

#convert to unicode

print(texttoemoji(i).encode('unicode-escape').decode('utf-8'))