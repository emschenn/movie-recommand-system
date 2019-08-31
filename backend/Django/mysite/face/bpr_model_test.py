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

user = np.loadtxt("bpr_userEmbeddingMatrix")
item = np.loadtxt("bpr_itemEmbeddingMatrix")
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

