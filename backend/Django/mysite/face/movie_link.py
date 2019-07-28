import pandas as pd
import numpy as np
import ast
import sys


df = pd.read_csv("face/mycsvfile.csv",sep=",")
imdb_id = pd.read_csv("../../movie_data/MovieLens/ml-latest-small/links.csv",sep=",")

df['movieId'] = df['movieId'].map(ast.literal_eval)
movie_dict = df.set_index('topic').T.to_dict('list')

    #ttt = list((movie_dict.get('Comedy')[0]))

topic = imdb_id.loc[imdb_id['movieId'] == 1]

i = float(''.join(str(i) for i in topic['tmdbId'].values))



def movieId_link(id):
    df = pd.read_csv("face/mycsvfile.csv",sep=",")
    imdb_id = pd.read_csv("../../movie_data/MovieLens/ml-latest-small/links.csv",sep=",")

    df['movieId'] = df['movieId'].map(ast.literal_eval)
    movie_dict = df.set_index('topic').T.to_dict('list')

    #ttt = list((movie_dict.get('Comedy')[0]))

    topic = imdb_id.loc[imdb_id['movieId'] == id]

    print('idididdididi', topic['tmdbId'].values)
    if(topic['tmdbId'].values != None):
        return int(float(''.join(str(i) for i in topic['tmdbId'].values)))
