import pandas as pd
import datetime

from functions_final import DeepQLearning

# Get the current date and time
current_datetime = datetime.datetime.now()
# Format the date and time as a string
date_string = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

# TRAIN_PATH='../data/matrix1/normal/train-normal.csv'
# TRAIN_PATH='/home/yoyoo/KLTN/detect_attack_by_reinforcement_learning/data/matrix1/normal/train-normal.csv'
# TRAIN_PATH='../data/matrix2/normal/train.csv'
TRAIN_PATH='../data/matrix4/normal/train.csv'


dataset = pd.read_csv(TRAIN_PATH)
dataset = dataset.to_numpy()

# select the parameters
gamma=1

# probability parameter for the epsilon-greedy approach
epsilon=0.1

# number of training episodes
numberEpisodes=10

stateDimension = dataset.shape[1] - 1  # column in dataset exculde label
actionDimension = 2

# create an object
LearningQDeep = DeepQLearning(dataset,stateDimension,actionDimension,gamma,epsilon,numberEpisodes)

# run the learning process
LearningQDeep.trainingEpisodes()

# get the obtained rewards in every episode
LearningQDeep.sumRewardsEpisode

#  summarize the model
LearningQDeep.mainNetwork.summary()
# save the model, this is important, since it takes long time to train the model 
# and we will need model in another file to visualize the trained model performance
LearningQDeep.mainNetwork.save(f"trained_model_{date_string}.h5")