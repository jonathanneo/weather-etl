import pandas as pd
import datetime as dt
from transform_functions import * 

def test_convert_unix_timestamp():

    # ASSEMBLE 
    input_df = pd.DataFrame({
        "id": [1,2],
        "timestamp1": [1638368789,1638369080], 
        "timestamp2": [1638369141,1638369162]
    })

    expected_df = pd.DataFrame({
        "id": [1,2], 
        "timestamp1": [dt.datetime(2021,12,1,14,26,29), dt.datetime(2021,12,1,14,31,20)], 
        "timestamp2": [dt.datetime(2021,12,1,14,32,21), dt.datetime(2021,12,1,14,32,42)]
    })

    # ACT 
    output_df = convert_unix_timestamp(input_df=input_df, date_columns=["timestamp1", "timestamp2"])

    # ASSERT 

    pd.testing.assert_frame_equal(left=output_df, right=expected_df,check_exact=True)

def test_replace_column_character():

    # ASSEMBLE 
    input_df = pd.DataFrame({
        "id": [1,2],
        "first.name": ["Bob","Tom"], 
        "last-name": ["Builder","Cruise"]
    })

    expected_df = pd.DataFrame({
        "id": [1,2],
        "first_name": ["Bob","Tom"], 
        "last_name": ["Builder","Cruise"]
    })

    # ACT 
    output_df = replace_column_character(input_df=input_df, replace_dict={
            ".":"_", 
            "-": "_"
        })

    # ASSERT 
    pd.testing.assert_frame_equal(left=output_df, right=expected_df,check_exact=True)