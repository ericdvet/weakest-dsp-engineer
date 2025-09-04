# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 10:22:03 2025

@author: ericdvet
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime

import weakest_dsp_engineer as wde

def main():
    
    routine_a = "strong_lifts_a.csv"
    routine_b = "strong_lifts_b.csv"
    path_to_data = "ericdvet.csv"
    first_label = 'a'
    folder_name = "program_cards"
    
    # Get the program cards for both routines 
    df_a = wde.get_exercise_df(routine_a)
    df_b = wde.get_exercise_df(routine_b)
    
    # 1 week of program cards
    first_date = datetime.date(2025, 9, 22)
    last_date = first_date + datetime.timedelta(days=5)
    
    # Create program cards
    dates, labels = wde.program_mwf_ab(first_date, last_date, first_label)
    wde.save_empty_program_card_ab(dates, labels, df_a, df_b, folder_name)
    
    input(f"Update the program cards in /{folder_name}. Click ENTER to continue")

    # Get the paths to all filled program cards
    for i, date in enumerate(dates):
        dates[i] = "/" + str(date) + ".csv"
        
    # Update the data with the program cards
    for entry in os.listdir(folder_name):
        if entry[-4:] == ".csv":
            date = entry
            wde.update_data_from_program_card(program_card_dir = folder_name, 
                                              program_card_name = date,
                                              path_to_data = path_to_data)
    
    # Remove all program cards since their contents are now saved in path_to_data
    for i, file in enumerate(dates):
        path_to_file = folder_name + file
        os.remove(path_to_file)
    
if __name__ == "__main__":
    main()