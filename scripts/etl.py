#!/usr/bin/env python
# coding: utf-8

# ## Import dependencies

# In[45]:


import requests
import pandas as pd 
import os 
import transform_functions as tf
from credentials import *  


# In[ ]:


# ignore warnings
import warnings
warnings.filterwarnings('ignore')


# ## Get Australian Capital Cities
# Read in CSV of australian capital cities

# In[46]:


file_path = os.path.dirname(os.path.realpath(__file__))
capital_cities_df = pd.read_csv(os.path.join(file_path, "..", "data", "australian_capital_cities.csv"))


# ## Get Weather Data 
# Get weather data by requesting from openweathermap REST APIs for each capital city 

# In[47]:


weather_data = []
for city_name in capital_cities_df["city_name"]:
    params = {
        "q": city_name,
        "units": "metric",
        "appid": api_key
    }   
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather", params=params)
    if response.status_code == 200: 
        weather_data.append(requests.get(f"http://api.openweathermap.org/data/2.5/weather", params=params).json())
    else: 
        raise Exception("Extracting weather api data failed. Please check if API limits have been reached.")


# ## Read JSON data into Pandas DataFrame

# In[48]:


weather_df = pd.json_normalize(weather_data)
weather_df.head()


# ## Convert unix timestamp to datetime timestamp string 

# In[49]:


date_fixed_weather_df = tf.convert_unix_timestamp(input_df = weather_df, date_columns=["dt"])
date_fixed_weather_df.head()


# ## Replace column names

# In[50]:


clean_weather_df = tf.replace_column_character(date_fixed_weather_df, {".": "_"})
clean_weather_df.head()


# ## Rename fields

# In[51]:


clean_weather_df = clean_weather_df.rename(columns={
    "id":"city_id", 
    "dt": "datetime"
})
clean_weather_df.head()


# ## Create City DataFrame

# In[52]:


city_df = clean_weather_df[["city_id", "name", "coord_lon", "coord_lat"]].drop_duplicates() 
city_df.head()


# ## Create Temperature DataFrame

# In[53]:


temperature_df = clean_weather_df[["city_id", "datetime", "main_temp", "main_feels_like", "main_temp_min", "main_temp_max"]]
temperature_df.head()


# ## Create Atmosphere DataFrame

# In[54]:


atmosphere_df = clean_weather_df[["city_id", "datetime", 'main_pressure', 'main_humidity']]
atmosphere_df.head()


# ## Create SQL Connection

# In[55]:


from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.dialects import postgresql
from urllib.parse import quote_plus as urlquote
connection_url = URL.create(
    drivername = "postgresql", 
    username = db_user,
    password = db_password,
    host = "localhost", 
    port = 5432,
    database = "weather_db", 
)

engine = create_engine(connection_url)


# ## Reflect ORM

# In[56]:


from sqlalchemy import MetaData
metadata_obj = MetaData()
metadata_obj.reflect(bind=engine)
city = metadata_obj.tables["city"]
temperature = metadata_obj.tables["temperature"]
atmosphere = metadata_obj.tables["atmosphere"]


# ## Upsert: City

# In[57]:


insert_statement = postgresql.insert(city).values(city_df.to_dict(orient='records'))
upsert_statement = insert_statement.on_conflict_do_update(
    index_elements=['city_id'],
    set_={c.key: c for c in insert_statement.excluded if c.key not in ['city_id']})
engine.execute(upsert_statement)


# ## Upsert: Temperature

# In[58]:


insert_statement = postgresql.insert(temperature).values(temperature_df.to_dict(orient='records'))
upsert_statement = insert_statement.on_conflict_do_update(
    index_elements=['city_id', 'datetime'],
    set_={c.key: c for c in insert_statement.excluded if c.key not in ['city_id', 'datetime']})
engine.execute(upsert_statement)


# ## Upsert Atmosphere

# In[59]:


insert_statement = postgresql.insert(atmosphere).values(atmosphere_df.to_dict(orient='records'))
upsert_statement = insert_statement.on_conflict_do_update(
    index_elements=['city_id', 'datetime'],
    set_={c.key: c for c in insert_statement.excluded if c.key not in ['city_id', 'datetime']})
engine.execute(upsert_statement)


# In[1]:


import datetime as dt 
print(f"ETL job completed at {dt.datetime.now()}")

