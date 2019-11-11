
import sys
sys.path.append("...")

import cognitive_face as CF
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.http import JsonResponse
import json
from django.http import StreamingHttpResponse
from face import face_identity
from face import face_confirm
from face import sql_insert
from face import sql_search
from face import item2vec_model



from PIL import Image
from PIL import ImageFile
import base64
from io import BytesIO
import numpy as np
import array

KEY = 'c0b94d1aa3354dca8f79b92167b649d3'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)

BASE_URL = 'https://eastasia.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

attributes = 'gender,age,emotion'

ans = None
happiness = None
anger = None
fear = None
neutral = None
contempt = None
disgust = None
sadness = None
surprise = None
tmdbId = None
recommendation = None

def hello_world(request):
    return JsonResponse({'foo':'bar'})
    '''
   return render(request, 'hello_world.html', {
        'current_time': str(datetime.now()),
    })
    '''

# 接收POST请求数据
def img_post(request):
    global ans
    global happiness
    global anger
    global fear
    global neutral
    global contempt
    global disgust
    global sadness
    global surprise
    global tmdbId
    global recommendation
    if request.method=='POST':
            print('get post')
            received_json_data=json.loads(request.body)
            #print(str(received_json_data))
            imgdata = base64.b64decode(str(received_json_data['img']))
            image = Image.open(BytesIO(imgdata))
            image.show()
            tmp = "temp.jpg"
            image.save(tmp,'JPEG')
            
            faces = CF.face.detect(tmp, True, False, attributes)
            
            if len(faces):
                print (faces)
                next_step = True
                #return JsonResponse({'success' : 'yes', 'name' : 'somebody'})
            else:
                print ('cannot detect face')
                next_step = False
                return JsonResponse({'success' : 'no', 'name' : ''})

            if next_step == True:
                
                ans, happiness, anger, neutral, fear, contempt, disgust, sadness, surprise, tmdbId, recommendation = face_identity.identify(tmp, faces)
                print ('ans  ' , ans)

                            
                #如果是陌生人
                if ans == 'stranger':
                    return JsonResponse({'success' : 'no', 'name' : 'stranger'})
                #如果不是
                else:
                    return JsonResponse({'success' : 'yes', 'name' : str(ans), 'happiness' : str(happiness), 'anger' : str(anger), 'neutral' : str(neutral), 'fear' : str(fear), 'contempt' : str(contempt), 'disgust' : str(disgust), 'sadness' : str(sadness), 'surprise' : str(surprise), 'movie' : str(tmdbId), 'recommandation': recommendation})
    return JsonResponse({'success' : 'no', 'name' : ''})


def face_post(request):
    next_step = False
    if request.method=='POST':
            image = request.FILES.get('img')
            print('image', image)
            im = Image.open(image)
            im.show()
            tmp = "temp.jpg"
            im.save(tmp,'JPEG')
            
            faces = CF.face.detect(tmp, True, False)
            
            if len(faces):
                print (faces)
                next_step = True
                #return JsonResponse({'success' : 'yes', 'name' : 'somebody'})
            else:
                print ('cannot detect face')
                next_step = False
                return JsonResponse({'success' : 'no', 'name' : ''})

            if next_step == True:
                
                ans, happiness, anger, neutral, fear, contempt, disgust, sadness, surprise, imdbId = face_identity.identify(tmp, faces)

                print ('ans  ' , ans)
                qqq = [{'success' : 'yes', 'name' : str(ans), 'happiness' : str(happiness), 'anger' : str(anger), 'neutral' : str(neutral), 'fear' : str(fear), 'contempt' : str(contempt), 'disgust' : str(disgust), 'sadness' : str(sadness), 'surprise' : str(surprise), 'movie' : str(imdbId)}]

                            
                #如果是陌生人
                if ans == 'stranger':
                    return JsonResponse({'success' : 'no', 'name' : 'stranger'})
                #如果不是
                else:
                    # return HttpResponse(json.dumps(qqq), content_type='application/json')
                    return JsonResponse({'success' : 'yes', 'name' : str(ans), 'happiness' : str(happiness), 'anger' : str(anger), 'neutral' : str(neutral), 'fear' : str(fear), 'contempt' : str(contempt), 'disgust' : str(disgust), 'sadness' : str(sadness), 'surprise' : str(surprise), 'movie' : str(imdbId)})
    print('get not post')
    return JsonResponse({'success' : 'no', 'name' : ''})

