import sys

import cognitive_face as CF
#draw face rectangle
import requests
import json
import uuid
import time
import random
from io import BytesIO
from PIL import Image, ImageDraw
#from face.sql_search import happiness_movie, anger_movie, neutral_movie, fear_movie
from face.face_confirm import confirm
from face.movie_link import movieId_link
import pandas as pd
import csv
import ast
import numpy as np
import keras
from face import sql_search
from face import user_similarity
import tensorflow as tf



KEY = 'c0b94d1aa3354dca8f79b92167b649d3'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)

BASE_URL = 'https://eastasia.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

attributes = 'gender,age,emotion'

TIME_SLEEP = 10

# model = keras.models.load_model('face/my_model.h5')
global graph
graph = tf.get_default_graph()

#create movie dict
df = pd.read_csv('face/util_data/mycsvfile1.csv')
df['movieId'] = df['movieId'].map(ast.literal_eval)
movie_dict = df.set_index('topic').T.to_dict('list')

#BPR prediction
user = np.loadtxt("face/BPR_data/bpr_userEmbeddingMatrix")
item = np.loadtxt("face/BPR_data/bpr_itemEmbeddingMatrix")
user_embedding = np.delete(user, 0, 1)
item_embedding = np.delete(item, 0, 1)
item_idx = item[:,0].tolist()
item_idx = [int(i) for i in item_idx]
predict = np.mat(user_embedding) * np.mat(item_embedding.T)
# print(predict)
predict_list = predict.tolist()



#取得臉部情緒
def getattributes(faceDictionary):
    rect2 = faceDictionary['faceAttributes']
    rect = rect2['emotion']
    h = rect['happiness']
    a = rect['anger']
    n = rect['neutral']
    f = rect['fear']
    c = rect['contempt']
    d = rect['disgust']
    sad = rect['sadness']
    sur = rect['surprise']
    return h, a, n, f, c, d, sad, sur

#根據情緒挑選電影
#rule base
def choose_movie_by_emotion(happiness, anger, neutral, fear, contempt, disgust, sadness, surprise):
    Id = pd.read_csv('face/util_data/most_view.csv')
    choose = list()
    emotion_list = list()
    emotion_list = (('happiness', happiness), ('anger', anger), ('neutral', neutral), ('fear', fear), ('contempt', contempt), ('disgust', disgust), ('sadness', sadness), ('surprise', surprise))
    m = max(emotion_list, key=lambda x : x[1])

    print(m[0])
    i = 0
    

    if m[0] == 'happiness':
        while i < 10:
            print( Id.loc[i, 'tmdbId'])
            choose.append( int(Id.loc[i, 'tmdbId']))
            i = i+1
        #print(choose)
        return choose
    if m[0] == 'neutral':
        while i < 10:
            print( Id.loc[i, 'tmdbId'])
            choose.append( int(Id.loc[i, 'tmdbId']))
            i = i+1
        #print(choose)
        return choose

    if surprise > 0.5:
        movie = list((movie_dict.get('Adventure')[0]))
        while i < 10:
            movieId = movie[random.randint(0, len(movie))]
            imdbId = movieId_link(movieId)
            choose.append( int(imdbId) )
            i = i+1
        return choose
    if sadness > 0.3:
        movie = list((movie_dict.get('Comedy')[0]))
        while i < 10:
            movieId = movie[random.randint(0, len(movie))]
            imdbId = movieId_link(movieId)
            choose.append( int(imdbId) )
            i = i+1
        return choose
    if anger >= 0.3:
        movie = list((movie_dict.get('Comedy')[0]))
        movie2 = list((movie_dict.get('Adventure')[0]))
        movie3 = list((movie_dict.get('Action')[0]))

        while i < 3:
            movieId = movie[random.randint(0, len(movie))]
            imdbId = movieId_link(movieId)
            choose.append( int(imdbId) )
            i = i+1

        while i < 6:
            movieId = movie2[random.randint(0, len(movie2))]
            imdbId = movieId_link(movieId)
            choose.append( int(imdbId) )
            i = i+1

        while i < 10:
            movieId = movie3[random.randint(0, len(movie3))]
            imdbId = movieId_link(movieId)
            choose.append( int(imdbId) )
            i = i+1

        return choose
    if disgust > 0.3:
        movie = list((movie_dict.get('Adventure')[0]))
        movie2 = list((movie_dict.get('Fantasy')[0]))
        while i < 6:
            movieId = movie[random.randint(0, len(movie))]
            imdbId = movieId_link(movieId)
            choose.append( int(imdbId) )
            i = i+1

        while i < 10:
            movieId = movie2[random.randint(0, len(movie2))]
            imdbId = movieId_link(movieId)
            choose.append( int(imdbId) )
            i = i+1

        return choose
    if fear >= 0.7:
        movie = list((movie_dict.get('Comedy')[0]))
        while i < 10:
            movieId = movie[random.randint(0, len(movie))]
            imdbId = movieId_link(movieId)
            choose.append( int(imdbId) )
            i = i+1
        return choose
    if contempt > 0.3:
        movie = list((movie_dict.get('Comedy')[0]))
        while i < 10:
            movieId = movie[random.randint(0, len(movie))]
            imdbId = movieId_link(movieId)
            choose.append( int(imdbId) )
            i = i+1
        return choose
    #movie_search()

