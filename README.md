# Purpose and motivation

Explain the questions you are trying to answer by provisioning data as a data engineer. Explain how the data you provision is going to help data analysts perform their role. 

# Solution 

## Solution architecture 

![simple_solution_architecture.drawio.png](images/simple_solution_architecture.drawio.png)

The **E**xtract, **T**ransform, and **L**oad steps are explained below. 

## Extract 

### Data sources 
Data is extracted from the following data sources. 

| No | Data Source | Description | Source Type | URL | 
| - | - | - |- | - |
| 1 | Australian Bureau of Statitics | Contains data relating to population statitics | REST API | https://www.abs.gov.au/ | 
| 2 | Accidents CSV | Contains data relating to road accidents from data.gov.au | CSV | https://data.gov.au/dataset/ds-sa-21386a53-56a1-4edf-bd0b-61ed15f10acf/details?q=car%20crash | 

### Schedule 

The ETL job runs on a scheduled basis at 5am every week using Cron on Mac OS. 

![cronjob.png](images/cronjob.png)

Here is the cron code used: 

```
0 5 * * 1 blah/blah/blah/python3 etl.py
```

## Transform 

The following transformation scripts are executed: 
| Script | Input | Output |  
| - | - |- |
| `etl.py` | [1], [2] | `population`, `suburb`, `crashes` | 

## Load 


### Entity Relationship Diagram 
Data is loaded into the tables listed below. 

![erd.png](images/erd.png)

The Data Definition Language (DDL) used to create the tables can be found [here](scripts/ddl_create_table.sql). 


### Loading process 
The loading procedure is as follows: 

1. Delete data from target tables 
```sql
-- Delete data from the target tables 
DELETE FROM crashes; 
DELETE FROM population; 
DELETE FROM suburb;
```

2. Insert data using sqlalchemy and pandas 
```python
# Insert data using sqlalchemy + pd.to_sql 
engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')

df_suburb.to_sql("suburb", engine)
df_population.to_sql("population", engine)
df_crashes.to_sql("crashes", engine)

```

### Data dictionary 
| Table name | Column name | Definition | 
| - | - | - | 
| suburb | suburb_id | The unique id of each suburb | 
| suburb | suburb_name | The name of each suburb | 
| population | population_id | The unique id of each population entry (unique per year + suburb_id) | 
| population | suburb_id | The foreign key to the suburb table | 
| population | year | The year of the population count |
| population | population_count | The population count observed for the specified year | 
| crashes | crash_id | The unique id of each crash | 
| crashes | crash_lat | The latitude of each crash | 
| crashes | crash_lng | The longitude of each crash | 
| crashes | suburb_id | The foreign key to the suburb table | 
| crashes | crash_description | The description of the crash that was entered by the attending officer at that time | 

# Usage 

## Python dependencies 
The required python libraries and version have been specified in [requirements.txt](requirements.txt). 

Install python dependencies by performing : 

```
pip install -r requirements.txt 
```

## Running code locally 
To run the ETL code on your computer, execute the following in your terminal: 

```
python scripts/etl.py
```

## Run unit tests 
To run the unit tests on your computer, execute the following in your terminal: 

```
pytest scripts/tests
```

You should see the following output: 

```
======= test session starts =======
collected 2 items   
scripts/tests/test_transformation_functions.py ...   [100%]
======= 2 passed in 5.40s =======
```

## Scheduling jobs 
TODO. 


# Contributors
- [@jonathanneo](https://github.com/jonathanneo)
- [@yourTeamMate1](https://github.com)
- [@yourTeamMate2](https://github.com)