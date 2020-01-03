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

row=['power','time','gas','pressure','ratio']
with open('ml_file.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)
        writer.writerows(zip(power,time,gas,pressure))