

from flask import Blueprint, json, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
import numpy as np
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from app.models.answer import Answer
import app.dummy_data_h
import app.routes.history_routes as history_routes



ml_bp = Blueprint('ml_bp', __name__)

modelP = pickle.load(open('app/modelp.pkl', 'rb')) # Load the trained model


@ml_bp.route('/generate_indiv_synth_data/<int:childid>/<float:readingtime>/<float:physicalactivitytime>)', methods=['POST'])
def generateIndivSynthData(childid, idealreadingtime, idealphysicalactivitytime):

    answers = Answer.query.filter_by(child_id=childid, question_id=1).all()
    answer_list = [answer.to_dict() for answer in answers]

    assessment_datapoints = []

    for answer in answer_list:
        print(answer)
        #get screen time, activity time, reading time from answer date
        entry = (history_routes.get_data_for_date(childid, answer['answer_date'])[0].json)['entry']
        print(entry)
        
        screentime = entry['screen_time']
        activitytime = entry['physical_activity']
        readingtime = entry['reading_time']

        question_hscore = (answer['rating']+1) * 25

        #is happy answer 3 or 0?
        assessment_datapoints.append([screentime, activitytime, readingtime, question_hscore])
    print(len(assessment_datapoints))



    dummy_data_h.generate_data(childid, idealreadingtime, idealphysicalactivitytime, assessment_datapoints)


@ml_bp.route('/train_indiv_model/<int:childid>)', methods=['POST'])
def trainIndivModel(childid):
    #Load data
    dataset = pd.read_csv('dummyh_'+str(childid)+'.csv')
    y = dataset['hscore']
    dataset.drop(columns='hscore', inplace=True)
    x = dataset[['screentime', 'activitytime', 'readingtime']]

    # Training the model
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    model = MLPRegressor(hidden_layer_sizes=(10, 5), verbose=True, max_iter=300, tol=1e-4, n_iter_no_change=100, random_state=10)
    model.fit(x_train, y_train)
    print(model.score(x_test, y_test))
    print("Model trained successfully!")

    pickle.dump(model, open('modelh_'+str(childid)+'.pkl', 'wb'))

 


@ml_bp.route('/predict_hscore/<int:childid>', methods=['POST'])
def predictHScore(childid):
    screentime = request.json['screentime']
    activitytime = request.json['activitytime']
    readingtime = request.json['readingtime']
    idealreadingtime = request.json['idealreadingtime']
    idealactivitytime = request.json['idealactivitytime']

    #print("Predicting Happiness Score for child: ", childid)
    #print("Screen Time: ", screentime)
    #print("Activity Time: ", activitytime)
    #print("Reading Time: ", readingtime)

    #if inidividual model does not exist, generate dummy data and train model
    try:
        modelH = pickle.load(open('modelh_'+str(childid)+'.pkl', 'rb'))
    except FileNotFoundError:
        generateIndivSynthData(childid, idealreadingtime, idealactivitytime)
        trainIndivModel(childid)
        modelH = pickle.load(open('modelh_'+str(childid)+'.pkl', 'rb'))

    if childid == 0:
        print("General model selected")
    else:
        print("Individual model selected")

    df = pd.DataFrame({'screentime':[screentime], 'activitytime':[activitytime], 'readingtime':[readingtime]})
    prediction = int(modelH.predict(df)) # Make a prediction
    print("Predicted Happiness Score: ", prediction)
    return jsonify({"msg": "Pedicted Happiness Score", "score":prediction})


@ml_bp.route('/predict_pscore/', methods=['POST'])
def predictPScore():
    timespentOnTasks = request.json['timespentontasks']
    benchmarktimes = request.json['benchmarktimes']
    taskCategories = request.json['taskcategories']
    catWeightsNormalized = request.json['catweightsnormalized']
    numTasks = len(timespentOnTasks)

    timespentOnTasks = [element/60 for element in timespentOnTasks] 
    benchmarktimes = [element/60 for element in benchmarktimes] 

    tasks = np.array([])
    for j in range(numTasks):
        timespent = timespentOnTasks[j]
        benchmark = benchmarktimes[j]
        taskCategory = taskCategories[j]
        encodedTaskCategory = np.zeros(20)
        encodedTaskCategory[int(taskCategory)] = 1

        catWeight = catWeightsNormalized[int(taskCategory)]
        #print(np.array([timespent, benchmark, taskCategory, catWeight]))
        
        tasks = np.append(tasks, np.array([timespent]))
        tasks = np.append(tasks, np.array([benchmark]))
        tasks = np.append(tasks, encodedTaskCategory)
        tasks = np.append(tasks, np.array([catWeight]))
        #print(tasks)

    #print(tasks)

    tasks = np.pad(tasks, (0, 460 - len(tasks)), 'constant', constant_values=(-1))

    prediction = int(modelP.predict([tasks])) # Make a prediction
    return jsonify({"msg": "Pedicted Performance Score", "score":prediction})


@ml_bp.route('/get_problem_area/<int:childid>', methods=['POST'])
def getProblemArea(childid):
    readingtime = request.json['readingtime']
    activitytime = request.json['activitytime']
    screentime = request.json['screentime']

    try:
        modelH = pickle.load(open('modelh_'+str(childid)+'.pkl', 'rb'))
    except FileNotFoundError:
        print("Individual model not found, choosing general model")
        modelH = pickle.load(open('modelh_0.pkl', 'rb'))

    #find the area which will improve the happiness score the most
    maxDiff = 0
    maxIndex = 2
    tmp = 0
        
    df = pd.DataFrame({'screentime':[screentime], 'activitytime':[activitytime], 'readingtime':[readingtime]})
    pred_before = int(modelH.predict(df))
    print("Initial prediction: ", pred_before)

    for i in range(3):
        print("Checking index: ", i)
        outOfBouds = False
        if i == 0:
            if screentime == 0:
                outOfBouds = True
            else:
                screentime-=0.1
        elif i == 1:
            activitytime+=0.1
        else:
            readingtime+=0.1 

        df = pd.DataFrame({'screentime':[screentime], 'activitytime':[activitytime], 'readingtime':[readingtime]})
        prediction_after = int(modelH.predict(df))
        print("Prediction after change: ", prediction_after)


        if i == 0:
            if not outOfBouds:
                screentime+=0.1
        elif i == 1:
            activitytime-=0.1
        else:
            readingtime-=0.1



        if prediction_after - pred_before > maxDiff and not outOfBouds:
            print("New max index: ", i)
            maxDiff = prediction_after - pred_before
            maxIndex = i



    return jsonify({"msg": "Problem area is:", "value":maxIndex})
