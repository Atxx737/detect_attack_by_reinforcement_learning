import keras
# import the class
from functions_final import DeepQLearning
import pandas as pd
# numpy
import numpy as np
import random
import time


# MODEL_PATH = 'trained_model_2023-06-20_09-52-23.h5'
# MODEL_PATH = 'model-20-06/trained_model_in_episode_9.h5'
# MODEL_PATH = 'model-20-06/trained_model_2023-06-20_09-52-23.h5'
# MODEL_PATH = 'trained_model_in_episode_1.h5'
MODEL_PATH = 'model-OK/main_model_in_episode_12.h5'


LIST_PATH_TEST = ['../data/matrix5/normal/TEST_OK_csic2010.csv', '../data/matrix5/normal/TEST_OK_fwaf.csv', '../data/matrix5/normal/TEST_OK_httpParams.csv','../data/matrix5/normal/TEST_OK_ECML.csv' ]

TEST_PATH = '../data/matrix5/normal/TEST_TIME.csv'

def sample_test(csv_test):
    row = pd.read_csv(csv_test)
    random_sample = row.sample(n=100)

    random_sample.to_csv(TEST_PATH,index=False)
    return pd

def test(TEST_PATH):
    dataTest = pd.read_csv(TEST_PATH)
    dataTest = dataTest.to_numpy()
    np.random.shuffle(dataTest)

    # print(type(dataset))

    state_size = dataTest.shape[1] - 1  # column in dataset exculde label

    # load the model
    loaded_model = keras.models.load_model(MODEL_PATH,custom_objects={'my_loss_fn':DeepQLearning.my_loss_fn})

   
    time_list = []

    # create the environment, here you need to keep render_mode='rgb_array' since otherwise it will not generate the movie
    # reset the environment
    for row in dataTest:

        state = row[:-1]
        # state = state.reshape(1,state_size)
        state = np.reshape(state, [1, state_size])
        state = np.array(state, dtype=np.float32)/255.0
        # since the initial state is not a terminal state, set this flag to false
        # get the Q-value (1 by 2 vector)
        start_time = time.time()
        Qvalues=loaded_model.predict(state)
        # select the action that gives the max Qvalue
        action=np.random.choice(np.where(Qvalues[0,:]==np.max(Qvalues[0,:]))[0])
        end_time = time.time()
        execution_time = end_time - start_time
        time_list.append(execution_time)
        
    print('Dataset records: %s' %len(dataTest))
   
    sum_values = sum(time_list)
    count_values = len(time_list)

    print("Average time predict:", sum_values / count_values)
    print("Maximum time predict:", max(time_list))
    print("Minimum time predict:", min(time_list))

    print(MODEL_PATH)
    # print(TEST_PATH)

for path in LIST_PATH_TEST:
    print(path)
    sample_test(path)
    test(TEST_PATH)
    print("---------------")