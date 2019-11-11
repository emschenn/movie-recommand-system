# i2v 呼叫和執行
from keras.models import Model
from keras.layers import Input, Dense, Reshape, merge, Dot, dot
from keras.layers.embeddings import Embedding
from keras.preprocessing.sequence import skipgrams
from keras.preprocessing import sequence

import keras
import urllib.request
import collections
import os
import zipfile

import numpy as np
import tensorflow as tf

from keras import backend as K

import pickle
import pandas as pd
 
import os  
import operator
import random

graph = tf.get_default_graph()


vocab_size = 9725
validation_model = keras.models.load_model('face/Item2vec_data/i2v_model_test.h5')
model = keras.models.load_model('face/Item2vec_data/i2v_model_train.h5')

# file = open('face/idx_item_dict.pickle', 'rb')
file = open('face/util_data/idx_item_dict.pickle', 'rb')
idx_item_dict =pickle.load(file)
file.close()
file = open('face/util_data/item_idx_dict.pickle', 'rb')
item_idx_dict =pickle.load(file)
file.close()
reverse_dictionary = dict(zip(item_idx_dict.values(), item_idx_dict.keys()))
file = open('face/util_data/id_to_name.pickle', 'rb')
idx_name_dict =pickle.load(file)
file.close()

imdb_id = pd.read_csv("../../movie_data/MovieLens/ml-latest-small/links.csv",sep=",")
def movieId_link(id):
  
    topic = imdb_id.loc[imdb_id['movieId'] == id]
    # print('idididdididi', topic['tmdbId'].values)
    if(topic['tmdbId'].values != None):
        return int(float(''.join(str(i) for i in topic['tmdbId'].values)))
def movieId_link_tmdb_to_id(id):
    topic = imdb_id.loc[imdb_id['tmdbId'] == id]
    # print('idididdididi', topic['tmdbId'].values)
    if(topic['movieId'].values != None):
        return int(float(''.join(str(i) for i in topic['movieId'].values)))

def run_sim(valid_examples):
    valid_examples = movieId_link_tmdb_to_id(valid_examples[0])
    if valid_examples == None or valid_examples > vocab_size:
        print(valid_examples)
        valid_examples = random.randint(0, vocab_size)
    else:
        valid_examples = valid_examples - 1

    print(valid_examples)
    similarity = []
    valid_word = reverse_dictionary[valid_examples]
    top_k = 10  # number of nearest neighbors
    sim = _get_sim(valid_examples)
    nearest = (-sim).argsort()[1:top_k + 1]
    similarity.append(list(map(lambda x: movieId_link(idx_item_dict.get(x)), nearest)))
    # log_str = 'Nearest to %s:' % idx_name_dict.get(movieId_link(valid_word))
    # print(log_str)
    return similarity[0]

def _get_sim(valid_word_idx):
    sim = np.zeros((vocab_size,))
    in_arr1 = np.zeros((1,))
    in_arr2 = np.zeros((1,))
    in_arr1[0,] = valid_word_idx
    print(in_arr1)
    with graph.as_default():
        for i in range(vocab_size):
            in_arr2[0,] = i
            out = model.predict_on_batch([in_arr1, in_arr2])
            sim[i] = out
    # print(sim)
    return sim


if __name__ == '__main__':
    f_test=open('positive_test2.pickle', 'rb')
    f2_test=open('negative_test2.pickle', 'rb')
    positive_test_list = []
    negative_test_list = []
    while 1:
        try:
            positive_test_list.append(pickle.load(f_test))
        except EOFError:
            break
    f_test.close()
    while 1:
        try:
            negative_test_list.append(pickle.load(f2_test))
        except EOFError:
            break
    f2_test.close()

    i = run_sim(862)
    print(i)

    # test = positive_test_list
    # test.extend(negative_test_list)
    # couples_test, labels_test = zip(*test)
    # word_target_test, word_context_test = zip(*couples_test)
    # # loss = model.evaluate(x=[list(word_target_test), list(word_context_test)], y=list(labels_test), batch_size=32)
    # # print(loss)
    # # print([list(word_target_test), list(word_context_test)])
    # y = model.predict_on_batch([list(word_target_test), list(word_context_test)])

    # # ===============================================
    # # 估算
    # for id in range(len(y)):
    #     if y[id] < 0.5:
    #         y[id] = 0
    #     else:
    #         y[id] = 1
    # # print(y)
    # count = 0
    # total = len(list(labels_test))
    # for id in range(len(y)):
    #     if y[id] == list(labels_test)[id]:
    #         count += 1
    # print(count/total)
    # # ==================================================

    # test = collections.defaultdict(list)
    # for pair, label in positive_test_list:
    #     if pair[1] in test[pair[0]]:
    #         pass
    #     else:
    #         test[pair[0]].append(pair[1])
    # count = 0
    # total = 0
    # index = list(test.keys())
    # for idx in index:
    #     # print(idx)
    #     i = run_sim(idx)
    #     total += len(i)
    #     # print(test[idx])
    #     print('title', idx_name_dict.get(movieId_link(reverse_dictionary[idx])))
    #     # print(i)
    #     for tmp in i:
    #         if tmp in test[idx]:
    #             print(idx_name_dict.get(movieId_link(reverse_dictionary[tmp])))
    #             count += 1
    #     print('count', count)
    #     print('total', total)
    #     print(count/total)
    #     print('==========')