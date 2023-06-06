import numpy as np
import random
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import RMSprop
from collections import deque 
from tensorflow import gather_nd
from tensorflow.keras.losses import mean_squared_error 
import pandas as pd
from functions_final import DeepQLearning

TRAIN_PATH='../data/matrix1/normal/train-normal.csv'
dataset = pd.read_csv(TRAIN_PATH)
# print(type(dataset))

# select the parameters
gamma=1
# probability parameter for the epsilon-greedy approach
epsilon=0.1
# number of training episodes
# NOTE HERE THAT AFTER CERTAIN NUMBERS OF EPISODES, WHEN THE PARAMTERS ARE LEARNED
# THE EPISODE WILL BE LONG, AT THAT POINT YOU CAN STOP THE TRAINING PROCESS BY PRESSING CTRL+C
# DO NOT WORRY, THE PARAMETERS WILL BE MEMORIZED
# numberEpisodes=100

state_size = 38  # column in dataset exculde label
action_size = 2
batch_size = 100 # mô hình cập nhật sau khi train 100 dữ liệu
# episodes = data.shape[0]

for i in range(0,len(dataset),batch_size):

    mini_batch = dataset[i : i + batch_size]
    # print(mini_batch)
    # create an object
    LearningQDeep = DeepQLearning(mini_batch,state_size,action_size,gamma,epsilon,batch_size)
    # run the learning process
    LearningQDeep.trainingEpisodes()
    # get the obtained rewards in every episode
    LearningQDeep.sumRewardsEpisode
    #  summarize the model
    LearningQDeep.mainNetwork.summary()
    # save the model, this is important, since it takes long time to train the model 
    # and we will need model in another file to visualize the trained model performance
    LearningQDeep.mainNetwork.save("trained_model_temp.h5")

    print("done",i,"in dataset ",len(dataset))
