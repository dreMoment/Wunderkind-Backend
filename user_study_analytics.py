import csv
import pandas as pd

csv_file = 'user_study_tasks.csv' 
data = pd.read_csv(csv_file)

# Group data by 'user_id' for calculations
stats = data.groupby('child_id')['time_taken']
# Calculate mean task completion time and count of tasks per user
results = stats.agg(['mean', 'count'])
results.rename(columns={'mean': 'mean_completion_time(min)', 'count': 'task_count'}, inplace=True)

results = results[results['task_count'] > 0]

print(results)

print(results['mean_completion_time(min)'].mean())
print(results['task_count'].mean())

###
stats = data.groupby(['child_id','done_date'])['time_taken']
results = stats.agg(['mean', 'count'])
results.rename(columns={'mean': 'mean_completion_time_per_day(min)', 'count': 'task_count_per_day'}, inplace=True)
print(results)
print(results['mean_completion_time_per_day(min)'].mean())
print(results['task_count_per_day'].mean())



