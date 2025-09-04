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

# This test harness is likely outdated
def main():
    data_file_name = "ericdvet.csv"
    df = pd.read_csv(data_file_name)
    movement = "overhead press"
    
    unique_dates, tonnage, average_weights, max_weights = get_metrics(
        df, movement)
    
    from_date = datetime(2025, 6, 1)
    to_date = datetime(2026, 1, 1)
    
    plot_progress(unique_dates, tonnage, average_weights, from_date, to_date)
    plot_weight_trend(unique_dates, max_weights, movement, MOVEMENT_GOALS)
    
    
    
def get_metrics(df : pd.DataFrame, movement : str):
    """
    Unpack various information from the data log DataFrame for later analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Data log.
    movement : str
        Movement name.

    Returns
    -------
    unique_dates : list
        List of unique dates.
    tonnage : list
        Tonnage for unique_dates. Tonnage is the weight x reps summed for each 
        set.
    average_weights : list
       Average weights for unique_dates.
    max_weights : list
        Maximum weight lifted on unique_dates.

    """
    isolated_df = df[df["exercise"] == movement]
    
    format_code = "%Y-%m-%d"
    dates = isolated_df["date"].values
    for i, date in enumerate(dates):
        dates[i] = datetime.strptime(date, format_code)

    weights = isolated_df["weight"].values
    reps = isolated_df["reps"].values
        
    unique_dates = []
    average_weights = []
    tonnage = []
    max_weights = []
    
    temp_weights = []
    temp_reps = []
    
    for i, date in enumerate(dates):
        # print(date)
        
        if i == 0:
            unique_dates.append(date)
            pass
        
        if unique_dates[-1] == date:
            pass
        else:
            unique_dates.append(date)
            
            tonnage.append(0)
            for weight, rep_count in zip(temp_weights, temp_reps):
                tonnage[-1] = tonnage[-1] + weight * rep_count
                
            average_weights.append(sum(temp_weights) / len(temp_weights))
            max_weights.append(max(temp_weights))
            
            temp_weights = []
            temp_reps = []
        
        temp_weights.append(weights[i])
        temp_reps.append(reps[i])
        
    tonnage.append(0)
    for weight, rep_count in zip(temp_weights, temp_reps):
        tonnage[-1] = tonnage[-1] + weight * rep_count
    
    average_weights.append(sum(temp_weights) / len(temp_weights))
    max_weights.append(max(temp_weights))
    
    return unique_dates, tonnage, average_weights, max_weights
    
def plot_progress(unique_dates : list, tonnage : list, average_weights : list,
                  from_date : datetime = datetime(2020, 1, 1), 
                  to_date : datetime = None):
    """
    Plot the progress as tonnage and average weights from a start to end date.

    Parameters
    ----------
    unique_dates : list
        List of unique dates.
    tonnage : list
        Tonnage for unique_dates. Tonnage is the weight x reps summed for each 
        set.
    average_weights : list
        Average weights for unique_dates.
    from_date : datetime, optional
        Date from which to start the plot. The default is datetime(2020, 1, 1).
    to_date : datetime, optional
        Date to which to end the plot. The default is None.

    Returns
    -------
    None.

    """
    
    for i, date in enumerate(unique_dates):
        if date > from_date:
            starting_idx = i
            break
    
    ending_idx = None
    for i, date in enumerate(unique_dates):
        if date > to_date:
            ending_idx = i
            break
        
    fig, ax = plt.subplots(1,1)
    
    locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    
    ax.plot(unique_dates[starting_idx:ending_idx], 
            tonnage[starting_idx:ending_idx], color='xkcd:teal')
    ax2 = ax.twinx()
    ax2.plot(unique_dates[starting_idx:ending_idx], 
             average_weights[starting_idx:ending_idx], color='green')
    plt.grid(True)
    plt.title("Average Weights and Tonnage v. Date")
    plt.show()
    
    # plot_weight_trend(dates, weights, movement, MOVEMENT_GOALS)
    
def plot_weight_trend(unique_dates : list, max_weights : list, movement : str, 
                      MOVEMENT_GOALS : dict):
    """
    Plot the overall change in maximum weights lifted across unique_dates.

    Parameters
    ----------
    unique_dates : list
        List of unique dates.
    max_weights : list
        Maximum weight lifted on unique_dates.
    movement : str
        Movement name.
    MOVEMENT_GOALS : dict
        Movement goals in the form: {"movement name" : 135}

    Returns
    -------
    None.

    """
    
    movement_goal = MOVEMENT_GOALS.get(movement)
    
    fig, ax = plt.subplots(1,1)
    
    locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    
    ax.plot(unique_dates, max_weights, color='xkcd:teal', label=movement)
    plt.ylim((min(max_weights)-10, movement_goal+10))
    plt.axhline(movement_goal, color='red',  label="goal")
    plt.grid(True)
    plt.legend()
    plt.show()
    
    
if __name__ == "__main__":
    main()
