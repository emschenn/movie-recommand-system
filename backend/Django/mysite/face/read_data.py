import pandas as pd
import csv
import ast
import math
import numpy as np
import keras
import pickle




def topic():
    movie_topic = dict()
    df = pd.read_csv('../../../movie_data/MovieLens/ml-latest-small/movies.csv')

    for index, i in df.iterrows():
        #print(i)
        topic = df.loc[index, 'genres'].split('|')

        #Traversing all topic
        for tmp in topic:
            #print (tmp)
            if tmp in movie_topic:
                movie_topic[tmp].add(i['movieId'])
            else:
                movie_topic[tmp] = set()
                movie_topic[tmp].add(i['movieId'])



    with open('mycsvfile.csv', 'w', newline='') as f:  # Just use 'w' mode in 3.x
        w = csv.writer(f)
        for key, val in movie_topic.items():
            w.writerow([key, val])
    
def most_rating():
    ratings_count = list()
    tmdbId = list()
    movieId = list()
    rating = pd.read_csv('../../../movie_data/MovieLens/ml-latest-small/ratings.csv')
    rating_id = pd.read_csv('../../../movie_data/MovieLens/ml-latest-small/links.csv')
    rating = pd.merge(rating, rating_id, on=['movieId'])
    #print(rating)

    for movie in rating['tmdbId']:
        #if tmdbId is null then not append
        if(math.isnan(movie)):
            pass
        else:
            ratings_count.append((int(movie)))
    
    for id in ratings_count:
        if(id in tmdbId):
            pass
        else:
            tmdbId.append(id)
    
    for id in tmdbId:
        movieId.append((id, ratings_count.count(id)))
    
    movieId.sort(key=lambda x : x[1], reverse=True)
    '''
    with open('most_view.csv', 'w', newline='') as f:  # Just use 'w' mode in 3.x
        w = csv.writer(f)
        w.writerow(['tmdbId', 'times'])
        for key, val in movieId:
            w.writerow([key, val])
    '''
    
def choose_movie_by_emotion():
    
        #Id = pd.read_csv('most_view.csv')
        df = pd.read_csv('mycsvfile.csv')
        df['movieId'] = df['movieId'].map(ast.literal_eval)
        movie_dict = df.set_index('topic').T.to_dict('list')
        choose = list()
        i = 0
        

        '''
        print('choose')
        i = 0
        while i < 5:
            print( Id.loc[i, 'tmdbId'])
            choose.append( Id.loc[i, 'tmdbId'])
            i = i+1
        #print(choose)
        '''
        return choose

def movieId_link(id):
    df = pd.read_csv("mycsvfile.csv",sep=",")
    imdb_id = pd.read_csv("../../../movie_data/MovieLens/ml-latest-small/links.csv",sep=",")

    df['movieId'] = df['movieId'].map(ast.literal_eval)
    movie_dict = df.set_index('topic').T.to_dict('list')

    #ttt = list((movie_dict.get('Comedy')[0]))

    topic = imdb_id.loc[imdb_id['movieId'] == id]

    print('idididdididi', topic['tmdbId'].values)
    if(topic['tmdbId'].values != None):
        return int(float(''.join(str(i) for i in topic['tmdbId'].values)))


def choose_movie_by_data(user_id):
    movie = pd.read_csv("../../../movie_data/MovieLens/ml-latest-small/movies.csv",sep=",")
    rating = pd.read_csv("../../../movie_data/MovieLens/ml-latest-small/ratings.csv",sep=",")

    rating_id = pd.read_csv("../../../movie_data/MovieLens/ml-latest-small/links.csv",sep=",")

    rating = pd.merge(rating, rating_id, on=['movieId'])

    #train, test = train_test_split(rating, test_size = 0.2)

    tmdbId = list()
    id_count = 0



    user_id_test = rating['userId'].values
    item_id_test = rating['movieId'].values
    rating_test = rating['rating'].values

    data = np.array(list(set(rating.movieId)))

    #數字為user id
    user = np.array([user_id for i in range(len(data))])


    #Model load
    model = keras.models.load_model('my_model.h5')

    predicted_ratings = model.predict([user, data])
    #print(predicted_ratings)

    predicted_ratings = np.array([a[0] for a in predicted_ratings])
    #print (predicted_ratings)

    predicted_ratings = np.array([a[0] for a in predicted_ratings])
    print (predicted_ratings)


    recommended_movie_ids = np.negative(predicted_ratings).argsort()[:len(predicted_ratings)]
    #print(recommended_movie_ids)
    for id in recommended_movie_ids:
        i = movieId_link(id)
        if(i != None):
            tmdbId.append(i)
            id_count += 1
        if id_count >= 5:
            break

    print(tmdbId)    
    #print(predicted_ratings[recommended_book_ids])
    #movie.head()
    #print(recommended_movie_ids)
    #print(movie[movie['movieId'].isin(recommended_movie_ids)])

    #元素轉成List
    '''
    first = [recommended_movie_ids[0]]
    second = [recommended_movie_ids[1]]
    third = [recommended_movie_ids[2]]

    print('1 ', movie[movie['movieId'].isin(first)])
    print('2 ', movie[movie['movieId'].isin(second)])
    print('3 ', movie[movie['movieId'].isin(third)])
    '''
    print("recommadation")
    return tmdbId

def id_to_name():
    mdict = dict()
    movie = pd.read_csv("name_to_id.csv",sep=",")
    print(movie[movie['862'].isnull()])
    movie = movie.dropna(subset=['862'])
    movie['862'] = movie['862'].astype(int)
    print('-----')
    for id, name in movie.iterrows():
        # print(name['862'], name['Toy Story (1995)'])
        # if math.isnan(int(name['862'])):
            # print(int(name['862']))
        mdict[name['862']] = name['Toy Story (1995)']
    mdict[862] = 'Toy Story (1995)'
    # print(mdict)
    file = open('id_to_name.pickle', 'wb')
    pickle.dump(mdict, file)
    file.close()

   


if __name__ == "__main__":
    #i = choose_movie_by_emotion()
    #print('i', i)
    # i = choose_movie_by_data(5)
    # print(i)
    id_to_name()