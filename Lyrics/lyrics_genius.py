import lyricsgenius
import string
import pandas as pd
from decouple import config

# generate an api key and paste it
# https://genius.com/api-clients
token = config('LYRICS_GENIUS_KEY')
genius = lyricsgenius.Genius(token)

def generate_lyrics(user_artist):
    # Use api to get top 5 songs from an artist
    artist_songs = genius.search_artist(user_artist, max_songs=5)

    # Convert artist songs object to dictionary
    artist_lyrics = {}
    for song in artist_songs.songs:
        artist_lyrics[song.title] = song.lyrics

    # Clean each lyric in the artist dictionary
    for song in artist_lyrics.keys():
        old_lyrics = artist_lyrics[song]
        new_lyrics = clean_lyrics(old_lyrics)
        artist_lyrics[song] = new_lyrics

    # Convert to pandas df
    df = pd.DataFrame.from_dict(artist_lyrics, orient='index', columns=['lyrics']).rename_axis('song').reset_index()

    # Save df to csv
    file_name = user_artist.lower().replace(' ', '_')
    df.to_csv(f'Lyrics/{file_name}.csv', index=False)

def clean_lyrics(raw_lyrics):
    # Change to lowercase
    clean_lyrics = raw_lyrics.lower()

    # Clean lyrics by removing head and verse/chorus info
    clean_lyrics = clean_lyrics.replace(clean_lyrics[:clean_lyrics.find('[')], '')

    cleaned = False
    while not cleaned:
        start = clean_lyrics.find('[')
        end = clean_lyrics.find(']')
        if start != -1 and end != -1:
            clean_lyrics = clean_lyrics.replace(clean_lyrics[start:end + 1], '')
        else:
            cleaned = True
        
    # Clean lyrics by removing puncuation, spaces, and new lines
    # clean_lyrics = clean_lyrics.replace('\n', ' ').replace('  ', ' ').replace('’', '').translate(str.maketrans('', '', string.punctuation)).strip()
    clean_lyrics = clean_lyrics.translate(str.maketrans('', '', string.punctuation)).strip().replace('’', '')

    # Remove 'embed' and numbers
    embed = clean_lyrics.find('embed')
    if embed != -1:
        clean_lyrics = clean_lyrics[:embed]

    end_number = True
    while end_number:
        if clean_lyrics[-1] not in string.ascii_lowercase:
            clean_lyrics = clean_lyrics[:-1]
        else:
            end_number = False

    # Remove recommendation
    recommendation = clean_lyrics.find('you might also like')
    if recommendation != -1:
        clean_lyrics = clean_lyrics.replace(clean_lyrics[recommendation:recommendation + 20], '')

    return clean_lyrics

if __name__ == '__main__':
    user_artists = ['Ed Sheeran',
                    'Linkin Park',
                    'Bring Me the Horizon',
                    'Adele',
                    'Palisades']
    
    for artist in user_artists:
        try:
            generate_lyrics(artist)
        except:
            print('Artist lyrics could not be imported.')