def add_to_group(request):
    if request.method=='POST':
        received_json_data=json.loads(request.body)
        print(str(received_json_data.keys()))
        name = 'tmp_name'
        print('nameeeee = ', name)
        
        
        imgdata = base64.b64decode(str(received_json_data['pic1']))
        image = Image.open(BytesIO(imgdata))
        #image.show()
        tmp1 = "temp.jpg"
        image.save(tmp1,'JPEG')
        faces1 = CF.face.detect(tmp1, True, False)
        print('pic1 ', faces1)

        imgdata = base64.b64decode(str(received_json_data['pic2']))
        image = Image.open(BytesIO(imgdata))
        #image.show()
        tmp2 = "temp2.jpg"
        image.save(tmp2,'JPEG')
        faces2 = CF.face.detect(tmp2, True, False)
        print('pic2 ', faces2)
        

        imgdata = base64.b64decode(str(received_json_data['pic3']))
        image = Image.open(BytesIO(imgdata))
        #image.show()
        tmp3 = "temp3.jpg"
        image.save(tmp3,'JPEG')
        faces3 = CF.face.detect(tmp3, True, False)
        print('pic3 ', faces3)

        imgdata = base64.b64decode(str(received_json_data['pic4']))
        image = Image.open(BytesIO(imgdata))
        #image.show()
        tmp4 = "temp4.jpg"
        image.save(tmp4,'JPEG')
        faces4 = CF.face.detect(tmp4, True, False)
        print('pic4 ', faces4)

    
       
        print('true')
        id = ''
        rating = ''
        movieId = ''
        favorite = ''
        topic = ''
        print(name)
        print('id = ', id, 'rating = ', rating, '')
        face_confirm.create_new_person(name, tmp1, tmp2, tmp3, tmp4)
        sql_insert.insert(name, id, rating, favorite, topic)
        
            
       

        

    return JsonResponse({'success' : 'yes', 'name' : "tmp_name"})
    #return

def user_seach(request):
    sql_search.user_search('qq')

    return JsonResponse({'success' : 'yes', 'name' : ''})

