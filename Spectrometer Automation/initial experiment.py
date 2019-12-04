#!/usr/bin/env python
# coding: utf-8

##Create the initial random dataset

import numpy as np
import csv
power=[]
time=[]
pressure=[]
gas=[]
for x in range(20):
    power.append(np.random.randint(10,5555))
    time.append(np.random.randint(500,20210))
    gas.append("Argon")
    pressure.append(np.random.randint(0,100))

row=['Power','Time','Gas','Pressure','Ratio']
with open('dataset-2.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)
        writer.writerows(zip(power,time,gas,pressure))

#File 2
#This will work for setting D to G ratio for 1st 20 random values

import pandas as pd
def update_ratio(k,value):
    df = pd.read_csv("dataset-2.csv")
    df.set_value(k, "Ratio", value)
    df.to_csv("dataset-2.csv", index=False)

for i in range(22):
    if i==15:
        print("Stop Running, Initial Experiment Done")
        break
    update_ratio(i,i*i)
