import random
import csv

ideal_physical_activity = 1.25
ideal_reading_time = 0.5


  
def generate_data(childId, ideal_physical_activity, ideal_reading_time, assessment_datapoints):
  data = []

  print('ideal_physical_activity:', ideal_physical_activity)
  print('ideal_reading_time:', ideal_reading_time)

  if ideal_physical_activity == 0:
    ideal_physical_activity = 0.1
  if ideal_reading_time == 0:
    ideal_reading_time = 0.1
  

  for i in range(100000):

    #Generate random inputs in hours
    screen_time = round(random.uniform(0, 10), 1)
    physical_activity = round(random.uniform(0, 10), 1)
    reading_time = round(random.uniform(0, 10), 1)


    # Calculate the happiness score
    score = calculate_hscore(ideal_physical_activity, ideal_reading_time, screen_time, physical_activity, reading_time)
    
    happiness_score = max(1, min(100, int(score*100) + round(random.uniform(-2, 2),0)))
    data.append([screen_time, physical_activity, reading_time, happiness_score])


  for j in range(len(assessment_datapoints)):
    data = list(filter(lambda x: not (x[0] == assessment_datapoints[j][0] and x[1] == assessment_datapoints[j][1] and x[2] == assessment_datapoints[j][2]) , data))
    for _ in range(10000):
      data.append(assessment_datapoints[j])

    
  with open('dummyh_'+str(childId)+'.csv', 'w', newline='') as csvfile:
  #with open('dummyh_0_without_assessment.csv', 'w', newline='') as csvfile:
  #with open('dummyh_0_with_assessment.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['screentime', 'activitytime', 'readingtime', 'hscore'])
    writer.writerows(data)

    
  print("Data generated successfully!")

def calculate_hscore(ideal_physical_activity, ideal_reading_time, screen_time, physical_activity, reading_time):
  screenW = 0.4
  ideal_screen_time = 2.0

  # Normalize the time inputs
  normalized_screen_time =  0.2 * (screen_time/ideal_screen_time) if screen_time <= ideal_screen_time else -(screen_time/ideal_screen_time) + 1
  # based on an ideal physical activity time
  normalized_physical_activity = min(0.9, physical_activity / ideal_physical_activity) + (0.1*(physical_activity / ideal_physical_activity) if physical_activity > ideal_physical_activity else 0)
  # based on an ideal reading time
  normalized_reading_time = min(0.9, reading_time / ideal_reading_time) + (0.1*(reading_time / ideal_reading_time) if reading_time > ideal_reading_time else 0)

  # Calculate the happiness score
  score = (screenW * normalized_screen_time) + (0.5 * normalized_physical_activity) + (0.5 * normalized_reading_time)

  return score

datapoints = []
datapoints = [[4, 0, 0, 25], [3, 0, 0, 50], [0, 0, 0, 75]]
ideal_physical_activity = ideal_physical_activity * 0.7 + 0 * 0.3 #0.25 is the mean of the activity time in the datapoints
ideal_reading_time = ideal_reading_time * 0.7 + 0 * 0.3 #0.25 is the mean of the reading time in the datapoints
generate_data(0, ideal_physical_activity, ideal_reading_time,datapoints)

