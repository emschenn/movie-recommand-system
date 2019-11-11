import sys
import numpy as np
from pandas import read_csv
from keras.layers import Input, Embedding, Flatten, Lambda
from keras.models import Model
from keras.initializers import RandomNormal
from keras.regularizers import l2
from keras.callbacks import EarlyStopping
from keras import backend as K
import pickle

from sql_search import get_movie_rating



negativeSampleCountPerPositive = 3
userNameToIndexDict = dict()
userIndexToNameDict = dict()
userIndex = 0

itemNameToIndexDict = dict()
itemIndexToNameDict = dict()
itemIndex = 0

ratingMatrix = read_csv('../../../movie_data/MovieLens/ml-latest-small/ratings.csv', usecols = [0,1,2], header = None, skiprows=1, sep=",").as_matrix()


def readRatings():
    global userNameToIndexDict
    global userIndexToNameDict
    global userIndex

    global itemNameToIndexDict
    global itemIndexToNameDict
    global itemIndex
   
    
    print(ratingMatrix)

    for (r, (user, item, weight)) in enumerate(ratingMatrix):
        # print(r, user, item, weight)
        user = int(user)
        item = int(item)

        if user not in userNameToIndexDict:
            userNameToIndexDict[user] = userIndex
            userIndexToNameDict[userIndex] = user
            userIndex += 1

        if item not in itemNameToIndexDict:
            itemNameToIndexDict[item] = itemIndex
            itemIndexToNameDict[itemIndex] = item
            itemIndex += 1

        user = userNameToIndexDict[user]
        item = itemNameToIndexDict[item]

        ratingMatrix[r] = [user, item, weight]
        # print(ratingMatrix)
    # file = open('bpr_userNameToIndexDict.pickle', 'wb')
    # pickle.dump(userNameToIndexDict, file)
    # file.close()
    # file = open('bpr_itemNameToIndexDict.pickle', 'wb')
    # pickle.dump(itemNameToIndexDict, file)
    # file.close()
    # file = open('bpr_userIndexToNameDict.pickle', 'wb')
    # pickle.dump(userIndexToNameDict, file)
    # file.close()
    # file = open('bpr_itemIndexToNameDict.pickle', 'wb')
    # pickle.dump(itemIndexToNameDict, file)
    # file.close()


    # return

def generateInstances(ratingMatrix):
        positiveSetList = [set() for user in range(userCount)]
        positiveCount = 0

        for (user, item, rating) in ratingMatrix: 
            
            user = int(user)
            item = int(item)
            positiveSetList[user].add(item)
            positiveCount += 1

        instanceMatrix = np.zeros((negativeSampleCountPerPositive * positiveCount, 3), dtype = int)
        row = 0

        for (user, item, rating) in ratingMatrix:
            user = int(user)
            item = int(item)

            for s in range(negativeSampleCountPerPositive):
                other = np.random.randint(itemCount)
                while other in positiveSetList[user]:
                    other = np.random.randint(itemCount)

                instanceMatrix[row] = [user, item, other]
                row += 1

        np.random.shuffle(instanceMatrix)

        return instanceMatrix[:, 0].reshape(-1, 1), instanceMatrix[:, 1].reshape(-1, 1), instanceMatrix[:, 2].reshape(-1, 1)

if __name__ == '__main__':
    readRatings()
    userCount = int(ratingMatrix[: , 0].max()) + 1
    itemCount = int(ratingMatrix[: , 1].max()) + 1

    print(userCount, "users")
    print(itemCount, "items")
    print(ratingMatrix.shape[0], "ratings")


    # add new user
    movie, rating = get_movie_rating('emschen')
    print(movie)
    print(rating)

    print(ratingMatrix.shape)
    for idx in range(len(movie)):
        print(int(userCount))
        add = np.array([int(userCount), int(movie[idx]), float(rating[idx])], ndmin=2)
        print(add.shape)
        ratingMatrix = np.concatenate((ratingMatrix, add))

    print(ratingMatrix)
    userCount = int(ratingMatrix[: , 0].max()) + 1
    itemCount = int(ratingMatrix[: , 1].max()) + 1

    print(userCount, "users")
    print(itemCount, "items")
    print(ratingMatrix.shape[0], "ratings")
    # =======================

    np.random.shuffle(ratingMatrix)
    userMatrix, itemPositiveMatrix, itemNegativeMatrix = generateInstances(ratingMatrix)
    print(len(userMatrix))
    print(len(itemPositiveMatrix))
    print(len(itemNegativeMatrix))
    length = len(userMatrix)
    cut = int(length/10)
    print(cut)

    # file = open('bpr_userMatrix_train.pickle', 'wb')
    # file2 = open('bpr_itemPositiveMatrix_train.pickle', 'wb')
    # file3 = open('bpr_itemNegativeMatrix_train.pickle', 'wb')

    # userMatrix_train = userMatrix[:length - cut]
    # itemPositiveMatrix_train = itemPositiveMatrix[:length - cut]
    # itemNegativeMatrix_train = itemNegativeMatrix[:length - cut]

    # pickle.dump(userMatrix_train, file)
    # pickle.dump(itemPositiveMatrix_train, file2)
    # pickle.dump(itemNegativeMatrix_train, file3)

    # file.close()
    # file2.close()
    # file3.close()

    # file = open('bpr_userMatrix_test.pickle', 'wb')
    # file2 = open('bpr_itemPositiveMatrix_test.pickle', 'wb')
    # file3 = open('bpr_itemNegativeMatrix_test.pickle', 'wb')


    # userMatrix_test = userMatrix[length - cut:]
    # itemPositiveMatrix_test = itemPositiveMatrix[length - cut:]
    # itemNegativeMatrix_test = itemNegativeMatrix[length - cut:]

    # pickle.dump(userMatrix_test, file)
    # pickle.dump(itemPositiveMatrix_test, file2)
    # pickle.dump(itemNegativeMatrix_test, file3)

    # file.close()
    # file2.close()
    # file3.close()

 