import pickle
import random
import numpy as np
import pandas as pd

model = pickle.load(open('modelp.pkl', 'rb')) # Load the trained model

def pad_with_nan(lst, n=20):
  return lst[:n] +[-1.0]* (n-len(lst))

timeSpentOnTasks = [[0]]

numTasks = 20
numCategories = 1
#benchmarkTasks = ([round(random.uniform(0.1,3),1) for i in range(numTasks)])
benchmarkTasks = [[0.5]]
taskCategories = ([random.randint(0, numCategories-1) for i in range(numTasks)])
catWeights = [1]


resdataset = []

for j in range(len(timeSpentOnTasks)):
    #print("number of samples", j,"/",len(timeSpentOnTasks))
    dataset = np.array([])
    for i in range(len(timeSpentOnTasks[j])):
        
        #print("number of tasks in sample", i, "/", len(timeSpentOnTasks[j]))
        
        encodedTaskCategory = np.zeros(20)
        encodedTaskCategory[int(taskCategories[i])] = 1
        dataset = np.append(dataset, [timeSpentOnTasks[j][i]])
        dataset = np.append(dataset, [benchmarkTasks[j][i]])
        dataset = np.append(dataset, encodedTaskCategory)
        dataset = np.append(dataset, catWeights[int(taskCategories[i])])
        #pad up to 460 elements
    
    dataset = np.append(dataset, np.zeros(460-len(dataset)))
    print(dataset)
    resdataset = resdataset + [dataset.tolist()]
     


predictions = model.predict(resdataset).astype(int) # Make a prediction

for prediction in predictions:
    print(max(1,min(100, prediction)))
