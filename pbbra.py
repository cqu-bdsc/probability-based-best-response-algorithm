"""
author: neardws
data: 7/27/2020

Input:
1. Tasks
task set (including the required transmission rate and required SINR)

2. Players
probability of changing action

3. Communication
channel resource
gaussian noise
symbol error rate
max power
min transmission rate
path loss

Output:
cycles
strategy
profits

"""
from config import settings
import random
import pandas as pd
import numpy as np


def initialize(fog_node_id, time, channel_resource):
    probability = random.random()
    print(probability)
    task_df = pd.read_csv(settings.task_csv_name)
    task_df = task_df[task_df["fog_id"] == fog_node_id]
    task_df = task_df[task_df["time"] == time]
    print(task_df.head(10))
    task_num = len(task_df)
    strategy = np.zeros([channel_resource, task_num], dtype= int)
    print(strategy)

if __name__ == '__main__':
    initialize(fog_node_id=1, time=1, channel_resource=settings.channel_resource)


