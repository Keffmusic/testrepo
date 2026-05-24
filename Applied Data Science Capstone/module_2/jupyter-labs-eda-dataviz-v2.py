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
# MAGIC # **SpaceX  Falcon 9 First Stage Landing Prediction**
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC  ## Hands-on Lab: Complete the EDA with Visualization
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Estimated time needed: **70** minutes
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC In this assignment, we will predict if the Falcon 9 first stage will land successfully. SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is due to the fact that SpaceX can reuse the first stage. 
# MAGIC
# MAGIC In this lab, you will perform Exploratory Data Analysis and Feature Engineering.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Falcon 9 first stage will land successfully
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/landing_1.gif)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Several examples of an unsuccessful landing are shown here:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/crash.gif)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Most unsuccessful landings are planned. Space X performs a controlled landing in the oceans. 
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC   ## Objectives
# MAGIC Perform exploratory Data Analysis and Feature Engineering using `Pandas` and `Matplotlib`
# MAGIC
# MAGIC - Exploratory Data Analysis
# MAGIC - Preparing Data  Feature Engineering 
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

!pip install pandas
!pip install numpy
!pip install seaborn
!pip install matplotlib

# COMMAND ----------

# MAGIC %md
# MAGIC ### Import Libraries and Define Auxiliary Functions
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC We will import the following libraries the lab 
# MAGIC
# MAGIC

# COMMAND ----------

# andas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exploratory Data Analysis 
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC First, let's read the SpaceX dataset into a Pandas dataframe and print its summary
# MAGIC

# COMMAND ----------

df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

# If you were unable to complete the previous lab correctly you can uncomment and load this csv

# df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/dataset_part_2.csv')

df.head(5)

# COMMAND ----------

# MAGIC %md
# MAGIC First, let's try to see how the `FlightNumber` (indicating the continuous launch attempts.) and `Payload` variables would affect the launch outcome.
# MAGIC
# MAGIC We can plot out the <code>FlightNumber</code> vs. <code>PayloadMass</code>and overlay the outcome of the launch. We see that as the flight number increases, the first stage is more likely to land successfully. The payload mass is also important; it seems the more massive the payload, the less likely the first stage will return.
# MAGIC

# COMMAND ----------

sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC Next, let's drill down to each site visualize its detailed launch records.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### TASK 1: Visualize the relationship between Flight Number and Launch Site
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Use the function <code>catplot</code> to plot <code>FlightNumber</code> vs <code>LaunchSite</code>, set the  parameter <code>x</code>  parameter to <code>FlightNumber</code>,set the  <code>y</code> to <code>Launch Site</code> and set the parameter <code>hue</code> to <code>'class'</code>
# MAGIC

# COMMAND ----------

# Plot a scatter point chart with x axis to be Flight Number and y axis to be the launch site, and hue to be the class value
sns.catplot(y = 'LaunchSite', x = 'FlightNumber', hue = 'Class', data = df, aspect = 5)
plt.xlabel("Flight Number", fontsize = 20)
plt.ylabel("Launch Site", fontsize = 20)
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC Now try to explain the patterns you found in the Flight Number vs. Launch Site scatter point plots.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### TASK 2: Visualize the relationship between Payload and Launch Site
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC We also want to observe if there is any relationship between launch sites and their payload mass.
# MAGIC

# COMMAND ----------

# Plot a scatter point chart with x axis to be Pay Load Mass (kg) and y axis to be the launch site, and hue to be the class value
sns.catplot(y = 'LaunchSite', x = 'PayloadMass', hue = 'Class', data = df, aspect = 5)
plt.xlabel("Pay Load Mass (kg)", fontsize = 20)
plt.ylabel("Launch Site", fontsize = 20)
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC Now if you observe Payload Vs. Launch Site scatter point chart you will find for the VAFB-SLC  launchsite there are no  rockets  launched for  heavypayload mass(greater than 10000).
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### TASK  3: Visualize the relationship between success rate of each orbit type
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Next, we want to visually check if there are any relationship between success rate and orbit type.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Let's create a `bar chart` for the sucess rate of each orbit
# MAGIC

# COMMAND ----------

# HINT use groupby method on Orbit column and get the mean of Class column

# Agrupar por Orbit y calcular la media de Class (success rate)
orbit_success = df.groupby('Orbit')['Class'].mean().reset_index()

# Crear el gráfico de barras
sns.barplot(x='Orbit', y='Class', data=orbit_success)
plt.ylabel("Success Rate", fontsize=12)
plt.xlabel("Orbit Type", fontsize=12)
plt.title("Success Rate by Orbit Type")
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC Analyze the ploted bar chart try to find which orbits have high sucess rate.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### TASK  4: Visualize the relationship between FlightNumber and Orbit type
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC For each orbit, we want to see if there is any relationship between FlightNumber and Orbit type.
# MAGIC

