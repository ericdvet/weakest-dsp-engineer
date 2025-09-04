# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 20:11:04 2025

@author: ericdvet
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime

import weakest_dsp_engineer as wde

def main():
    
    first_date = datetime.date(2025, 6, 23)
    last_date = datetime.date(2025, 8, 25)
    
    dates, labels = wde.program_mwf_ab(first_date, last_date)    
    path_to_data = "ericdvet.csv"
    
    for i, date in enumerate(dates):
        dates[i] = "/" + str(date) + ".csv"
        
    # Update the program cards with the data
    for entry in os.listdir("fill_out"):
        if entry[-4:] == ".csv":
            date = entry
            wde.update_data_from_program_card(program_card_dir = "fill_out", 
                                              program_card_name = date,
                                              path_to_data = path_to_data)

if __name__ == "__main__":
    main()