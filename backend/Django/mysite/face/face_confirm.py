import cognitive_face as CF
#draw face rectangle
import requests
import json
import uuid
import time
from io import BytesIO
from PIL import Image, ImageDraw
import uuid


KEY = 'c0b94d1aa3354dca8f79b92167b649d3'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)

BASE_URL = 'https://eastasia.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

TIME_SLEEP = 10



def person_train(person_group_id):
    #time.sleep(2)
    CF.util.wait_for_person_group_training(person_group_id)
    #time.sleep(2)
    res = CF.person_group.get_status(person_group_id)
    print(res)

def person_list():
    res = CF.person_group.lists()
    print(res)

def create_new_person(name, pic1, pic2, pic3, pic4):
    print('now in create process')

    #接收使用者名稱
    person_group_id = str(uuid.uuid4())
    #
    print('groupId ' + person_group_id)

    try:
        res = CF.person_group.create(person_group_id)
        print(res)
    except CF.util.CognitiveFaceException as identifier:
        print('except ', identifier)
        pass
    

    res = CF.person.create(person_group_id, name)
    person_id = res['personId']
    print(person_id)
    res = CF.person_group.update(person_group_id, name)

    #新增4張辨識圖片
    res = CF.person.add_face(pic1, person_group_id, person_id)
    res = CF.person.add_face(pic2, person_group_id, person_id)
    res = CF.person.add_face(pic3, person_group_id, person_id)
    res = CF.person.add_face(pic4, person_group_id, person_id)
    
    res = CF.person_group.train(person_group_id)
    print(res)
    #time.sleep(3)
    person_train(person_group_id)
    

    print('create complete')

def name_update(name):
    uid = None
    res =  CF.person_group.lists()
    for id in res:
        if id['name'] == 'tmp_name':
            uid = id['personGroupId']
            break
    
    res = CF.person_group.update(uid, name)





def confirm(face, img):
    confidence = 0
    value = []
    find = False
    print ('confirm start')

    res = CF.person_group.lists()
    print(res)
    print (face)
    

    for id in res:
        value = []
        if find == False:
            personId = id['personGroupId']
            value = CF.face.identify([face], personId)
            print ('personid')
            print (personId)
            print (value)
            #time.sleep(3)

        if len(value):
            print ('value')
            for tmp in value:
                tmp2 = tmp['candidates']
                print (tmp2)
        
            if len(tmp2):
                print ('else')
                for tmp3 in tmp2:
                    confidence = tmp3['confidence']
                    print (confidence)
                    find = True
                    break
                    
            else:
                print ('none')
                confidence = 0

    
       

   

    if confidence >= 0.5:
        ans = None
        for id in res:
            if personId == id['personGroupId']:
                ans = id['name']

        print (ans)
        return ans
    else:
        print ('stranger')
        #create_new_person(img)
        #person_list()
        return 'stranger'
    

   
    print ('confirm end')