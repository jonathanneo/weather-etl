# THIS IS A DEMO SCRIPT AND CONTAINS UN-TESTED AND UN-VERIFIED CODE
import sqlalchemy 
import pandas as pd 
import requests 
import transform_functions as tf

# EXTRACT 
json_data = requests.get("https://abs.gov.au/some_api_here").json()
df_abs_data = pd.read_json(json_data)
df_road_crash_data = pd.read_csv("https://data.sa.gov.au/data/dataset/12345/road_crash.csv")

# TRANSFORM 
df_suburb, df_population = tf.clean_abs_data(df_abs_data)
df_road_crash_data_clean = tf.clean_road_crash_data(df_road_crash_data)

# LOAD 
engine = sqlalchemy.create_engine("postgresql://scott:tiger@localhost/mydatabase")

# Delete data first 
engine.execute("DELETE FROM crashes;")
engine.execute("DELETE FROM population;")
engine.execute("DELETE FROM suburb;")

# Load data 
df_suburb.to_sql("suburb", engine, if_exists="append")
df_population.to_sql("population", engine, if_exists="append")
df_road_crash_data_clean.to_sql("crashes", engine, if_exists="append")

print("ETL complete!")