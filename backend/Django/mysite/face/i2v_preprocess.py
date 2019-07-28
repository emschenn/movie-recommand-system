import sys
# from movie_link import movieId_link
import pandas as pd
import numpy as np
import ast
import math
import csv
from collections import defaultdict


movie = pd.read_csv("../../../movie_data/MovieLens/ml-latest-small/movies.csv",sep=",")
m_dict = dict()
title_dict = dict()

user =  pd.read_csv("../../../movie_data/MovieLens/ml-latest-small/ratings.csv",sep=",")
user_dict = defaultdict(list)

df = pd.read_csv("mycsvfile.csv",sep=",")
imdb_id = pd.read_csv("../../../movie_data/MovieLens/ml-latest-small/links.csv",sep=",")
df['movieId'] = df['movieId'].map(ast.literal_eval)
movie_dict = df.set_index('topic').T.to_dict('list')


def movieId_link(id):
    topic = imdb_id.loc[imdb_id['movieId'] == id]

    # print('idididdididi', topic['tmdbId'].values)
    if(topic['tmdbId'].values != None):
        if(math.isnan(float(''.join(str(i) for i in topic['tmdbId'].values))) == False):
            return int(float(''.join(str(i) for i in topic['tmdbId'].values)))

def name_to_id():
    for index, i in movie.iterrows():
        #print(i)
        id = movie.loc[index, 'movieId']
        tmdb = movieId_link(id)
        # print(id)
        title = movie.loc[index, 'title']
        # print(title)
        if(tmdb != math.nan):
            # m_dict[title] = tmdb
            title_dict[tmdb] = title
   
    #建檔
    # with open('name_to_id.csv', 'w', encoding = 'utf8', newline='') as f:  # Just use 'w' mode in 3.x
    #     w = csv.writer(f)
    #     for key, val in m_dict.items():
    #         w.writerow([key, val])
    # 建檔
    # with open('id_to_name.csv', 'w', encoding = 'utf8', newline='') as f:  # Just use 'w' mode in 3.x
    #     w = csv.writer(f)
    #     for key, val in title_dict.items():
    #         w.writerow([key, val])

def user_set():
    length = 0
    for index, i in user.iterrows():
        id = user.loc[index, 'userId']
        # print(id)
        mId = user.loc[index, 'movieId']
        tmdb = movieId_link(mId)
        # print(title)
        if(tmdb != math.nan):
            user_dict[id].append(title_dict[tmdb])
            length += 1
    
    user_dict['<unk>'].append(length)
    # with open('usre_set.csv', 'w', encoding = 'utf8', newline='') as f:  # Just use 'w' mode in 3.x
    #     w = csv.writer(f)
    #     for key, val in user_dict.items():
    #         w.writerow([key, val])
    with open('user_set_movie_name.csv', 'w', encoding = 'utf8', newline='') as f:  # Just use 'w' mode in 3.x
        w = csv.writer(f)
        for key, val in user_dict.items():
            w.writerow([key, val])

def shuffle(reader, buf_size):
    """
    Creates a data reader whose data output is shuffled.

    Output from the iterator that created by original reader will be
    buffered into shuffle buffer, and then shuffled. The size of shuffle buffer
    is determined by argument buf_size.

    :param reader: the original reader whose output will be shuffled.
    :type reader: callable
    :param buf_size: shuffle buffer size.
    :type buf_size: int

    :return: the new reader whose output is shuffled.
    :rtype: callable
    """
    import random
    def data_reader():
        buf = []
        for e in reader():
            buf.append(e)
            if len(buf) >= buf_size:
                random.shuffle(buf)
                for b in buf:
                    yield b
                buf = []

        if len(buf) > 0:
            random.shuffle(buf)
            for b in buf:
                yield b

    return data_reader

if __name__ == '__main__':
    name_to_id()
    user_set()