# Databricks notebook source
# MAGIC %md
# MAGIC <p style="text-align:center">
# MAGIC     <a href="https://skills.network" target="_blank">
# MAGIC     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo">
# MAGIC     </a>
# MAGIC </p>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # **SpaceX  Falcon 9 first stage Landing Prediction**
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Hands-on Lab: Complete the Data Collection API Lab
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Estimated time needed: **45** minutes
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC In this capstone, we will predict if the Falcon 9 first stage will land successfully. SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because SpaceX can reuse the first stage. Therefore if we can determine if the first stage will land, we can determine the cost of a launch. This information can be used if an alternate company wants to bid against SpaceX for a rocket launch. In this lab, you will collect and make sure the data is in the correct format from an API. The following is an example of a successful and launch.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/lab_v2/images/landing_1.gif)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Several examples of an unsuccessful landing are shown here:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/lab_v2/images/crash.gif)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Most unsuccessful landings are planned. Space X performs a controlled landing in the oceans. 
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Objectives
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC In this lab, you will make a get request to the SpaceX API. You will also do some basic data wrangling and formating. 
# MAGIC
# MAGIC - Request to the SpaceX API
# MAGIC - Clean the requested data
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ----
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Install the below libraries
# MAGIC

# COMMAND ----------

!pip install requests
!pip install pandas
!pip install numpy

# COMMAND ----------

# MAGIC %md
# MAGIC ## Import Libraries and Define Auxiliary Functions
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC We will import the following libraries into the lab
# MAGIC

# COMMAND ----------

# Requests allows us to make HTTP requests which we will use to get data from an API
import requests
# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Datetime is a library that allows us to represent dates
import datetime

# Setting this option will print all collumns of a dataframe
pd.set_option('display.max_columns', None)
# Setting this option will print all of the data in a feature
pd.set_option('display.max_colwidth', None)

# COMMAND ----------

# MAGIC %md
# MAGIC Below we will define a series of helper functions that will help us use the API to extract information using identification numbers in the launch data.
# MAGIC
# MAGIC From the <code>rocket</code> column we would like to learn the booster name.
# MAGIC

# COMMAND ----------

# Takes the dataset and uses the rocket column to call the API and append the data to the list
def getBoosterVersion(data):
    for x in data['rocket']:
       if x:
        response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
        BoosterVersion.append(response['name'])

# COMMAND ----------

# MAGIC %md
# MAGIC From the <code>launchpad</code> we would like to know the name of the launch site being used, the logitude, and the latitude.
# MAGIC

# COMMAND ----------

# Takes the dataset and uses the launchpad column to call the API and append the data to the list
def getLaunchSite(data):
    for x in data['launchpad']:
       if x:
         response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
         Longitude.append(response['longitude'])
         Latitude.append(response['latitude'])
         LaunchSite.append(response['name'])

# COMMAND ----------

# MAGIC %md
# MAGIC From the <code>payload</code> we would like to learn the mass of the payload and the orbit that it is going to.
# MAGIC

# COMMAND ----------

# Takes the dataset and uses the payloads column to call the API and append the data to the lists
def getPayloadData(data):
    for load in data['payloads']:
       if load:
        response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])

# COMMAND ----------

# MAGIC %md
# MAGIC From <code>cores</code> we would like to learn the outcome of the landing, the type of the landing, number of flights with that core, whether gridfins were used, wheter the core is reused, wheter legs were used, the landing pad used, the block of the core which is a number used to seperate version of cores, the number of times this specific core has been reused, and the serial of the core.
# MAGIC

# COMMAND ----------

# Takes the dataset and uses the cores column to call the API and append the data to the lists
def getCoreData(data):
    for core in data['cores']:
            if core['core'] != None:
                response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                Block.append(response['block'])
                ReusedCount.append(response['reuse_count'])
                Serial.append(response['serial'])
            else:
                Block.append(None)
                ReusedCount.append(None)
                Serial.append(None)
            Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
            Flights.append(core['flight'])
            GridFins.append(core['gridfins'])
            Reused.append(core['reused'])
            Legs.append(core['legs'])
            LandingPad.append(core['landpad'])

# COMMAND ----------

# MAGIC %md
# MAGIC Now let's start requesting rocket launch data from SpaceX API with the following URL:
# MAGIC

# COMMAND ----------

spacex_url="https://api.spacexdata.com/v4/launches/past"

# COMMAND ----------

response = requests.get(spacex_url)

