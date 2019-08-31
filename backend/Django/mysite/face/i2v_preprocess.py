import sys
# from movie_link import movieId_link
import pandas as pd
import numpy as np
import ast
import math
import csv
import random
from collections import defaultdict
import pickle


movie_dict = pd.read_csv("user_rating_last.csv",sep=",")
movie_dict['rating'] = movie_dict['rating'].map(ast.literal_eval)
movie_dict = movie_dict.set_index('userId').T.to_dict('list')

file = open('item_idx_dict.pickle', 'rb')
item_idx_dict =pickle.load(file)
file.close()
file = open('idx_item_dict.pickle', 'rb')
idx_item_dict =pickle.load(file)
file.close()
# print(item_idx_dict)
# print(idx_item_dict)

file = open('positive_train2.pickle', 'ab')
file2 = open('negative_train2.pickle', 'ab')
file_test = open('positive_test2.pickle', 'ab')
file2_test = open('negative_test2.pickle', 'ab')

imdb_id = pd.read_csv("../../../movie_data/MovieLens/ml-latest-small/links.csv",sep=",")
def movieId_link(id):
  
    topic = imdb_id.loc[imdb_id['tmdbId'] == id]
    print(id)
    print('idididdididi', topic['movieId'].values)
    print('idididdididi', topic['movieId'].values[0])
    if(topic['movieId'].values[0] != None):
        return topic['movieId'].values[0]


if __name__ == '__main__':
    vocabulary_size = len(item_idx_dict)
    # print(vocabulary_size)
    for i in range(len(movie_dict)):
        old_user = movie_dict[i + 1][0]
        # print(old_user_1)
        # old_rating = list()
        # if i == 0:
        #     print(old_user)
        user_dict = []
        for movieId, rating in old_user.items():
            if movieId != None:
                print(movieId, item_idx_dict.get(movieId_link(movieId)))
                user_dict.append(item_idx_dict.get(movieId_link(movieId), item_idx_dict['unk']))
        # if i == 0:
        #     print(user_dict)
        for k in range(len(user_dict)):
            target = user_dict[k]
            # generate positive sample
            context_list = []
            negative_list = []
            j = k - 2
            while j <= k + 2 and j < len(user_dict) -3:
                if j >= 0 and j != k:
                    context_list.append(user_dict[j])
                j += 1
            for con in context_list:
                pickle.dump(((target, con), 1), file)
            # if i == 0:
            #     for con in context_list:
            #         print((target, con), 1)
            # generate negative sample
            for _ in range(len(context_list)):
                ne_idx = random.randrange(0, vocabulary_size)
                while ne_idx in context_list:
                    ne_idx = random.randrange(0, vocabulary_size)
                negative_list.append(ne_idx)
            for con in negative_list:
                pickle.dump(((target, con), 0), file2)
            
            # train
            # ==========================================
            # test
            context_list = []
            negative_list = []

            while j <= k + 2 and j < len(user_dict):
                if j >= 0 and j != k:
                    context_list.append(user_dict[j])
                j += 1
            for con in context_list:
                pickle.dump(((target, con), 1), file_test)
            # if i == 0:
            #     for con in context_list:
            #         print((target, con), 1)
            # generate negative sample
            for _ in range(len(context_list)):
                ne_idx = random.randrange(0, vocabulary_size)
                while ne_idx in context_list:
                    ne_idx = random.randrange(0, vocabulary_size)
                negative_list.append(ne_idx)
            for con in negative_list:
                pickle.dump(((target, con), 0), file2_test)
            # if i == 0:
            #     for con in negative_list:
            #         print((target, con), 0)
        # print(i, '===============')
    
    # print(user_dict)