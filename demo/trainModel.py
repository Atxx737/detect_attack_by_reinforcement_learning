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

# TRAIN_PATH='../data/matrix1/normal/train-normal.csv'
# TRAIN_PATH='/home/yoyoo/KLTN/detect_attack_by_reinforcement_learning/data/matrix1/normal/train-normal.csv'
TRAIN_PATH='../data/matrix2/normal/train.csv'


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

stateDimension = 38  # column in dataset exculde label
actionDimension = 2
# episodes = data.shape[0]

# print(mini_batch)
# create an object
LearningQDeep = DeepQLearning(dataset,stateDimension,actionDimension,gamma,epsilon)
# run the learning process
LearningQDeep.trainingEpisodes()
# get the obtained rewards in every episode
LearningQDeep.sumRewardsEpisode

#  summarize the model
LearningQDeep.mainNetwork.summary()
# save the model, this is important, since it takes long time to train the model 
# and we will need model in another file to visualize the trained model performance
LearningQDeep.mainNetwork.save("trained_model_temp.h5")

