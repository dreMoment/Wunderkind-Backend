import random
import csv
import matplotlib.pyplot as plt

MAXTASKS=20

def pad_with_nan(lst, n=MAXTASKS):
  return lst[:n] +[-1.0]* (n-len(lst))

data = []


for i in range(50000):

  day = random.randint(1, 28)
  month = random.randint(1, 12)
  year = 2023
  date_str = f"{year}-{month:02d}-{day:02d}"


  #Generate random inputs in hours
  numTasks = round(random.uniform(0, MAXTASKS), 0)

  while(True):
    timeSpentOnTasks = [round(random.uniform(0.1, 3),1) for i in range(int(numTasks))]

    #select a random number of tasks to be 0
    numZeroTasks = random.randint(0, int(numTasks))
    for i in range(numZeroTasks):
      timeSpentOnTasks[i] = 0

    benchmarktimes = [round(random.uniform(0.1, 3),1) for i in range(int(numTasks))]
    totalTime = sum(timeSpentOnTasks)
    totalTimeBenchmark = sum(benchmarktimes)
    if totalTime<=24 and totalTimeBenchmark<=24:
      break

  numCategories = round(random.uniform(1, numTasks)) if numTasks > 0 else 0
  catWeights = [random.uniform(0, 1) for i in range(int(numCategories))]
  taskCategories = [random.randint(0, numCategories-1) for i in range(int(numTasks))]

  #filter out categories that are not used
  catWeights = [x if i in taskCategories else 0 for i, x in enumerate(catWeights) ]

  catWeightsNormalized = [round(w/sum(catWeights),2) for w in catWeights]

  #print("numTasks", numTasks)
  #print("timeSpentOnTasks", timeSpentOnTasks)
  #print("benchmarktimes", benchmarktimes)
  #print("totalTime", totalTime)
  #print("numCategories", numCategories)
  #print("catWeights", catWeights)
  #print("catWeightsNormalized", catWeightsNormalized)
  #print("taskCategories", taskCategories)
  #print("sum", sum(catWeightsNormalized))
  

  assert round(sum(catWeightsNormalized),1)==1 or numCategories == 0
  assert not (len(catWeightsNormalized)>0 and max(catWeightsNormalized) == 0 and numTasks > 0)


  score = 0
  for i in range(int(numCategories)):
    if i in taskCategories and sum([1 if timeSpentOnTasks[j]>0 else 0 for j in range(int(numTasks)) if taskCategories[j] == i]) > 0: 
      assert (sum([1 if timeSpentOnTasks[j]>0 else 0 for j in range(int(numTasks)) if taskCategories[j] == i]) / len([1 for j in range(int(numTasks)) if taskCategories[j] == i])) <= 1
      score += catWeightsNormalized[i] * (sum([1 if timeSpentOnTasks[j]>0 else 0 for j in range(int(numTasks)) if taskCategories[j] == i])/ len([1 for j in range(int(numTasks)) if taskCategories[j] == i])) * min(1,sum([benchmarktimes[j] for j in range(int(numTasks)) if taskCategories[j] == i])/sum([timeSpentOnTasks[j] for j in range(int(numTasks)) if taskCategories[j] == i]))
  #print(score)

  #assert len(timeSpentOnTasks) == len(taskCategories) == len(catWeightsNormalized) == len(benchmarktimes) == MAXTASKS

  #performance_score = max(1, min(100, int(score*100) + round(random.uniform(-5, 5),0)))
  performance_score = max(1, min(100, int(score*100) ))
  data.append([date_str, timeSpentOnTasks, benchmarktimes, taskCategories, catWeightsNormalized, performance_score])
  
  #if performance_score <= 5:
  #  print(numTasks, totalTime, performance_score)
#fig = plt.figure(figsize=(10,6))
#ax = fig.add_subplot(111,projection='3d')
#ax.scatter([row[1] for row in data],[row[2] for row in data],[row[3] for row in data], c='b')
#ax.view_init(elev=15, azim=60)
#plt.show()
  


with open('dummyp.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(['date', 'timeSpentOnTasks','benchmarktimes', 'taskCategories','catWeightsNormalized','pscore'])
  writer.writerows(data)

print("Data generated successfully!")
