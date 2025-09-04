# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 22:13:54 2025

@author: ericdvet
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime

import weakest_dsp_engineer as wde

import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import matplotlib.units as munits
import matplotlib.pyplot as plt

MOVEMENT_GOALS = {"overhead press" : 135, "pause bench" : 225, "pull up" : 45,
                  "chin up" : 45, "pendlay row" : 225}

def main():
    data_file_name = "ericdvet.csv"
    df = pd.read_csv(data_file_name)
    
    movement = "pull up"
    
    movement_goal = MOVEMENT_GOALS.get(movement)
    isolated_df = df[df["exercise"] == movement]
    
    format_code = "%Y-%m-%d"
    dates = isolated_df["date"].values
    for i, date in enumerate(dates):
        dates[i] = datetime.strptime(date, format_code)
    
    weights = isolated_df["weight"].values
    reps = isolated_df["reps"].values
    
    plt.figure()
    plt.plot(dates, weights, color='xkcd:teal', label=movement)
    plt.ylim((min(weights)-10, movement_goal+10))
    plt.axhline(movement_goal, color='red',  label="goal")
    plt.grid(True)
    plt.legend()
    plt.show()
    
    
if __name__ == "__main__":
    main()