def new_user(name, genres, like):
    rating = list()
    for topic in genres:
        print(topic)
        rating.append(5)
    for tmdbId in like:
        print(tmdbId)

    sql_search.update('First', like, rating, genres)

#新加入使用者id
def create_id():
    rating = pd.read_csv("../../movie_data/MovieLens/ml-latest-small/ratings.csv",sep=",")
    bottom = rating.tail(1)
    newest_id = int(bottom['userId'].to_string(index=False)) + 1
    print('newest_id', newest_id)
    return newest_id



#根據使用者習慣推薦電影
#user_id先用random 資料庫處理完後再更新
#model
def choose_movie_by_data(user_id):
    tmdbId = list()
    id_count = 0

   
    # print(len(p[0]))
    tmp = predict_list[user_id]
    top = list()
    recommended_movie_ids = list()
    tmp2 = sorted(range(len(tmp)), key=lambda i: tmp[i])[-10:]
    # print(tmp2)
    for t in tmp2:
        top.append(t)
    top.reverse()
    # print(top)
    for i in top:
        recommended_movie_ids.append(item_idx[i-1])
        # print(item_idx[i-1])

    #print(recommended_movie_ids)
    for id in recommended_movie_ids:
        i = movieId_link(id)
        if(i != None):
            tmdbId.append(i)
            id_count += 1
        if id_count >= 10:
            break

    #print(tmdbId)    
  

    print("recommadation")
    return tmdbId




#將傳進來的臉部圖片分析
def identify(path, faces):
    print('face identify')
  
    #print ('nice ', ttt[random.randint(0, 610)])
    

    # You can use this example JPG or replace the URL below with your own URL to a JPEG image.
    #img_url = 'D://禹竣//成大//專題//root//LIAO//1.jpg'
    img_url = path
    i = Image.open(img_url)
    #i.show()

    #辨識臉部資訊
    #faces = CF.face.detect(img_url, True, False, attributes)
    
    if len(faces):
        print (faces)
        
        for face in faces:
            f1 = face['faceId']
            print ('face1 ' + f1)
            h, a, n, f, c, d, sad, sur= getattributes(face)

            print ('happiness: %f anger: %f neutral: %f fear: %f contempt: %f disgust: %f sadness: %f surprise: %f' % 
            (h, a, n, f, c, d, sad, sur))
            
            #接資料庫



            #model推薦電影
            # Recommendation = choose_movie_by_data(5)  # [13, 278, 680, 9691, 451]
            
            #心情推薦電影
            tmdbId = choose_movie_by_emotion(h, a, n, f, c, d, sad, sur)
        
        result = confirm(f1, img_url)
        # model推薦電影
        bpr = sql_search.get_bpr(result)
        if bpr == 1:
            Recommendation = choose_movie_by_data(5)  # [13, 278, 680, 9691, 451]
        else:
            movie, rating = sql_search.get_movie_rating(result)
            new = dict()
            for index in range(len(movie)):
                new[movie[index]] = rating[index]
            Recommendation_user = user_similarity.similitary(new)
            print(Recommendation_user[0])
            Recommendation = choose_movie_by_data(Recommendation_user[0])

        # i2v
        # valid_words, nearests = item2vec.nearest_words(0, 10)

        return result, h, a, n, f, c, d, sad, sur, tmdbId, Recommendation
    else:
        print ('no face')
        return str('stranger')

        
#if __name__=='__main__':
    #identify()