import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
import pickle
from sklearn.preprocessing import OneHotEncoder


from sklearn.neural_network import MLPRegressor
import torch
from app.models.child import Child
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import app.config as config
from sqlalchemy.ext.declarative import declarative_base


MAX_CATS = 20

#For PScores
users = pd.read_csv('dummyp.csv')
y = users['pscore'].to_numpy()
x = users[['timeSpentOnTasks', 'benchmarktimes', 'taskCategories','catWeightsNormalized']]

for col in x.columns:
    x[col] = x[col].apply(lambda x: np.fromstring(x[1:-1], sep=','))
x = x.to_numpy()

dataset = []
#all data entries (timeSpentOnTasks, benchmarktimes, taskCategories, catWeightsNormalized)
for i in range(x.shape[0]):
#for i in range(1):
    #print(x[i])
    numTasks = len(x[i][0])
    tasks = np.array([])
    for j in range(numTasks):
        timespent = x[i][0][j]
        benchmark = x[i][1][j]
        
        taskCategory = x[i][2][j]
        encodedTaskCategory = np.zeros(MAX_CATS)
        encodedTaskCategory[int(taskCategory)] = 1

        catWeight = x[i][3][int(taskCategory)]
        #print(np.array([timespent, benchmark, taskCategory, catWeight]))
        
        tasks = np.append(tasks, np.array([timespent]))
        tasks = np.append(tasks, np.array([benchmark]))
        tasks = np.append(tasks, encodedTaskCategory)
        tasks = np.append(tasks, np.array([catWeight]))
        
    dataset = dataset + [tasks]


max = 0
for i in range(len(dataset)):
    if len(dataset[i]) > max:
        max = len(dataset[i])

for i in range(len(dataset)):
    dataset[i] = np.pad(dataset[i], (0, max - len(dataset[i])), 'constant', constant_values=(-1))

np_dataset = np.array(dataset)


# Training the model
x_train, x_test, y_train, y_test = train_test_split(np_dataset, y, test_size=0.3)

model = MLPRegressor(hidden_layer_sizes=(128, 16), learning_rate='adaptive', verbose=True, max_iter=500, n_iter_no_change=100) 
model.fit(x_train, y_train)
print(model.score(x_test, y_test))
 
pickle.dump(model, open('modelp.pkl', 'wb'))

    

