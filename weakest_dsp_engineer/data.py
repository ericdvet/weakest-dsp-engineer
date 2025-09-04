# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 10:10:25 2025

@author: ericdvet
"""

import pandas as pd
import datetime
import sys
import os

def main():
    
    file_name = "novice_program_a.csv"
    df_a = get_exercise_df(file_name)
    file_name = "novice_program_b.csv"
    df_b = get_exercise_df(file_name)
    
    first_date = datetime.date(2025, 6, 23)
    last_date = datetime.date(2025, 8, 25)
    
    dates, labels = program_mwf_ab(first_date, last_date)
    folder_name = "fill_out"
    
    # Create the program cards
    # save_empty_program_ab(dates, labels, df_a, df_b, folder_name)
    
    
    program_name = "/2025-06-23.csv"
    path_to_data = "ericdvet.csv"
    
    for i, date in enumerate(dates):
        dates[i] = "/" + str(date) + ".csv"
    
    # Update the program cards with the data
    for program_card_name in dates:
        update_data_from_program_card(program_card_dir = "fill_out", 
                                      program_card_name = program_card_name,
                                      path_to_data = path_to_data)

def update_data_from_program_card(program_card_dir : str, program_card_name : str, 
                                  path_to_data : str):
    """
    Updates the data log from program card.

    Parameters
    ----------
    program_card_dir : str
        Directory of program card.
    program_card_name : str
        Program card file name.
    path_to_data : str
        Path to data log.

    Returns
    -------
    None.

    """
    
    path_to_program = program_card_dir + "/" + program_card_name
    program = pd.read_csv(path_to_program)
    
    if os.path.exists(path_to_data):
        df = pd.read_csv(path_to_data, index_col=0)
    else:
        d = {"date": [], "exercise": [], "weight": [], "reps": []}
        df = pd.DataFrame(d)
        df.index.name = "index"
    
    for index, row in program.iterrows():
        date = program_card_name[1:]
        date = date[:-4]
        
        if index == 0:
            if date in df["date"].values:
                print(f"WARNING: Skipping duplicate entry {date}")
                break
        
        new_row = {"date": date, "exercise": row["exercise name"],
                   "weight": row["weight"], "reps": row["reps"]}
        df.loc[len(df)] = new_row
    
    df.to_csv(path_to_data)
    

def save_empty_program_card_ab(dates : list, labels : list,
                            df_a : pd.DataFrame, df_b : pd.DataFrame,
                            folder_name : str = "fill_out"):
    """
    Save empty program cards for program with 'a'/'b' labels.

    Parameters
    ----------
    dates : list
        List of dates.
    labels : list
        Labels for dates.
    df_a :  pd.DataFrame
        Program card for workout 'a'.
    df_b :  pd.DataFrame
        Program card for workout 'b'.
    folder_name : str, optional
        Name of folder in which to save program cards. The default is 
        "fill_out".

    Returns
    -------
    None.

    """
    for i, date in enumerate(dates):
        
        if labels[i] == 'a':
            df = df_a
        else:
            df = df_b
            
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)
            
        path_to_csv = f"{folder_name}/{date}.csv"
        
        if os.path.exists(path_to_csv):
            if not os.path.isdir(f"{folder_name}/archive"):
                os.makedirs(f"{folder_name}/archive")
            archive = pd.read_csv(path_to_csv)
            print(f"Archiving previous file in {folder_name}/archive/{date}.csv")
            archive.to_csv(f"{folder_name}/archive/{date}.csv")
            
        df.to_csv(path_to_csv)
    
def program_mwf_ab(first_date : datetime.date, last_date : datetime.date,
                   first_label : str = 'a'):
    """
    Generates dates and labels for workout routine following A and B days,
    done Monday, Wednesday, Friday.

    Parameters
    ----------
    first_date : datetime.date
        Starting date.
    last_date : datetime.date
        Ending date.
    first_label : str, optional
        Label of first_date.

    Returns
    -------
    dates : TYPE
        List of mondays, wednesdays, and fridays from first_date to last_date.
    labels : TYPE
        'a' and 'b' labels for dates.

    """
    
    dates = []
    labels = []
    
    date = first_date
    label = first_label
    
    while(date <= last_date):
        dates.append(date)
        labels.append(label)
        
        date = date + datetime.timedelta(days=2)
        if date.weekday() == 6:
            date = date + datetime.timedelta(days=1)
            
        if label == 'a':
            label = 'b'
        else:
            label = 'a'
            
    return dates, labels

def get_exercise_df(file_name : str):
    """
    Convert the exercise and set scheme to a fillable program card. Exercise
    and set scheme is expected to be in the following format:

        pause bench,3
        pull-up,3


    Parameters
    ----------
    file_name : str
        Name of file with exercise and set scheme.

    Returns
    -------
    df : pd.Dataframe
        Program card.

    """
    
    f = open(file_name)
    file_contents = f.read()
    routine = file_contents.split('\n')
    
    exercises = []
    sets = []
    
    for i in routine:
        
        if ',' not in i:
            raise ValueError(f"ERROR: No ',' found in [{i}]")
            
        exercises_set = i.split(',')
        if exercises_set[0][-1] == ' ':
            exercise = exercises_set[0][:-1]
        else:
            exercise = exercises_set[0]
        exercises.append(exercise.lower()) # Standardize
        
        if exercises_set[0][0] == ' ':
            set_num = exercises_set[1][1:]
        else:
            set_num = exercises_set[1]
        sets.append(set_num)
    
    exercises_duplicated  = []
    for i, set_num in enumerate(sets):
        exercise_name = exercises[i]
        for j in range(int(set_num)):
            exercises_duplicated.append(exercise_name)
            
    df = pd.DataFrame(exercises_duplicated, columns=["exercise name"])
    df["weight"] = None
    df["reps"] = None
    
    return df
    
if __name__ == "__main__":
    main()