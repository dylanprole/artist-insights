import pandas as pd
import numpy as np
import string

def get_artist_songs(artist_name):
    artist_name = '-'.join(artist_name.lower().split(' '))
    artist_df = pd.read_csv(f'Lyrics/{artist_name}.csv')
    return artist_df.to_numpy()

def create_frequency_list(artist_np):
    word_frequency = {}
    for song in artist_np:
        try:
            words = song[2].split(' ')
            for word in words:
                if not word_frequency.get(word, False):
                    word_frequency[word] = 1
                else:
                    word_frequency[word] += 1
        except:
            print('Could not split...skipping...')

    word_frequency_df = pd.DataFrame.from_dict(word_frequency, orient='index',
                       columns=['freq'])  
    word_frequency_df = word_frequency_df.sort_values(by=['freq'], 
                                                      ascending=False)      
    return word_frequency_df



ed = get_artist_songs('ed sheeran')
ed_freq = create_frequency_list(ed)
print(ed_freq.head(10))