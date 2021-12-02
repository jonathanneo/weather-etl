import pandas as pd 

def convert_unix_timestamp(input_df:pd.DataFrame, date_columns:list=[])->pd.DataFrame:
    """
    Converts unix timestamp columns to datetime string.. 

    input: 
    - input_df: your input dataframe 
    - date_columns: a list of column names which contains unix timestamps you wish to convert 

    returns: 
    - cleaned dataframe
    """
    df = input_df.copy(deep=True)
    for date_column in date_columns: 
        df[date_column] = pd.to_datetime(df[date_column], unit="s") # i did some change
    return df 

def replace_column_character(input_df:pd.DataFrame, replace_dict:dict={})->pd.DataFrame:
    """
    Replaces characters that exist in your columns. 

    input: 
    - input_df: your input dataframe 
    - replace_dict: a dictionary with mappings of {"source": "target"}

    returns: 
    - cleaned dataframe
    """
    df = input_df.copy(deep=True)
    new_columns = {} 
    for column in df.columns: 
        for key in replace_dict.keys():
            if new_columns.get(column) is None: 
                new_columns[column] = column.replace(key, replace_dict[key])
            else: 
                new_columns[column] = new_columns[column].replace(key, replace_dict[key])
    return df.rename(columns=new_columns)