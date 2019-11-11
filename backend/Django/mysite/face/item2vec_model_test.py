# i2v model structure and training process
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


os.environ["CUDA_VISIBLE_DEVICES"] = '0' #use GPU with ID=0
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.7 # maximun alloc gpu50% of MEM
config.gpu_options.allow_growth = True #allocate dynamically
# sess = tf.Session(config = config)
K.set_session(tf.Session(config=config))


# def maybe_download(filename, url, expected_bytes):
#     """Download a file if not present, and make sure it's the right size."""
#     if not os.path.exists(filename):
#         filename, _ = urllib.request.urlretrieve(url + filename, filename)
#     statinfo = os.stat(filename)
#     if statinfo.st_size == expected_bytes:
#         print('Found and verified', filename)
#     else:
#         print(statinfo.st_size)
#         raise Exception(
#             'Failed to verify ' + filename + '. Can you get to it with a browser?')
#     return filename


# # Read the data into a list of strings.
# def read_data(filename):
#     """Extract the first file enclosed in a zip file as a list of words."""
#     with zipfile.ZipFile(filename) as f:
#         data = tf.compat.as_str(f.read(f.namelist()[0])).split()
#     return data


# def build_dataset(words, n_words):
#     """Process raw inputs into a dataset."""
#     count = [['UNK', -1]]
#     count.extend(collections.Counter(words).most_common(n_words - 1))
#     dictionary = dict()
#     for word, _ in count:
#         dictionary[word] = len(dictionary)
#     data = list()
#     unk_count = 0
#     for word in words:
#         if word in dictionary:
#             index = dictionary[word]
#         else:
#             index = 0  # dictionary['UNK']
#             unk_count += 1
#         data.append(index)
#     count[0][1] = unk_count
#     reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
#     return data, count, dictionary, reversed_dictionary

# def collect_data(vocabulary_size=10000):
#     url = 'http://mattmahoney.net/dc/'
#     filename = maybe_download('text8.zip', url, 31344016)
#     vocabulary = read_data(filename)
#     # print(vocabulary[:20])
#     print(len(vocabulary))
#     data, count, dictionary, reverse_dictionary = build_dataset(vocabulary,
#                                                                 vocabulary_size)
#     del vocabulary  # Hint to reduce memory.
#     return data, count, dictionary, reverse_dictionary

# vocab_size = 10000
# data, count, dictionary, reverse_dictionary = collect_data(vocabulary_size=vocab_size)
# # print(data[:20])
# print(data[1:])

file = open('item_idx_dict.pickle', 'rb')
item_idx_dict =pickle.load(file)
file.close()
reverse_dictionary = dict(zip(item_idx_dict.values(), item_idx_dict.keys()))
file = open('id_to_name.pickle', 'rb')
idx_name_dict =pickle.load(file)
file.close()

imdb_id = pd.read_csv("../../../movie_data/MovieLens/ml-latest-small/links.csv",sep=",")
def movieId_link(id):
  
    topic = imdb_id.loc[imdb_id['movieId'] == id]
    # print('idididdididi', topic['tmdbId'].values)
    if(topic['tmdbId'].values != None):
        return int(float(''.join(str(i) for i in topic['tmdbId'].values)))

# print(item_idx_dict.values())
vocab = list(item_idx_dict.values())
# print(vocab)
vocab_size = 9725

window_size = 3
vector_dim = 300
epochs = 200000

valid_size = 16     # Random set of words to evaluate similarity on.
valid_window = 100  # Only pick dev samples in the head of the distribution.
valid_examples = np.random.choice(valid_window, valid_size, replace=False)

# sampling_table = sequence.make_sampling_table(vocab_size)
# couples, labels = skipgrams(vocab, vocab_size, window_size=window_size, sampling_table=sampling_table)
f=open('positive_train.pickle', 'rb')
f2=open('negative_train.pickle', 'rb')
positive_list = []
negative_list = []
while 1:
    try:
        positive_list.append(pickle.load(f))
    except EOFError:
        break
f.close()
while 1:
    try:
        negative_list.append(pickle.load(f2))
    except EOFError:
        break
f2.close()

train = positive_list
train.extend(negative_list)
couples, labels = zip(*train)
# print(couples)
word_target, word_context = zip(*couples)
word_target = np.array(word_target, dtype="int32")
word_context = np.array(word_context, dtype="int32")

print(couples[:10], labels[:10])

# create some input variables
input_target = Input((1,))
input_context = Input((1,))

embedding = Embedding(vocab_size, vector_dim, input_length=1, name='embedding')
target = embedding(input_target)
target = Reshape((vector_dim, 1))(target)
context = embedding(input_context)
context = Reshape((vector_dim, 1))(context)

# setup a cosine similarity operation which will be output in a secondary model
# similarity = merge([target, context], mode='cos', dot_axes=0)
similarity = Dot(axes=1,normalize=True)([target,context])

