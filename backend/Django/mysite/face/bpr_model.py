import pandas as pd
import csv
import ast
import numpy as np
import keras
import tensorflow as tf
from keras import Model
from keras import metrics
from keras.models import Sequential
from keras.layers import *
import math
import random
import implicit
from sklearn.metrics import roc_auc_score
import json

user = np.loadtxt("../../../movie_data/MovieLens/ml-latest-small/ratings.csv.user_embedding")
item = np.loadtxt("../../../movie_data/MovieLens/ml-latest-small/ratings.csv.item_embedding")
user_embedding = np.delete(user, 0, 1)
item_embedding = np.delete(item, 0, 1)
item_idx = item[:,0].tolist()
item_idx = [int(i) for i in item_idx]
print(item_idx)
# print(user_embedding)
print(user_embedding.shape)
print(item_embedding.shape)
predict = np.mat(user_embedding) * np.mat(item_embedding.T)
# print(predict)
p = predict.tolist()
# print(len(p[0]))
for j in range(10):
    tmp = p[j]
    top = list()
    tmp2 = sorted(range(len(tmp)), key=lambda i: tmp[i])[-5:]
    print(tmp2)
    for t in tmp2:
        top.append(t)
    top.reverse()
    print(top)
    for i in top:
        print(item_idx[i-1])
    print("==================")

# user_count = 610
# item_count = 193609
# user_rating_matrix = pd.read_csv("user_rating_last.csv",sep=",")
# user_rating_matrix['rating'] = user_rating_matrix['rating'].map(ast.literal_eval)
# user_ratings = user_rating_matrix.set_index('userId').T.to_dict('list')

# def generate_test(user_ratings):
#     '''
#     for each user, random select one of his(her) rating into test set
#     '''
#     user_test = dict()
#     for u, i_list in user_ratings.items():
#         tmp = i_list[0]
#         # print(type(tmp))
#         user_test[u] = random.choice(list(tmp.keys()))
#     return user_test


# def generate_train_batch(user_ratings, user_ratings_test, item_count, batch_size=512):
#     '''
#     uniform sampling (user, item_rated, item_not_rated)
#     '''
#     t = []
#     for b in range(batch_size):
#         u = random.sample(user_ratings.keys(), 1)[0]
#         i = random.sample(user_ratings[u], 1)[0]
#         while i == user_ratings_test[u]:
#             i = random.sample(user_ratings[u], 1)[0]
        
#         j = random.randint(1, item_count)
#         while j in user_ratings[u]:
#             j = random.randint(1, item_count)
#         t.append([u, i, j])
#     return np.asarray(t)

# def generate_test_batch(user_ratings, user_ratings_test, item_count):
#     '''
#     for an user u and an item i rated by u, 
#     generate pairs (u,i,j) for all item j which u has't rated
#     it's convinent for computing AUC score for u
#     '''
#     for u in user_ratings.keys():
#         t = []
#         i = user_ratings_test[u]
#         for j in range(1, item_count+1):
#             if not (j in user_ratings[u]):
#                 t.append([u, i, j])
#         yield np.asarray(t)

# def bpr_mf(user_count, item_count, hidden_dim):
#     u = tf.placeholder(tf.int32, [None])
#     i = tf.placeholder(tf.int32, [None])
#     j = tf.placeholder(tf.int32, [None])

#     with tf.device("/cpu:0"):
#         user_emb_w = tf.get_variable("user_emb_w", [user_count+1, hidden_dim], 
#                             initializer=tf.random_normal_initializer(0, 0.1))
#         item_emb_w = tf.get_variable("item_emb_w", [item_count+1, hidden_dim], 
#                                 initializer=tf.random_normal_initializer(0, 0.1))
#         item_b = tf.get_variable("item_b", [item_count+1, 1], 
#                                 initializer=tf.constant_initializer(0.0))
        
#         u_emb = tf.nn.embedding_lookup(user_emb_w, u)
#         i_emb = tf.nn.embedding_lookup(item_emb_w, i)
#         i_b = tf.nn.embedding_lookup(item_b, i)
#         j_emb = tf.nn.embedding_lookup(item_emb_w, j)
#         j_b = tf.nn.embedding_lookup(item_b, j)
    
#     # MF predict: u_i > u_j
#     x = i_b - j_b + tf.reduce_sum(tf.multiply (u_emb, (i_emb - j_emb)), 1, keepdims=True)
    
#     # AUC for one user:
#     # reasonable iff all (u,i,j) pairs are from the same user
#     # 
#     # average AUC = mean( auc for each user in test set)
#     mf_auc = tf.reduce_mean(tf.to_float(x > 0))
    
#     l2_norm = tf.add_n([
#             tf.reduce_sum(tf.multiply (u_emb, u_emb)), 
#             tf.reduce_sum(tf.multiply (i_emb, i_emb)),
#             tf.reduce_sum(tf.multiply (j_emb, j_emb))
#         ])
    
#     regulation_rate = 0.0001
#     bprloss = regulation_rate * l2_norm - tf.reduce_mean(tf.log(tf.sigmoid(x)))
    
#     train_op = tf.train.GradientDescentOptimizer(0.01).minimize(bprloss)
#     return u, i, j, mf_auc, bprloss, train_op


# if __name__ == '__main__':
#     user_ratings_test = generate_test(user_ratings)
#     print(user_ratings_test)
#     # print(generate_train_batch(user_ratings, user_ratings_test, item_count))
#     # print(generate_test_batch(user_ratings, user_ratings_test, item_count))
    
#     with tf.Graph().as_default(), tf.Session() as session:
#         u, i, j, mf_auc, bprloss, train_op = bpr_mf(user_count, item_count, 20)
#         session.run(tf.global_variables_initializer())
#         for epoch in range(1, 11):
#             _batch_bprloss = 0
#             for k in range(1, 5000): # uniform samples from training set
#                 uij = generate_train_batch(user_ratings, user_ratings_test, item_count)
                
#                 print(type(u))
#                 _bprloss, _ = session.run([bprloss, train_op], 
#                                     feed_dict={u:uij[:,0], i:uij[:,1], j:uij[:,2]})
#                 _batch_bprloss += _bprloss
            
#             print ("epoch: "), epoch
#             print ("bpr_loss: "), _batch_bprloss / k

#             user_count = 0
#             _auc_sum = 0.0

#             # each batch will return only one user's auc
#             for t_uij in generate_test_batch(user_ratings, user_ratings_test, item_count):

#                 _auc, _test_bprloss = session.run([mf_auc, bprloss],
#                                         feed_dict={u:t_uij[:,0], i:t_uij[:,1], j:t_uij[:,2]}
#                                     )
#                 user_count += 1
#                 _auc_sum += _auc
#             print ("test_loss: ", _test_bprloss, "test_auc: ", _auc_sum/user_count)
#             print ("")