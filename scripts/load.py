# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 20:11:36 2025

@author: ericdvet
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime

import weakest_dsp_engineer as wde

def main():
    
    file_name = "novice_program_a.csv"
    df_a = wde.get_exercise_df(file_name)
    file_name = "novice_program_b.csv"
    df_b = wde.get_exercise_df(file_name)
    
    first_date = datetime.date(2025, 7, 14)
    last_date = datetime.date(2025, 8, 25)
    
    dates, labels = wde.program_mwf_ab(first_date, last_date, 'a')
    folder_name = "fill_out"
    
    # Create the program cards
    wde.save_empty_program_card_ab(dates, labels, df_a, df_b, folder_name)
    
if __name__ == "__main__":
    main()