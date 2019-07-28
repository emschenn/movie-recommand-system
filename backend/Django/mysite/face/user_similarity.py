import sys

import numpy as np
import pandas as pd
import ast
import math
import csv
from collections import defaultdict
from scipy import spatial
import collections
from sklearn.metrics.pairwise import cosine_similarity

# 收集user-item資訊
# user =  pd.read_csv("../../../movie_data/MovieLens/ml-latest-small/ratings.csv",sep=",")
# user_dict = defaultdict(list)

# df = pd.read_csv("mycsvfile.csv",sep=",")
# imdb_id = pd.read_csv("../../../movie_data/MovieLens/ml-latest-small/links.csv",sep=",")
# df['movieId'] = df['movieId'].map(ast.literal_eval)
# movie_dict = df.set_index('topic').T.to_dict('list')


# def movieId_link(id):
#     topic = imdb_id.loc[imdb_id['movieId'] == id]

#     # print('idididdididi', topic['tmdbId'].values)
#     if(topic['tmdbId'].values != None):
#         if(math.isnan(float(''.join(str(i) for i in topic['tmdbId'].values))) == False):
#             return int(float(''.join(str(i) for i in topic['tmdbId'].values)))


# def user_rating_matrix():
#     length = 0
#     for index, i in user.iterrows():
#         save = dict()
#         id = user.loc[index, 'userId']
#         # print(id)
#         mId = user.loc[index, 'movieId']
#         tmdb = movieId_link(mId)
#         rating = user.loc[index, 'rating']
#         save[tmdb] = rating
#         # print(title)
#         if(tmdb != math.nan):
#             user_dict[id].append(save)
#             length += 1
    
#     with open('user_rating.csv', 'w', encoding = 'utf8', newline='') as f:  # Just use 'w' mode in 3.x
#         w = csv.writer(f)
#         for key, val in user_dict.items():
#             w.writerow([key, val])


# 資料處理
# user_rating_matrix = pd.read_csv("user_rating.csv",sep=",")


# def user_rating_matrix2():
#     user_rating_matrix['rating'] = user_rating_matrix['rating'].map(ast.literal_eval)
#     movie_dict = user_rating_matrix.set_index('userId').T.to_dict('list')
#     last = dict()
#     for index in movie_dict:
#         t = movie_dict[index]
#         new = dict()
#         for i in t[0]:
#             for key, value in i.items():
#                 new[key] = value
#         # print(new)
#         last[index] = new
#         with open('user_rating_last.csv', 'w', encoding = 'utf8', newline='') as f:  # Just use 'w' mode in 3.x
#             w = csv.writer(f)
#             w.writerow(['userId', 'rating'])
#             for key, val in last.items():
#                 w.writerow([key, val])

# cosine similarity 
user_rating_matrix = pd.read_csv("face/user_rating_last.csv",sep=",")
user_rating_matrix['rating'] = user_rating_matrix['rating'].map(ast.literal_eval)
movie_dict = user_rating_matrix.set_index('userId').T.to_dict('list')
def similitary(new_user):
   

    similitary_list = dict()

    
    # 遍歷所有使用者
    for i in range(len(movie_dict)):
        old_user = movie_dict[i + 1]
        # 解開list
        old_user_1 = old_user[0]
        # print(old_user_1)
        old_rating = list()
        new_rating = list()
        for movieId, rating in new_user.items():
            # print(old_user_1.get(int(movieId)))
            if old_user_1.get(int(movieId)) != None:
                new_rating.append(int(rating))
                old_rating.append(old_user_1.get(int(movieId)))
        # print(new_rating)
        # print(old_rating)

        if len(new_rating) != 0:
            # Pearson correlation-based similarity 
            # 評分平均
            new_arg = sum(new_rating) / len(new_rating)
            old_arg = sum(old_rating) / len(old_rating)
            for j in range(len(new_rating)):
                if (new_rating[j] - new_arg) == 0:
                    new_rating[j] = 0.001
                else:
                    new_rating[j] = new_rating[j] - new_arg
                if (old_rating[j] - old_arg) == 0:
                    old_rating[j] = 0.001
                else:
                    old_rating[j] = old_rating[j] - old_arg
            if sum(new_rating) != 0 and sum(old_rating) != 0:
                result = 1 - spatial.distance.cosine(new_rating, old_rating)
            else:
                result = 0
            # print(spatial.distance.cosine(new_ratig, old_rating))
            # print(result)
        else:
            result = 0
        
        # print(i+1, ' ', result)
        # if len(new_ratig) != 0:
        #     result = result / len(new_ratig)
        # print(result)
        similitary_list[i+1] = result
        old_rating.clear()
        new_rating.clear()
      

    # print(similitary_list)
    sorted_x = sorted(similitary_list.items(), key=lambda d: d[1], reverse = True)
    # print(sorted_x)
    Recommendation = list()
    for i in range(3):
        print(sorted_x[i])
        Recommendation.append(sorted_x[i][0])

    # print( movie_dict[270][0].get(949))
    # print( movie_dict[270][0].get(15602))
    # print( movie_dict[270][0].get(862))
    
    return Recommendation
        
    



if __name__ == '__main__':
    # user_rating_matrix()
    # user_rating_matrix2()
    new = dict()
    new[862] = 1
    new[15602] = 1
    new[949] = 1
    # print(new)
    r = similitary(new)
    print(r)