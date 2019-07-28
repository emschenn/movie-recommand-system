import sys
import keras
from keras.models import Sequential, Model
from keras.layers import Activation, merge, Reshape
from keras.layers import Input, Embedding, Dense, dot
from keras.layers.core import Lambda
from keras import optimizers
from keras import backend as K
import random
import pandas as pd
import numpy as np
from i2v_preprocess import shuffle

name_id_dict = pd.read_csv('user_set_movie_name.csv', encoding='unicode_escape')

def skipgram_model(vocab_size, embedding_dim=100, paradigm='Sequential'):
    # Sequential paradigm
    if paradigm == 'Sequential':
        target = Sequential()
        target.add(Embedding(vocab_size, embedding_dim, input_length=1))
        context = Sequential()
        context.add(Embedding(vocab_size, embedding_dim, input_length=1))

        # merge the pivot and context models
        model = Sequential()
        model.add(Merge([target, context], mode='dot'))
        model.add(Reshape((1,), input_shape=(1,1)))
        model.add(Activation('sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy')
        return model

def skipgram_reader_generator(movie_dict,  context_window=2):
    def reader():
        vocabulary_size = len(movie_dict)
        tmp = name_id_dict
        for key, values in tmp.items():
            line_list = values
            movie_ids = [movie_dict.get(_, movie_dict['<unk>']) for _ in line_list]
            for i in range(len(movie_ids)):
                target = movie_ids[i]
                # generate positive sample
                context_list = []
                j = i - context_window
                while j <= i + context_window and j < len(movie_ids):
                    if j >= 0 and j != i:
                        context_list.append(movie_ids[j])
                        yield ((target, movie_ids[j]), 1)
                    j += 1
                # generate negative sample
                for _ in range(len(context_list)):
                    ne_idx = random.randrange(0, vocabulary_size)
                    while ne_idx in context_list:
                        ne_idx = random.randrange(0, vocabulary_size)
                    yield ((target, ne_idx), 0)
    return reader

if __name__ == '__main__':
    # network conf
    paradigm = 'Functional'
    min_word_freq = 10

    word_dict = name_id_dict
    dict_size = len(word_dict)
    emb_size = 100
    context_window_size = 2
    epochs = 50
    batch_size = 256
    print(word_dict)

    model = skipgram_model(dict_size, emb_size, paradigm)
    # print (model.layers)
    for epoch_id in range(epochs):
        # train by batch
        batch_id = 0
        x_batch = [[],[]]
        y_batch = []
        loss_list = []
        for movie_ids, label in shuffle(skipgram_reader_generator(word_dict, context_window=context_window_size), 10000)():
            batch_id += 1
            x_batch[0].append(movie_ids[0])
            x_batch[1].append(movie_ids[1])
            y_batch.append(label)
            if batch_id % (batch_size*1000) == 0:
                # Print evaluate log
                # logger.info('[epoch #%d] batch #%d, train loss:%s' % (epoch_id, batch_id, np.mean(loss_list)))
                loss_list = []
            if batch_id % batch_size == 0:
                X = [np.array(x_batch[0]), np.array(x_batch[1])]
                loss = model.train_on_batch(X, np.array(y_batch))
                loss_list.append(loss)
                x_batch = [[],[]]
                y_batch = []
    # logger.info('model train done')
    # store word embedding
    # with open('./models/keras_0804_09_skipgram', 'w') as fwrite:
    #     for idx, vec in enumerate(model.layers[2].get_weights()[0].tolist()):
    #         fwrite.write('%d %s\n' % (idx, ' '.join([str(_) for _ in vec])))
