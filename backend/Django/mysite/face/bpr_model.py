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


file = open('BPR_data/bpr_userMatrix_train_611.pickle', 'rb')
bpr_userMatrix_train =pickle.load(file)
file.close()
file = open('BPR_data/bpr_itemPositiveMatrix_train_611.pickle', 'rb')
bpr_itemPositiveMatrix_train =pickle.load(file)
file.close()
file = open('BPR_data/bpr_itemNegativeMatrix_train_611.pickle', 'rb')
bpr_itemNegativeMatrix_train =pickle.load(file)
file.close()
file = open('BPR_data/bpr_userIndexToNameDict_611.pickle', 'rb')
userIndexToNameDict =pickle.load(file)
file.close()
file = open('BPR_data/bpr_itemIndexToNameDict_611.pickle', 'rb')
itemIndexToNameDict =pickle.load(file)
file.close()

print(userIndexToNameDict)

regularizationScale = 0
embeddingDimension = 10
userCount = 611
itemCount = 9724
epochCount = 10
batchSize = 256


def getSoftplusLoss(labelMatrix, predictionMatrix):
    return K.mean(K.softplus(- predictionMatrix))

# Count the ratio of prediction value > 0 (i.e., predicting positive item score > negative item score for a user)
def getAUC(labelMatrix, predictionMatrix):
    return K.mean(K.switch(predictionMatrix > 0, K.ones_like(predictionMatrix), K.zeros_like(predictionMatrix)))

def getDotDifference(parameterMatrixList):
    userEmbeddingMatrix, itemPositiveEmbeddingMatrix, itemNegativeEmbeddingMatrix = parameterMatrixList
    return K.batch_dot(userEmbeddingMatrix, itemPositiveEmbeddingMatrix, axes = 1) - K.batch_dot(userEmbeddingMatrix, itemNegativeEmbeddingMatrix, axes = 1)

def getDotDifferenceShape(shapeVectorList):
    userEmbeddingShapeVector, itemPositiveEmbeddingShapeVector, itemNegativeEmbeddingShapeVector = shapeVectorList
    return userEmbeddingShapeVector[0], 1



# userInputLayer = Input(shape = (1, ), dtype = "int32")

# itemPositiveInputLayer = Input(shape = (1, ), dtype = "int32")
# itemNegativeInputLayer = Input(shape = (1, ), dtype = "int32")

userInputLayer = Input((1, ))

itemPositiveInputLayer = Input((1, ))
itemNegativeInputLayer = Input((1, ))

userEmbeddingLayer = Embedding(input_dim = userCount, output_dim = embeddingDimension, input_length = 1, 
        embeddings_regularizer = l2(regularizationScale), embeddings_initializer = RandomNormal())(userInputLayer)
userEmbeddingLayer = Flatten()(userEmbeddingLayer)

# Both positive and negative items share the same embedding space
itemEmbeddingLayer = Embedding(input_dim = itemCount, output_dim = embeddingDimension, input_length = 1, 
        embeddings_regularizer = l2(regularizationScale), embeddings_initializer = RandomNormal())

itemPositiveEmbeddingLayer = itemEmbeddingLayer(itemPositiveInputLayer)
itemPositiveEmbeddingLayer = Flatten()(itemPositiveEmbeddingLayer)

itemNegativeEmbeddingLayer = itemEmbeddingLayer(itemNegativeInputLayer)
itemNegativeEmbeddingLayer = Flatten()(itemNegativeEmbeddingLayer)

dotDifferenceLayer = Lambda(getDotDifference, output_shape = getDotDifferenceShape) \
    ([userEmbeddingLayer, itemPositiveEmbeddingLayer, itemNegativeEmbeddingLayer])

model = Model(inputs = [userInputLayer, itemPositiveInputLayer, itemNegativeInputLayer], outputs = dotDifferenceLayer)
model.compile(optimizer = "adam", loss = getSoftplusLoss, metrics = [getAUC])


# Label set does not exist in BPR, so we give Keras with a dummy label set
labelMatrix = np.ones((bpr_userMatrix_train.shape[0], 1), dtype = int);


model.fit([bpr_userMatrix_train, bpr_itemPositiveMatrix_train, bpr_itemNegativeMatrix_train], labelMatrix, epochs = epochCount, batch_size = batchSize,
               callbacks = [EarlyStopping(mode = "min")])


userIndexMatrix = np.arange(userCount, dtype = int).reshape(-1, 1)
itemIndexMatrix = np.arange(itemCount, dtype = int).reshape(-1, 1)


userEmbeddingOutputModel = Model(inputs = userInputLayer, outputs = userEmbeddingLayer)
userEmbeddingMatrix = userEmbeddingOutputModel.predict(userIndexMatrix)

itemEmbeddingOutputModel = Model(inputs = itemPositiveInputLayer, outputs = itemPositiveEmbeddingLayer)
itemEmbeddingMatrix = itemEmbeddingOutputModel.predict(itemIndexMatrix)

userNameVector = np.array([userIndexToNameDict[index] for index in range(userEmbeddingMatrix.shape[0])])
itemNameVector = np.array([itemIndexToNameDict[index] for index in range(itemEmbeddingMatrix.shape[0])])

np.savetxt('BPR_data/bpr_userEmbeddingMatrix_611', np.hstack((userNameVector[np.newaxis].T, userEmbeddingMatrix)), fmt = "%g", header = "", delimiter = " ")
np.savetxt("BPR_data/bpr_itemEmbeddingMatrix_611", np.hstack((itemNameVector[np.newaxis].T, itemEmbeddingMatrix)), fmt = "%g", header = "", delimiter = " ")
# print(userEmbeddingMatrix)
# print(itemEmbeddingMatrix)

file = open('BPR_data/bpr_userMatrix_test_611.pickle', 'rb')
bpr_userMatrix_test =pickle.load(file)
file.close()
file = open('BPR_data/bpr_itemPositiveMatrix_test_611.pickle', 'rb')
bpr_itemPositiveMatrix_test =pickle.load(file)
file.close()
file = open('BPR_data/bpr_itemNegativeMatrix_test_611.pickle', 'rb')
bpr_itemNegativeMatrix_test =pickle.load(file)
file.close()

predict = np.mat(userEmbeddingMatrix) * np.mat(itemEmbeddingMatrix.T)
print(predict.shape)
p = predict.tolist()
# print((bpr_userMatrix_test))
# print(len(bpr_itemPositiveMatrix_test))
total = len(bpr_userMatrix_test)
count = 0
for idx in range(len(bpr_userMatrix_test)):
        # print(idx)
        # print('postive', p[int(bpr_userMatrix_test[idx])][int(bpr_itemPositiveMatrix_test[idx])])
        # print('negative', p[int(bpr_userMatrix_test[idx])][int(bpr_itemNegativeMatrix_test[idx])])
        post = p[int(bpr_userMatrix_test[idx])][int(bpr_itemPositiveMatrix_test[idx])]
        nega = p[int(bpr_userMatrix_test[idx])][int(bpr_itemNegativeMatrix_test[idx])]
        if post > 0 and nega < 0 and post > nega:
                count += 1

print(count / total)
