import numpy as np
import pandas as pd


SIZE = 1000000

#activity days per week, screen hours per day, reading, hscore
mean = [3.81, 3.055, 0.5, 7.95]

# Default correlation coefficient
rho = 0.75

#Original standard deviations
physicalActivitySD = 2.26
screenTimeSD = 1.67
hscoreSD = 2.00


#ASSUMED Reading time standard deviation
readingTimeSD = 2.26


cov = [[physicalActivitySD**2, 0, 0, rho * physicalActivitySD * hscoreSD ],
       [0, screenTimeSD**2, 0, -rho * screenTimeSD * hscoreSD],
       [0, 0, readingTimeSD**2, rho * readingTimeSD * hscoreSD],
       [rho * physicalActivitySD * hscoreSD , -rho * screenTimeSD * hscoreSD, rho * readingTimeSD * hscoreSD, hscoreSD**2]]


# Generate the dataset
data = np.random.multivariate_normal(mean, cov, SIZE)


df = pd.DataFrame(data, columns=['activitytime', 'screentime', 'readingtime' ,'hscore'])


# Convert the score to a percentage (0-100)
df['hscore'] = df['hscore'].apply(lambda x: x*10)

# turn activity times from days per week to hours per day
df['activitytime'] = df['activitytime'] / 7


# Some constraints making the hscore more realistic
df['hscore'] = df['hscore'].astype(int)-20 # to cover more of the total hscore range
df = df[df['hscore'] >= 1]
df = df[df['hscore'] <= 100]


# Parameters cannot be negative
df = df[df['activitytime'] >= 0]
df = df[df['screentime'] >= 0]
df = df[df['readingtime'] >= 0]





# Some constraints making the dataset more realistic
df = df[df['activitytime'] + df['readingtime'] + df['screentime'] <= 16]
df = df[df['screentime'] <= 6]
df = df[df['activitytime'] <= 6]
df = df[df['readingtime'] <= 6]

df = round(df, 1)

df.to_csv('dataset.csv', index=False)

print(df.head())


### PLOTTING ###

import matplotlib.pyplot as plt
import seaborn as sns

##Plot Realtionships between paramteters and Happiness Score

#df.sort_values(by=['screentime', 'readingtime'], inplace=True)
#
#fig, ax = plt.subplots(figsize=(10, 6))
#sns.scatterplot(x='screentime', y='hscore', hue='readingtime', palette='viridis', size='activitytime', sizes=(20,200),legend=False, data=df, ax=ax)
#sns.lineplot(x='screentime', y='hscore', data=df, color='orange', sort=False, ax=ax)
#
#norm = plt.Normalize(df['readingtime'].min(), df['readingtime'].max())
#sm = plt.cm.ScalarMappable(cmap="viridis", norm=norm)
#sm.set_array([])
#
#cbar = plt.colorbar(sm, ax=ax)
#cbar.set_label('Reading Time')
#
#plt.xlabel('Screen Time')
#plt.ylabel('Happiness Score')
#plt.title('Screen Time vs Activity Time vs Reading Time vs Happiness Score')
#plt.show()



#Plot Histogram of distribution of parameters

plt.figure(figsize=(10, 6))
sns.histplot(df['hscore'], kde=False, bins=111)
plt.title('Distribution of Happiness Score')
plt.xlabel('Happiness Score')
plt.ylabel('Frequency')
plt.show()




