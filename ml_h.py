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



for i in range(1):
    #users = pd.read_csv('dummyh_'+str(i)+'.csv')
    #users = pd.read_csv('dummyh_0_without_assessment.csv')
    users = pd.read_csv('dummyh_0_with_assessment.csv')

    
    y = users['hscore']
    users.drop(columns='hscore', inplace=True)
    x = users[['screentime', 'activitytime', 'readingtime']]

    # Training the model
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    model = MLPRegressor(hidden_layer_sizes=(8, 8), verbose=True, max_iter=300, tol=1e-4, n_iter_no_change=100)
    model.fit(x_train, y_train)
    print(model.score(x_test, y_test))

    #pickle.dump(model, open('modelh_'+str(i)+'.pkl', 'wb'))
    #pickle.dump(model, open('modelh_0_without_assessment.pkl', 'wb'))
    pickle.dump(model, open('modelh_0_with_assessment.pkl', 'wb'))
