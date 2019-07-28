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

model = keras.models.load_model('face/my_model.h5')
global graph
graph = tf.get_default_graph()

#create movie dict
df = pd.read_csv('face/mycsvfile1.csv')
df['movieId'] = df['movieId'].map(ast.literal_eval)
movie_dict = df.set_index('topic').T.to_dict('list')

#for prediction
user = np.loadtxt("../../movie_data/MovieLens/ml-latest-small/ratings.csv.user_embedding")
item = np.loadtxt("../../movie_data/MovieLens/ml-latest-small/ratings.csv.item_embedding")
user_embedding = np.delete(user, 0, 1)
item_embedding = np.delete(item, 0, 1)
item_idx = item[:,0].tolist()
item_idx = [int(i) for i in item_idx]
# print(item_idx)
# print(user_embedding)
# print(user_embedding.shape)
# print(item_embedding.shape)
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
    Id = pd.read_csv('face/most_view.csv')
    choose = list()
    emotion_list = list()
    emotion_list = (('happiness', happiness), ('anger', anger), ('neutral', neutral), ('fear', fear), ('contempt', contempt), ('disgust', disgust), ('sadness', sadness), ('surprise', surprise))
    m = max(emotion_list, key=lambda x : x[1])

    print(m[0])
    i = 0
    

    if m[0] == 'happiness':
        while i < 3:
            print( Id.loc[i, 'tmdbId'])
            choose.append( str(Id.loc[i, 'tmdbId']))
            i = i+1
        #print(choose)
        return choose
    if m[0] == 'neutral':
        while i < 3:
            print( Id.loc[i, 'tmdbId'])
            choose.append( str(Id.loc[i, 'tmdbId']))
            i = i+1
        #print(choose)
        return choose

    if surprise > 0.5:
        movie = list((movie_dict.get('Adventure')[0]))
        while i < 3:
            movieId = movie[random.randint(0, len(movie))]
            imdbId = movieId_link(movieId)
            choose.append( str(imdbId) )
            i = i+1
        return choose
    if sadness > 0.3:
        movie = list((movie_dict.get('Comedy')[0]))
        while i < 3:
            movieId = movie[random.randint(0, len(movie))]
            imdbId = movieId_link(movieId)
            choose.append( str(imdbId) )
            i = i+1
        return choose
    if anger >= 0.3:
        movie = list((movie_dict.get('Comedy')[0]))
        movie2 = list((movie_dict.get('Adventure')[0]))
        movie3 = list((movie_dict.get('Action')[0]))

        movieId = movie[random.randint(0, len(movie))]
        imdbId = movieId_link(movieId)
        choose.append( str(imdbId) )

        movieId = movie2[random.randint(0, len(movie2))]
        imdbId = movieId_link(movieId)
        choose.append( str(imdbId) )

        movieId = movie3[random.randint(0, len(movie3))]
        imdbId = movieId_link(movieId)
        choose.append( str(imdbId) )

        return choose
    if disgust > 0.3:
        movie = list((movie_dict.get('Adventure')[0]))
        movie2 = list((movie_dict.get('Fantasy')[0]))
        while i < 2:
            movieId = movie[random.randint(0, len(movie))]
            imdbId = movieId_link(movieId)
            choose.append( str(imdbId) )
            i = i+1

        movieId = movie2[random.randint(0, len(movie2))]
        imdbId = movieId_link(movieId)
        choose.append( str(imdbId) )

        return choose
    if fear >= 0.7:
        movie = list((movie_dict.get('Comedy')[0]))
        while i < 3:
            movieId = movie[random.randint(0, len(movie))]
            imdbId = movieId_link(movieId)
            choose.append( str(imdbId) )
            i = i+1
        return choose
    if contempt > 0.3:
        movie = list((movie_dict.get('Comedy')[0]))
        while i < 3:
            movieId = movie[random.randint(0, len(movie))]
            imdbId = movieId_link(movieId)
            choose.append( str(imdbId) )
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
    # movie = pd.read_csv("../../movie_data/MovieLens/ml-latest-small/movies.csv",sep=",")
    # rating = pd.read_csv("../../movie_data/MovieLens/ml-latest-small/ratings.csv",sep=",")

    # rating_id = pd.read_csv("../../movie_data/MovieLens/ml-latest-small/links.csv",sep=",")

    # rating = pd.merge(rating, rating_id, on=['movieId'])

    # #train, test = train_test_split(rating, test_size = 0.2)

    # tmdbId = list()
    # id_count = 0

   



    # user_id_test = rating['userId'].values
    # item_id_test = rating['movieId'].values
    # rating_test = rating['rating'].values

    # data = np.array(list(set(rating.movieId)))

    

    # #數字為user id
    # user = np.array([user_id for i in range(len(data))])
    # print(user)


    # #Model load
    # # model = keras.models.load_model('face/my_model.h5')
    

    # # model.summary()
    # # print(len(user))
    # # print(len(data))
   
    # global graph
    # with graph.as_default():
    #     predicted_ratings = model.predict([user, data])

    # print('data')
    # print('user ', user)
    # #print(predicted_ratings)

    # predicted_ratings = np.array([a[0] for a in predicted_ratings])
    # #print (predicted_ratings)

    # predicted_ratings = np.array([a[0] for a in predicted_ratings])
    # print (predicted_ratings)


    # recommended_movie_ids = np.negative(predicted_ratings).argsort()[:len(predicted_ratings)]

    tmdbId = list()
    id_count = 0

   
    # print(len(p[0]))
    tmp = predict_list[user_id]
    top = list()
    recommended_movie_ids = list()
    tmp2 = sorted(range(len(tmp)), key=lambda i: tmp[i])[-5:]
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
        if id_count >= 5:
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

        return result, h, a, n, f, c, d, sad, sur, tmdbId, Recommendation
    else:
        print ('no face')
        return str('stranger')


    '''
    for face in faces:
        f1 = face['faceId']
        print ('face1 ' + f1)
        h, a, n, f = getattributes(face)
        choose_movie(h, a, n, f)
        confirm(f1, img_url)

    time.sleep(1)
    '''


    '''

    img_url2 = 'D://禹竣//成大//專題//root//LIAO//2.jpg'
    i3 = Image.open(img_url2)
    #i3.show()

    faces = CF.face.detect(img_url2, True, False, attributes)

    for face in faces:
        f2 = face['faceId']
        print ('face2 ' + f2)
        h, a, n, f = getattributes(face)
        choose_movie(h, a, n, f)

    time.sleep(1)

    img_url3 = 'D://禹竣//成大//專題//root//LIAO//70.jpg'
    i4 = Image.open(img_url3)
    #i4.show()

    faces = CF.face.detect(img_url3, True, False, attributes)

    for face in faces:
        f3 = face['faceId']
        print ('face3 ' + f3)
        h, a, n, f = getattributes(face)
        choose_movie(h, a, n, f)

    time.sleep(1)


    person_group_id = 'me'
    print('groupId ' + person_group_id)

    '''
    '''

    res = CF.person_group.create(person_group_id)
    print(res)

    res = CF.person.create(person_group_id, 'TempPerson')
    person_id = res['personId']
    print(person_id)



    res = CF.person.add_face(img_url, person_group_id, person_id)
    res = CF.person_group.train(person_group_id)
    print(res)
    res = CF.person_group.update(person_group_id, 'HaHa')
    print(res)

    r = CF.person_group.get(person_group_id)
    print(r['personGroupId'])
    rect3 = r['personGroupId']
    '''
    

    #get image from web
    '''
    img = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/PersonGroup/Family1-Dad/Family1-Dad3.jpg'
    response2 = requests.get(img)
    i2 = Image.open(BytesIO(response2.content))
    i2.show()

    faces = CF.face.detect(img, True, False)

    for face in faces:
        rect = face['faceId']
        print ('face2 ' + rect)
    '''

    '''

    img = 'D://禹竣//成大//專題//root//DO//nm0000100_rm46373120_1955-1-6_2003.jpg'
    ii = Image.open(img)
    ii.show()

    faces = CF.face.detect(img, True, False)

    for face in faces:
        f4 = face['faceId']
        print ('face4 ' + f4)

    time.sleep(1)

    img2 = 'D://禹竣//成大//專題//root//DO//nm0000100_rm616798464_1955-1-6_2003.jpg'
    ii2 = Image.open(img2)
    ii2.show()

    faces = CF.face.detect(img2, True, False)

    for face in faces:
        f5 = face['faceId']
        print ('face5 ' + f5)

    time.sleep(1)

    img3 = 'D://禹竣//成大//專題//root//DO//nm0000100_rm1019451648_1955-1-6_2003.jpg'
    ii3 = Image.open(img3)
    ii3.show()

    faces = CF.face.detect(img3, True, False)

    for face in faces:
        f6 = face['faceId']
        print ('face6 ' + f6)

    time.sleep(1)

    person_group_id2 = 'other'
    print('groupId ' + person_group_id2)

    res = CF.person_group.create(person_group_id2)
    print(res)

    res = CF.person.create(person_group_id2, 'TempPerson')
    person_id2 = res['personId']
    print(person_id2)



    res = CF.person.add_face(img, person_group_id2, person_id2)
    time.sleep(10)
    res = CF.person_group.train(person_group_id2)
    print(res)
    time.sleep(10)
    res = CF.person_group.update(person_group_id2, 'Ha')
    print(res)

    r = CF.person_group.get(person_group_id2)
    print(r['personGroupId'])
    rect3 = r['personGroupId']


    res = CF.person_group.lists()
    print(res)
    time.sleep(10)
    CF.util.wait_for_person_group_training(person_group_id)
    #res = CF.person_group.train(person_group_id)
    time.sleep(2)
    res = CF.person_group.get_status(person_group_id)
    print(res)
    time.sleep(10)

    CF.util.wait_for_person_group_training(person_group_id2)
    time.sleep(2)
    res = CF.person_group.get_status(person_group_id2)
    print(res)
    time.sleep(10)

    
    res = CF.face.identify(
                [f1, f2, f3, f4, f5, f6],
                person_group_id)

    print(res)

    time.sleep(2)

    res = CF.face.identify(
                [f1, f2, f3, f4, f5, f6],
                person_group_id2)

    print(res)
'''





        
#if __name__=='__main__':
    #identify()