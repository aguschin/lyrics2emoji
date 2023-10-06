import spotify
import text_to_emoji
import rich

lyrics = spotify.get_lyric_of_top_song('spotify:playlist:37i9dQZF1E4AfEUiirXPyP', limit=5, one_line=False, title=True)
rich.print(lyrics)

#emoji to text for each line of lyrics input as text 
#split each line at comma and then translate each to emoji
#join back together with comma

for line in lyrics:
    line = line.split(',')
    for word in line:
        print(text_to_emoji.translate_text(word))
    print(','.join(line))
    print('\n')
    