# COMMAND ----------

# Plot a scatter point chart with x axis to be FlightNumber and y axis to be the Orbit, and hue to be the class value
sns.scatterplot(x = 'FlightNumber', y = 'Orbit', hue = 'Class', data = df)
plt.xlabel("Flight Number", fontsize = 20)
plt.ylabel("Orbit", fontsize = 20)
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC You should see that in the LEO orbit the Success appears related to the number of flights; on the other hand, there seems to be no relationship between flight number when in GTO orbit.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### TASK  5: Visualize the relationship between Payload and Orbit type
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Similarly, we can plot the Payload vs. Orbit scatter point charts to reveal the relationship between Payload and Orbit type
# MAGIC

# COMMAND ----------

# Plot a scatter point chart with x axis to be Payload and y axis to be the Orbit, and hue to be the class value
sns.catplot(x = 'PayloadMass', y = 'Orbit', hue = 'Class', data = df)
plt.xlabel("Payload Mass", fontsize = 20)
plt.ylabel("Orbit", fontsize = 20)
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC With heavy payloads the successful landing or positive landing rate are more for Polar,LEO and ISS.   
# MAGIC
# MAGIC However for GTO we cannot distinguish this well as both positive landing rate and negative landing(unsuccessful mission) are both there here.
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### TASK  6: Visualize the launch success yearly trend
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC You can plot a line chart with x axis to be <code>Year</code> and y axis to be average success rate, to get the average launch success trend. 
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC The function will help you get the year from the date:
# MAGIC

# COMMAND ----------

# A function to Extract years from the date 
year=[]
def Extract_year(date):
    for i in df["Date"]:
        year.append(i.split("-")[0])
    return year
    

# COMMAND ----------

# Plot a line chart with x axis to be the extracted year and y axis to be the success rate
year = Extract_year(df['Date'])
df['year'] = year
year_success = df.groupby('year')['Class'].mean().reset_index()
sns.lineplot(x = 'year', y = 'Class', data = year_success)
plt.xlabel("Year", fontsize = 20)
plt.ylabel("Success Rate", fontsize = 20)
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC You can observe that the success rate since 2013 kept increasing till 2017 (stable in 2014) and after 2015 it started increasing.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Features Engineering 
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC By now, you should obtain some preliminary insights about how each important variable would affect the success rate, we will select the features that will be used in success prediction in the future module.
# MAGIC

# COMMAND ----------

features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()

# COMMAND ----------

# MAGIC %md
# MAGIC  ### TASK  7: Create dummy variables to categorical columns
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Use the function <code>get_dummies</code> and <code>features</code> dataframe to apply OneHotEncoder to the column <code>Orbits</code>, <code>LaunchSite</code>, <code>LandingPad</code>, and <code>Serial</code>. Assign the value to the variable <code>features_one_hot</code>, display the results using the method head. Your result dataframe must include all features including the encoded ones.
# MAGIC

# COMMAND ----------

# HINT: Use get_dummies() function on the categorical columns
features_one_hot = pd.get_dummies(features, columns = ['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])
features_one_hot.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ### TASK  8: Cast all numeric columns to `float64`
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Now that our <code>features_one_hot</code> dataframe only contains numbers cast the entire dataframe to variable type <code>float64</code>
# MAGIC

# COMMAND ----------

# HINT: use astype function
features_one_hot = features_one_hot.astype(float)

# COMMAND ----------

# MAGIC %md
# MAGIC We can now export it to a <b>CSV</b> for the next section,but to make the answers consistent, in the next lab we will provide data in a pre-selected date range. 
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <code>features_one_hot.to_csv('dataset_part_3.csv', index=False)</code>
# MAGIC

# COMMAND ----------

features_one_hot.to_csv('/Workspace/Users/jkgonzalezp@gmail.com/Ciencia de datos IBM - Coursera/Applied Data Science Capstone/module_2/dataset_part_3.csv', index=False)

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
# MAGIC <a href="https://www.linkedin.com/in/nayefaboutayoun/">Nayef Abou Tayoun</a> is a Data Scientist at IBM and pursuing a Master of Management in Artificial intelligence degree at Queen's University.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Change Log
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC | Date (YYYY-MM-DD) | Version | Changed By | Change Description      |
# MAGIC | ----------------- | ------- | ---------- | ----------------------- |
# MAGIC | 2021-10-12        | 1.1     | Lakshmi Holla     | Modified markdown |
# MAGIC | 2020-09-20        | 1.0     | Joseph     | Modified Multiple Areas |
# MAGIC | 2020-11-10       | 1.1    | Nayef      | updating the input data |
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Copyright © 2020 IBM Corporation. All rights reserved.
# MAGIC