# 主頁
def test_req(request):
    global ans
    global happiness
    global anger
    global fear
    global neutral
    global contempt
    global disgust
    global sadness
    global surprise
    global tmdbId
    global recommendation

    if request.method=='GET':
            print('get post')
            #received_json_data=json.loads(request.body)
            #print('body ', str(received_json_data))
            #imgdata = base64.b64decode(str(received_json_data['img']))
            #image = Image.open(BytesIO(imgdata))
            #image.show()
            tmp = "temp.jpg"
            #image.save(tmp,'JPEG')
            
            
            faces = CF.face.detect(tmp, True, False, attributes)
            
            if len(faces):
                print (faces)
                next_step = True
                #return JsonResponse({'success' : 'yes', 'name' : 'somebody'})
            else:
                print ('cannot detect face')
                next_step = False
                return JsonResponse({'success' : 'no', 'name' : ''})

            if next_step == True:
                
                ans, happiness, anger, neutral, fear, contempt, disgust, sadness, surprise, tmdbId, recommendation = face_identity.identify(tmp, faces)
                print ('ans  ' , ans)
                    
                #array = 
                #myarray = ' '.join(tmdbId)
                print('tmdbId ', tmdbId)
                print('recommendation ', recommendation)
                qqq = [{'success' : 'yes', 'name' : str(ans), 'happiness' : str(happiness), 'anger' : str(anger), 'neutral' : str(neutral), 'fear' : str(fear), 'contempt' : str(contempt), 'disgust' : str(disgust), 'sadness' : str(sadness), 'surprise' : str(surprise), 'movie' : tmdbId, 'recommandation': recommendation}]


                            
                #如果是陌生人
                if ans == 'stranger':
                    return JsonResponse({'success' : 'no', 'name' : 'stranger'})
                #如果不是
                else:
                    # return HttpResponse(json.dumps(qqq), content_type='application/json')
                    return JsonResponse({'success' : 'yes', 'name' : str(ans), 'happiness' : str(happiness), 'anger' : str(anger), 'neutral' : str(neutral), 'fear' : str(fear), 'contempt' : str(contempt), 'disgust' : str(disgust), 'sadness' : str(sadness), 'surprise' : str(surprise), 'movie' : tmdbId, 'recommandation': recommendation})
    return JsonResponse({'success' : 'no', 'name' : ''})
    
    #qqq = [{'success' : 'yes', 'name' : str(ans), 'happiness' : str(happiness), 'anger' : str(anger), 'neutral' : str(neutral), 'fear' : str(fear), 'contempt' : str(contempt), 'disgust' : str(disgust), 'sadness' : str(sadness), 'surprise' : str(surprise), 'movie' : str(tmdbId)}]
    
               
    #return HttpResponse(json.dumps(qqq), content_type='application/json')
    #return JsonResponse({'success' : 'yes', 'name' : str(ans), 'happiness' : str(happiness), 'anger' : str(anger), 'neutral' : str(neutral), 'fear' : str(fear), 'contempt' : str(contempt), 'disgust' : str(disgust), 'sadness' : str(sadness), 'surprise' : str(surprise)})


def user_list(request):
    if request.method=='POST':
            print('get post')
            received_json_data=json.loads(request.body)
            print('body ', str(received_json_data))

            face_confirm.name_update(received_json_data['name'])
            sql_search.update(received_json_data['name'], received_json_data['genres'], received_json_data['like'])
    return JsonResponse({'success' : 's'})

def update_rating(request):
    if request.method=='POST':
        received_json_data=json.loads(request.body)
        # print(str(received_json_data))
        sql_search.rating_update(received_json_data['name'], received_json_data['tmdbId'], received_json_data['rating'])

    return JsonResponse({'success' : 'update_rating'})

def update_favorite(request):
    if request.method=='POST':
        received_json_data=json.loads(request.body)
        print(str(received_json_data))
        sql_search.favorite_update(received_json_data['name'], received_json_data['tmdbId'])

    return JsonResponse({'success' : 'update_favorite'})

# 重複檢查
def get_favorite(request):
    if request.method=='POST':
        received_json_data=json.loads(request.body)
        print(str(received_json_data))
        favorite = sql_search.get_favorite(received_json_data['name'])

    return JsonResponse({'success' : favorite})

def remove_favorite(request):
    if request.method=='POST':
        received_json_data=json.loads(request.body)
        print(str(received_json_data))
        sql_search.favorite_remove(received_json_data['name'], received_json_data['tmdbId'])

    return JsonResponse({'success' : 'remove_favorite'})

def get_movie_rating(request):
    if request.method=='POST':
        received_json_data=json.loads(request.body)
        print(str(received_json_data))
        movie, rating = sql_search.get_movie_rating(received_json_data['name'])
        # new = dict()
        # for index in range(len(movie)):
        #     new[movie[index]] = rating[index]

    return JsonResponse({'tmdbId' : movie, 'rating' : rating})

# item2vector model
def post_i2vId(request):
    if request.method=='POST':
        received_json_data=json.loads(request.body)
        print(str(received_json_data))
        nearests = item2vec_model.run_sim([received_json_data['id']])
        print(nearests)
        # i2v = json.dumps(nearests[0].tolist())

    return JsonResponse({'id' : nearests})

