# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 09:52:09 2025

@author: erikv
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime

import weakest_dsp_engineer as wde

import pandas as pd

MOVEMENT_GOALS = {"overhead press" : 135, "pause bench" : 225, "pull up" : 45,
                  "chin up" : 45, "pendlay row" : 225}

def main():
    data_file_name = "ericdvet.csv"
    df = pd.read_csv(data_file_name)
    movement = "overhead press"
    
    unique_dates, tonnage, average_weights, max_weights = wde.get_metrics(
        df, movement)
    
    from_date = datetime(2025, 6, 1)
    to_date = datetime(2026, 1, 1)
    
    wde.plot_progress(unique_dates, tonnage, average_weights, from_date, to_date)
    wde.plot_weight_trend(unique_dates, max_weights, movement, MOVEMENT_GOALS)
    
if __name__ == "__main__":
    main()