# COMMAND ----------

# MAGIC %md
# MAGIC Check the content of the response
# MAGIC

# COMMAND ----------

print(response.content)

# COMMAND ----------

# MAGIC %md
# MAGIC You should see the response contains massive information about SpaceX launches. Next, let's try to discover some more relevant information for this project.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 1: Request and parse the SpaceX launch data using the GET request
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC To make the requested JSON results more consistent, we will use the following static response object for this project:
# MAGIC

# COMMAND ----------

static_json_url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'

# COMMAND ----------

# MAGIC %md
# MAGIC We should see that the request was successfull with the 200 status response code
# MAGIC

# COMMAND ----------

response=requests.get(static_json_url)

# COMMAND ----------

response.status_code

# COMMAND ----------

# MAGIC %md
# MAGIC Now we decode the response content as a Json using <code>.json()</code> and turn it into a Pandas dataframe using <code>.json_normalize()</code>
# MAGIC

# COMMAND ----------

# Use json_normalize meethod to convert the json result into a dataframe
data = pd.json_normalize(response.json())

# COMMAND ----------

# MAGIC %md
# MAGIC Using the dataframe <code>data</code> print the first 5 rows
# MAGIC

# COMMAND ----------

# Get the head of the dataframe
data.head()

# COMMAND ----------

# MAGIC %md
# MAGIC You will notice that a lot of the data are IDs. For example the rocket column has no information about the rocket just an identification number.
# MAGIC
# MAGIC We will now use the API again to get information about the launches using the IDs given for each launch. Specifically we will be using columns <code>rocket</code>, <code>payloads</code>, <code>launchpad</code>, and <code>cores</code>.
# MAGIC

# COMMAND ----------

# Lets take a subset of our dataframe keeping only the features we want and the flight number, and date_utc.
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# We will remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket.
data = data[data['cores'].map(len)==1]
data = data[data['payloads'].map(len)==1]

# Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
data['cores'] = data['cores'].map(lambda x : x[0])
data['payloads'] = data['payloads'].map(lambda x : x[0])

# We also want to convert the date_utc to a datetime datatype and then extracting the date leaving the time
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# Using the date we will restrict the dates of the launches
data = data[data['date'] <= datetime.date(2020, 11, 13)]

# COMMAND ----------

# MAGIC %md
# MAGIC * From the <code>rocket</code> we would like to learn the booster name
# MAGIC
# MAGIC * From the <code>payload</code> we would like to learn the mass of the payload and the orbit that it is going to
# MAGIC
# MAGIC * From the <code>launchpad</code> we would like to know the name of the launch site being used, the longitude, and the latitude.
# MAGIC
# MAGIC * **From <code>cores</code> we would like to learn the outcome of the landing, the type of the landing, number of flights with that core, whether gridfins were used, whether the core is reused, whether legs were used, the landing pad used, the block of the core which is a number used to seperate version of cores, the number of times this specific core has been reused, and the serial of the core.**
# MAGIC
# MAGIC The data from these requests will be stored in lists and will be used to create a new dataframe.
# MAGIC

# COMMAND ----------

#Global variables 
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

# COMMAND ----------

# MAGIC %md
# MAGIC These functions will apply the outputs globally to the above variables. Let's take a looks at <code>BoosterVersion</code> variable. Before we apply  <code>getBoosterVersion</code> the list is empty:
# MAGIC

# COMMAND ----------

BoosterVersion

# COMMAND ----------

# MAGIC %md
# MAGIC Now, let's apply <code> getBoosterVersion</code> function method to get the booster version
# MAGIC

# COMMAND ----------

# Call getBoosterVersion
getBoosterVersion(data)

# COMMAND ----------

# MAGIC %md
# MAGIC the list has now been update 
# MAGIC

# COMMAND ----------

BoosterVersion[0:5]

# COMMAND ----------

# MAGIC %md
# MAGIC we can apply the rest of the  functions here:
# MAGIC

# COMMAND ----------

# Call getLaunchSite
getLaunchSite(data)

# COMMAND ----------

# Call getPayloadData
getPayloadData(data)

# COMMAND ----------

# Call getCoreData
getCoreData(data)

# COMMAND ----------

# MAGIC %md
# MAGIC Finally lets construct our dataset using the data we have obtained. We we combine the columns into a dictionary.
# MAGIC

# COMMAND ----------

