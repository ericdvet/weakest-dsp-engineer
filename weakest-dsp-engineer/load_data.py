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
    print(dates)
    print(labels)
    
    folder_name = "fill_out"
    
    for i, date in enumerate(dates):
        if labels[i] == 'a':
            df = df_a
        else:
            df = df_b
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)
        df.to_csv(f"{folder_name}/{date}.csv")
    
def program_mwf_ab(first_date : datetime.date, 
                   last_date : datetime.date):
    
    dates = []
    labels = []
    
    date = first_date
    label = 'a'
    
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
    
    # 
    


def get_exercise_df(file_name : str):
    """
    Convert the exercise and set scheme to a pandas dataframe format.

    Parameters
    ----------
    file_name : str
        DESCRIPTION.

    Returns
    -------
    df : pd.Dataframe
        DESCRIPTION.

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
    
    sets_indented = []
    for i in sets:
        temp = []
        for j in range(int(i)):
            temp.append('')
            temp.append('')
        sets_indented.append(temp)
        
    df = pd.DataFrame(index=exercises, data = {'Set': sets_indented})
    df.index.name = "exercise name"
    
    df = df.join(
        pd.DataFrame(df.pop('Set').tolist(), index=df.index)
          .fillna('')
          .rename(columns=lambda c: f'set_{c//2 + 1}' if c % 2 == 0 else f'reps_{c//2 + 1}')
    )
    
    return df
    
if __name__ == "__main__":
    main()