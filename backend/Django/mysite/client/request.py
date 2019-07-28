# 引入 requests 模組
import requests
import json

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import base64
from io import BytesIO

# pip3 install pillow
from PIL import Image

# 使用 GET 方式下載普通網頁
# r = requests.get('http://127.0.0.1:8000/test/')
url = 'http://127.0.0.1:8000/new_user_list/'
data = ({'name': '1234', 'genres': ['Animation', 'Sci-Fi'], 'like': ['10193', '129', '181808', '49047']})
headers = {'content-type': 'application/json'}
# r = requests.post(url, data=json.dumps(data), headers=headers)
url = 'http://127.0.0.1:8000/post/'
# with open('../temp2.jpg', "rb") as imageFile:
#     str1 = base64.b64encode(imageFile.read()).decode("utf-8")
with open('../../../image/tmp_5.jpg', "rb") as imageFile:
    str1 = base64.b64encode(imageFile.read()).decode("utf-8")
data = ({'img':str1})
r = requests.post(url, data=json.dumps(data), headers=headers)
files={'pic1':('test.png',open('../../../image/tmp_1.jpg','rb'),'image/png')}
# r = requests.post(url, data=json.dumps(data), headers=headers)
url = 'http://127.0.0.1:8000/add/'

with open('../../../image/tmp_5.jpg', "rb") as imageFile:
    str1 = base64.b64encode(imageFile.read()).decode("utf-8")

with open('../../../image/tmp_6.jpg', "rb") as imageFile:
    str2 = base64.b64encode(imageFile.read()).decode("utf-8")

with open('../../../image/tmp_7.jpg', "rb") as imageFile:
    str3 = base64.b64encode(imageFile.read()).decode("utf-8")

with open('../../../image/tmp_8.jpg', "rb") as imageFile:
    str4 = base64.b64encode(imageFile.read()).decode("utf-8")

data = ({'name':'tmp_name', 'pic1':str1, 'pic2':str2, 'pic3':str3, 'pic4':str4})
headers = {'content-type': 'application/json'}
#r = requests.post(url, data=json.dumps(data), headers=headers)

url = 'http://127.0.0.1:8000/user/'
data = ({'img':'val1'})
headers = {'content-type': 'application/json'}
#r = requests.post(url, data=json.dumps(data), headers=headers)

url = 'http://127.0.0.1:8000/update_rating/'
data = ({'name': '1234', 'tmdbId': '710', 'rating': '3'})
headers = {'content-type': 'application/json'}
# r = requests.post(url, data=json.dumps(data), headers=headers)

url = 'http://127.0.0.1:8000/update_favorite/'
data = ({'name': '1234', 'tmdbId': '777'})
headers = {'content-type': 'application/json'}
# r = requests.post(url, data=json.dumps(data), headers=headers)

url = 'http://127.0.0.1:8000/get_favorite/'
data = ({'name': '1234'})
headers = {'content-type': 'application/json'}
# r = requests.post(url, data=json.dumps(data), headers=headers)

url = 'http://127.0.0.1:8000/remove_favorite/'
data = ({'name': '1234', 'tmdbId': '777'})
headers = {'content-type': 'application/json'}
# r = requests.post(url, data=json.dumps(data), headers=headers)

url = 'http://127.0.0.1:8000/get_movie_rating/'
data = ({'name': '1234'})
headers = {'content-type': 'application/json'}
# r = requests.post(url, data=json.dumps(data), headers=headers)



#r.json()
# 伺服器回應的狀態碼
print(r.status_code)
print(r.text)
# 檢查狀態碼是否 OK
'''
if r.status_code == requests.codes.ok:
    print("OK")
    # 輸出網頁 HTML 原始碼
    #r.json()
    print(r.text)
'''