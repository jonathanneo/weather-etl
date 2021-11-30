from typing import Tuple
import pandas as pd 

def clean_abs_data(input_df:pd.DataFrame)->Tuple:
    df = input_df.copy(deep=True) # create a deep copy of the DataFrame
    # do cleaning here 
    df = df.dropna()  # this is one example cleaning step, you should do more 
    df_suburb = df[["colA", "colB"]]
    df_population = df[["colA", "colB"]]
    return (df_suburb, df_population)

def clean_road_crash_data(input_df:pd.DataFrame)->pd.DataFrame:
    df = input_df.copy(deep=True) # create a deep copy of the DataFrame
    # do cleaning here 
    df = df.dropna()  # this is one example cleaning step, you should do more 
    return df 
