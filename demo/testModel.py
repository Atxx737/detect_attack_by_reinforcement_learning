import keras
# import the class
from functions_final import DeepQLearning
import pandas as pd
# numpy
import numpy as np

TEST_PATH='../data/matrix4/normal/TEST_OK_csic2010.csv'
# TEST_PATH='../data/matrix4/normal/TEST_OK_fwaf.csv'
# TEST_PATH='../data/matrix4/normal/TEST_OK_httpParams.csv'

MODEL_PATH = 'trained_model_2023-06-16_19-28-03.h5'

dataTest = pd.read_csv(TEST_PATH)
dataTest = dataTest.to_numpy()
np.random.shuffle(dataTest)

# print(type(dataset))

state_size = dataTest.shape[1] - 1  # column in dataset exculde label

# load the model
loaded_model = keras.models.load_model(MODEL_PATH,custom_objects={'my_loss_fn':DeepQLearning.my_loss_fn})

TN=0
FN=0
TP=0
FP=0

accurancy=0
precision=0
F1_score=0
recall=0

# create the environment, here you need to keep render_mode='rgb_array' since otherwise it will not generate the movie
# reset the environment
for row in dataTest:

    state = row[:-1]
    # state = state.reshape(1,state_size)
    state = np.reshape(state, [1, state_size])
    state = np.array(state, dtype=np.float32)
    # since the initial state is not a terminal state, set this flag to false
    # get the Q-value (1 by 2 vector)
    Qvalues=loaded_model.predict(state)
    # select the action that gives the max Qvalue
    action=np.random.choice(np.where(Qvalues[0,:]==np.max(Qvalues[0,:]))[0])
    label = row[-1]
    # if you want random actions for comparison
    #action = env.action_space.sample()
    # apply the action

    if label==1 and action==1:
        TP +=1
        print("TP")
    elif label==0 and action==0:
        TN +=1
    elif label==1 and action==0:
        FP +=1
    elif label==0 and action==1:
        FN +=1
        print("FN")

    # sum the rewards
    # print(f"Label: {label}, Action {action}")

print('Dataset records: %s' %len(dataTest))
print("_______________")
print("TP: ",TP)
print("TN: ",TN)
print("FP: ",FP)
print("FN: ",FN)
print("_______________")

accurancy = (TP + TN) / (TP + TN + FP + FN)
precision = TP / (TP + FP)
recall = TP / (TP + FN)
F1_score = 2 * (precision * recall) / (precision + recall)

print("accurancy: ",accurancy)
print("precision: ",precision)
print("recall: ",recall)
print("F1_score: ",F1_score)
print("_______________")

print(MODEL_PATH)
print(TEST_PATH)