# now perform the dot product operation to get a similarity measure
# dot_product = merge([target, context], mode='dot', dot_axes=1)
dot_product = dot([target, context], axes=1, normalize=False)
dot_product = Reshape((1,))(dot_product)
# add the sigmoid output layer
output = Dense(1, activation='sigmoid')(dot_product)
# create the primary training model
model = Model(input=[input_target, input_context], output=output)
model.compile(loss='binary_crossentropy', optimizer='rmsprop',  metrics=['accuracy'])

# create a secondary validation model to run our similarity checks during training
validation_model = Model(input=[input_target, input_context], output=similarity)


class SimilarityCallback:
    def run_sim(self):
        for i in range(valid_size):
            valid_word = reverse_dictionary[valid_examples[i]]
            top_k = 8  # number of nearest neighbors
            sim = self._get_sim(valid_examples[i])
            nearest = (-sim).argsort()[1:top_k + 1]
            log_str = 'Nearest to %s:' % idx_name_dict.get(movieId_link(valid_word))
            for k in range(top_k):
                close_word = idx_name_dict.get(movieId_link(reverse_dictionary[nearest[k]]))
                log_str = '%s %s,' % (log_str, close_word)
            print(log_str)

    @staticmethod
    def _get_sim(valid_word_idx):
        sim = np.zeros((vocab_size,))
        in_arr1 = np.zeros((1,))
        in_arr2 = np.zeros((1,))
        in_arr1[0,] = valid_word_idx
        for i in range(vocab_size):
            in_arr2[0,] = i
            out = validation_model.predict_on_batch([in_arr1, in_arr2])
            sim[i] = out
        return sim
sim_cb = SimilarityCallback()

# train by fit
# model.fit(x=[list(word_target), list(word_context)], y=list(labels), epochs=10, batch_size=32)

# train by train_on_banch 
# arr_1 = np.zeros((1,))
# arr_2 = np.zeros((1,))
# arr_3 = np.zeros((1,))
# for cnt in range(epochs):
#     idx = np.random.randint(0, len(labels)-1)
#     arr_1[0,] = word_target[idx]
#     arr_2[0,] = word_context[idx]
#     arr_3[0,] = labels[idx]
#     loss = model.train_on_batch([arr_1, arr_2], arr_3)
#     if cnt % 100 == 0:
#         print("Iteration {}, loss={}".format(cnt, loss))
#     if cnt % 10000 == 0:
#         sim_cb.run_sim()
#         # print('cut')

# print('model train done')
# model.save("i2v_model_train_fit.h5")
# validation_model.save("i2v_model_test_fit.h5")
# with open('keras_skipgram_train_fit', 'w') as fwrite:
#     for idx, vec in enumerate(model.layers[2].get_weights()[0].tolist()):
#         fwrite.write('%d %s\n' % (idx, ' '.join([str(_) for _ in vec])))

validation_model = keras.models.load_model('i2v_model_test.h5')
model = keras.models.load_model('i2v_model_train.h5')
# # print(model.summary())
# weights = model.layers[2].get_weights()[0].tolist()
# print(weights[0])
# weights2 = validation_model.layers[2].get_weights()[0].tolist()
# print(weights2[0])
# print(operator.eq(weights, weights2))

def run_sim(valid_examples):
    # for i in range(valid_size):
    valid_word = reverse_dictionary[valid_examples]
    top_k = 8  # number of nearest neighbors
    sim = _get_sim(valid_examples)
    nearest = (-sim).argsort()[1:top_k + 1]
    # log_str = 'Nearest to %s:' % idx_name_dict.get(movieId_link(valid_word))
    # for k in range(top_k):
    #     close_word = idx_name_dict.get(movieId_link(reverse_dictionary[nearest[k]]))
    #     log_str = '%s %s,' % (log_str, close_word)
    # print(log_str)
    return nearest

def _get_sim(valid_word_idx):
    sim = np.zeros((vocab_size,))
    in_arr1 = np.zeros((1,))
    in_arr2 = np.zeros((1,))
    in_arr1[0,] = valid_word_idx
    for i in range(vocab_size):
        in_arr2[0,] = i
        out = validation_model.predict_on_batch([in_arr1, in_arr2])
        sim[i] = out
    print(sim)
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

    test = positive_test_list
    test.extend(negative_test_list)
    couples_test, labels_test = zip(*test)
    word_target_test, word_context_test = zip(*couples_test)
    loss = model.evaluate(x=[list(word_target_test), list(word_context_test)], y=list(labels_test), batch_size=32)
    print(loss)
    # print([list(word_target_test), list(word_context_test)])
    y = model.predict([list(word_target_test), list(word_context_test)])

    # ===============================================
    # 估算
    for id in range(len(y)):
        if y[id] < 0.5:
            y[id] = 0
        else:
            y[id] = 1
    # print(y)
    count = 0
    total = len(list(labels_test))
    for id in range(len(y)):
        if y[id] == list(labels_test)[id]:
            count += 1
    print(count/total)
    # ==================================================



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

    