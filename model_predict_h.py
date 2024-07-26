import pickle
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

model_default = pickle.load(open('modelh_0.pkl', 'rb')) # Load the trained model
model_without_assessment = pickle.load(open('modelh_0_without_assessment.pkl', 'rb')) # Load the trained model
model_with_assessment = pickle.load(open('modelh_0_with_assessment.pkl', 'rb')) # Load the trained model


screentime = np.arange(0, 5, 0.1).tolist()
readingtime = np.array([0]*50).tolist()
activitytime = np.array([0]*50).tolist()

#activitytime = [2.0]
#screentime = [0]
#readingtime = [3]

df = pd.DataFrame({'screentime':screentime, 'activitytime':activitytime, 'readingtime':readingtime})

predictions_default = model_default.predict(df).astype(int) # Make a prediction
predictions_without_assessment = model_without_assessment.predict(df).astype(int) # Make a prediction
predictions_with_assessment = model_with_assessment.predict(df).astype(int) # Make a prediction

for prediction in predictions_default:
    predictions_default[predictions_default == prediction] = max(1,min(100, prediction))
    #print(max(1,min(100, prediction)))

for prediction in predictions_without_assessment:
    predictions_without_assessment[predictions_without_assessment == prediction] = max(1,min(100, prediction))

for prediction in predictions_with_assessment:
    predictions_with_assessment[predictions_with_assessment == prediction] = max(1,min(100, prediction))

df['hscore_default'] = predictions_default
df['hscore_without_assessment'] = predictions_without_assessment
df['hscore_with_assessment'] = predictions_with_assessment

import matplotlib.pyplot as plt
import seaborn as sns


sns.lineplot(x='screentime', y='hscore_default', data=df)
sns.lineplot(x='screentime', y='hscore_without_assessment', data=df)
sns.lineplot(x='screentime', y='hscore_with_assessment', data=df)

legend_elements = [
    Line2D([0], [0], color='blue', lw=2, label='Default Model'),
    Line2D([0], [0], color='orange', lw=2, label='Individual Ideal Times'),
    Line2D([0], [0], color='green', lw=2, label='Individual Ideal Times with self reported Happiness'),
]

plt.legend(handles=legend_elements)

plt.scatter(3.0, 50, color='blue', s=50)
plt.scatter(0, 75, color='blue', s=50)
plt.scatter(4, 25, color='blue', s=50)

plt.xlabel('Screen Time')
plt.ylabel('Happiness Score')
plt.title('Screen Time vs Happiness Score')
plt.show()
