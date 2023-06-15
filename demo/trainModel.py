import pandas as pd
import datetime
import keras
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.losses import mean_squared_error 
from functions_final import DeepQLearning

# Get the current date and time
current_datetime = datetime.datetime.now()
# Format the date and time as a string
date_string = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

# TRAIN_PATH='../data/matrix1/normal/train-normal.csv'
# TRAIN_PATH='/home/yoyoo/KLTN/detect_attack_by_reinforcement_learning/data/matrix1/normal/train-normal.csv'
# TRAIN_PATH='../data/matrix2/normal/train.csv'
TRAIN_PATH='../data/matrix4/normal/train.csv'
MODEL_PATH = './model-15-06/trained_model_in_episode_4.h5'

dataset = pd.read_csv(TRAIN_PATH)
dataset = dataset.to_numpy()

# select the parameters
gamma=1

# probability parameter for the epsilon-greedy approach
epsilon=0.1

# number of training episodes
numberEpisodes=10
# numberEpisodes=5

stateDimension = dataset.shape[1] - 1  # column in dataset exculde label
actionDimension = 2

# create an object
LearningQDeep = DeepQLearning(dataset,stateDimension,actionDimension,gamma,epsilon,numberEpisodes)

# Load the saved model
model = keras.models.load_model(MODEL_PATH,custom_objects={'my_loss_fn':DeepQLearning.my_loss_fn})

# Assign the loaded model to the mainNetwork attribute of LearningQDeep
LearningQDeep.mainNetwork = model
LearningQDeep.targetNetwork = model

# Compile the model with the desired optimizer, loss, and metrics
model.compile(optimizer = RMSprop())

# run the learning process
LearningQDeep.trainingEpisodes()

# get the obtained rewards in every episode
LearningQDeep.sumRewardsEpisode

#  summarize the model
LearningQDeep.mainNetwork.summary()
# save the model, this is important, since it takes long time to train the model 
# and we will need model in another file to visualize the trained model performance
LearningQDeep.mainNetwork.save(f"trained_model_{date_string}.h5")

