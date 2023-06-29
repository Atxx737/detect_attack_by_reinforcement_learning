import keras
# import the class
from functions_final import DeepQLearning
import pandas as pd
# numpy
import numpy as np

from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error
                             ,mean_absolute_error)
from sklearn import metrics
from tensorflow.keras.utils import to_categorical

TEST_PATH='../data2/TEST_OK_csic2010.csv'
# TEST_PATH='../data2/TEST_OK_fwaf.csv'
# TEST_PATH='../data2/TEST_OK_httpParams.csv'
# TEST_PATH='../data2/TEST_OK_ECML.csv'

MODEL_PATH = 'main_model_in_episode_12.h5'

dataTest = pd.read_csv(TEST_PATH)
dataTest = dataTest.to_numpy()
np.random.shuffle(dataTest)

# print(type(dataset))

state_size = dataTest.shape[1] - 1  # column in dataset exculde label

# load the model
loaded_model = keras.models.load_model(MODEL_PATH,custom_objects={'my_loss_fn':DeepQLearning.my_loss_fn})

y_true = []
y_pred = []

# create the environment, here you need to keep render_mode='rgb_array' since otherwise it will not generate the movie
# reset the environment
for row in dataTest:

    # (currentState,prob)=env.reset()
    state1 = row[:-1]
    state2 = state1.reshape(1,state_size)
    state = np.array(state2, dtype=np.float32)/255.0

    # since the initial state is not a terminal state, set this flag to false
    # get the Q-value (1 by 2 vector)
    Qvalues=loaded_model.predict(state)
    # select the action that gives the max Qvalue
    action=np.random.choice(np.where(Qvalues[0,:]==np.max(Qvalues[0,:]))[0])
    y_pred.append(action)

    label = row[-1]
    y_true.append(label)

    # sum the rewards
    # print("Label: %s, Action %s, Result %s" %(label, action, action==label))

y_true = np.array(y_true)
y_pred = np.array(y_pred)

# y_true = to_categorical(y_true)
# y_pred = to_categorical(y_pred)

accuracy = accuracy_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print('Dataset records: %s' %len(dataTest))
print("_______________")
print("confusion matrix")
print("----------------------------------------------")
print("accuracy: %.6f" %accuracy)
print("recall: %.6f" %recall)
print("precision: %.6f" %precision)
print("f1_score: %.6f" %f1)

cm = metrics.confusion_matrix(y_true, y_pred)
print("confusion matrix")
print("==============================================")
print(cm)
print("==============================================")

print(MODEL_PATH)
print(TEST_PATH)