launch_dict = {'FlightNumber': list(data['flight_number']),
'Date': list(data['date']),
'BoosterVersion':BoosterVersion,
'PayloadMass':PayloadMass,
'Orbit':Orbit,
'LaunchSite':LaunchSite,
'Outcome':Outcome,
'Flights':Flights,
'GridFins':GridFins,
'Reused':Reused,
'Legs':Legs,
'LandingPad':LandingPad,
'Block':Block,
'ReusedCount':ReusedCount,
'Serial':Serial,
'Longitude': Longitude,
'Latitude': Latitude}


# COMMAND ----------

# MAGIC %md
# MAGIC Then, we need to create a Pandas data frame from the dictionary launch_dict.
# MAGIC

# COMMAND ----------

# Create a data from launch_dict
df = pd.DataFrame(launch_dict)

# COMMAND ----------

# MAGIC %md
# MAGIC Show the summary of the dataframe
# MAGIC

# COMMAND ----------

# Show the head of the dataframe
df.describe()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2: Filter the dataframe to only include `Falcon 9` launches
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Finally we will remove the Falcon 1 launches keeping only the Falcon 9 launches. Filter the data dataframe using the <code>BoosterVersion</code> column to only keep the Falcon 9 launches. Save the filtered data to a new dataframe called <code>data_falcon9</code>.
# MAGIC

# COMMAND ----------

# Hint data['BoosterVersion']!='Falcon 1'
data_falcon9 = df[df['BoosterVersion']!='Falcon 1']

# COMMAND ----------

# MAGIC %md
# MAGIC Now that we have removed some values we should reset the FlgihtNumber column
# MAGIC

# COMMAND ----------

data_falcon9.loc[:,'FlightNumber'] = list(range(1, data_falcon9.shape[0]+1))
data_falcon9

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Wrangling
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC We can see below that some of the rows are missing values in our dataset.
# MAGIC

# COMMAND ----------

data_falcon9.isnull().sum()

# COMMAND ----------

# MAGIC %md
# MAGIC Before we can continue we must deal with these missing values. The <code>LandingPad</code> column will retain None values to represent when landing pads were not used.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3: Dealing with Missing Values
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Calculate below the mean for the <code>PayloadMass</code> using the <code>.mean()</code>. Then use the mean and the <code>.replace()</code> function to replace `np.nan` values in the data with the mean you calculated.
# MAGIC

# COMMAND ----------

# Calculate the mean value of PayloadMass column
PayloadMassMean = data_falcon9['PayloadMass'].mean()
# Replace the np.nan values with its mean value
data_falcon9['PayloadMass'] = data_falcon9['PayloadMass'].replace(np.nan, PayloadMassMean)

# COMMAND ----------

# MAGIC %md
# MAGIC You should see the number of missing values of the <code>PayLoadMass</code> change to zero.
# MAGIC

# COMMAND ----------

data_falcon9.isnull().sum()

# COMMAND ----------

# MAGIC %md
# MAGIC Now we should have no missing values in our dataset except for in <code>LandingPad</code>.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC We can now export it to a <b>CSV</b> for the next section,but to make the answers consistent, in the next lab we will provide data in a pre-selected date range. 
# MAGIC

# COMMAND ----------

data_falcon9.to_csv('/Workspace/Users/jkgonzalezp@gmail.com/Ciencia de datos IBM - Coursera/Applied Data Science Capstone/module_1/dataset_part_1.csv', index=False)

# COMMAND ----------

# MAGIC %md
# MAGIC <code>data_falcon9.to_csv('dataset_part_1.csv', index=False)</code>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Authors
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <a href="https://www.linkedin.com/in/joseph-s-50398b136/">Joseph Santarcangelo</a> has a PhD in Electrical Engineering, his research focused on using machine learning, signal processing, and computer vision to determine how videos impact human cognition. Joseph has been working for IBM since he completed his PhD. 
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <!--## Change Log
# MAGIC -->
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <!--
# MAGIC
# MAGIC |Date (YYYY-MM-DD)|Version|Changed By|Change Description|
# MAGIC |-|-|-|-|
# MAGIC |2020-09-20|1.1|Joseph|get result each time you run|
# MAGIC |2020-09-20|1.1|Azim |Created Part 1 Lab using SpaceX API|
# MAGIC |2020-09-20|1.0|Joseph |Modified Multiple Areas|
# MAGIC -->
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Copyright © 2021 IBM Corporation. All rights reserved.
# MAGIC