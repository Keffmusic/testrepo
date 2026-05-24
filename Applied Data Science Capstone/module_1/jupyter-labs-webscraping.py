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
# MAGIC # **Space X  Falcon 9 First Stage Landing Prediction**
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Web scraping Falcon 9 and Falcon Heavy Launches Records from Wikipedia
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Estimated time needed: **40** minutes
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC In this lab, you will be performing web scraping to collect Falcon 9 historical launch records from a Wikipedia page titled `List of Falcon 9 and Falcon Heavy launches`
# MAGIC
# MAGIC https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_1_L2/images/Falcon9_rocket_family.svg)
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
# MAGIC More specifically, the launch records are stored in a HTML table shown below:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_1_L2/images/falcon9-launches-wiki.png)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC   ## Objectives
# MAGIC Web scrap Falcon 9 launch records with `BeautifulSoup`: 
# MAGIC - Extract a Falcon 9 launch records HTML table from Wikipedia
# MAGIC - Parse the table and convert it into a Pandas data frame
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC First let's import required packages for this lab
# MAGIC

# COMMAND ----------

!pip3 install beautifulsoup4
#!pip3 install requests

# COMMAND ----------

import sys

import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd

# COMMAND ----------

# MAGIC %md
# MAGIC and we will provide some helper functions for you to process web scraped HTML table
# MAGIC

# COMMAND ----------

def date_time(table_cells):
    """
    This function returns the data and time from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    """
    This function returns the booster version from the HTML  table cell 
    Input: the  element of a table data cell extracts extra row
    """
    out=''.join([booster_version for i,booster_version in enumerate( table_cells.strings) if i%2==0][0:-1])
    return out

def landing_status(table_cells):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    out=[i for i in table_cells.strings][0]
    return out


def get_mass(table_cells):
    mass=unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass=mass[0:mass.find("kg")+2]
    else:
        new_mass=0
    return new_mass


def extract_column_from_header(row):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    if (row.br):
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
        
    colunm_name = ' '.join(row.contents)
    
    # Filter the digit and empty names
    if not(colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name    


# COMMAND ----------

# MAGIC %md
# MAGIC To keep the lab tasks consistent, you will be asked to scrape the data from a snapshot of the  `List of Falcon 9 and Falcon Heavy launches` Wikipage updated on
# MAGIC `9th June 2021`
# MAGIC

# COMMAND ----------

static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}

# COMMAND ----------

# MAGIC %md
# MAGIC Next, request the HTML page from the above URL and get a `response` object
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### TASK 1: Request the Falcon9 Launch Wiki page from its URL
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC First, let's perform an HTTP GET method to request the Falcon9 Launch HTML page, as an HTTP response.
# MAGIC

# COMMAND ----------

# use requests.get() method with the provided static_url and headers
# assign the response to a object
requests.get(static_url, headers=headers)

# COMMAND ----------

# MAGIC %md
# MAGIC Create a `BeautifulSoup` object from the HTML `response`
# MAGIC

# COMMAND ----------

# Use BeautifulSoup() to create a BeautifulSoup object from a response text content
soup = BeautifulSoup(requests.get(static_url, headers=headers).text, 'html.parser')

# COMMAND ----------

# MAGIC %md
# MAGIC Print the page title to verify if the `BeautifulSoup` object was created properly 
# MAGIC

# COMMAND ----------

# Use soup.title attribute
soup.title

# COMMAND ----------

# MAGIC %md
# MAGIC ### TASK 2: Extract all column/variable names from the HTML table header
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Next, we want to collect all relevant column names from the HTML table header
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Let's try to find all tables on the wiki page first. If you need to refresh your memory about `BeautifulSoup`, please check the external reference link towards the end of this lab
# MAGIC

# COMMAND ----------

# Use the find_all function in the BeautifulSoup object, with element type `table`
# Assign the result to a list called `html_tables`
html_tables = soup.find_all('table')

# COMMAND ----------

# MAGIC %md
# MAGIC Starting from the third table is our target table contains the actual launch records.
# MAGIC

# COMMAND ----------

# Let's print the third table and check its content
first_launch_table = html_tables[2]
print(first_launch_table)

# COMMAND ----------

# MAGIC %md
# MAGIC You should able to see the columns names embedded in the table header elements `<th>` as follows:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC <tr>
# MAGIC <th scope="col">Flight No.
# MAGIC </th>
# MAGIC <th scope="col">Date and<br/>time (<a href="/wiki/Coordinated_Universal_Time" title="Coordinated Universal Time">UTC</a>)
# MAGIC </th>
# MAGIC <th scope="col"><a href="/wiki/List_of_Falcon_9_first-stage_boosters" title="List of Falcon 9 first-stage boosters">Version,<br/>Booster</a> <sup class="reference" id="cite_ref-booster_11-0"><a href="#cite_note-booster-11">[b]</a></sup>
# MAGIC </th>
# MAGIC <th scope="col">Launch site
# MAGIC </th>
# MAGIC <th scope="col">Payload<sup class="reference" id="cite_ref-Dragon_12-0"><a href="#cite_note-Dragon-12">[c]</a></sup>
# MAGIC </th>
# MAGIC <th scope="col">Payload mass
# MAGIC </th>
# MAGIC <th scope="col">Orbit
# MAGIC </th>
# MAGIC <th scope="col">Customer
# MAGIC </th>
# MAGIC <th scope="col">Launch<br/>outcome
# MAGIC </th>
# MAGIC <th scope="col"><a href="/wiki/Falcon_9_first-stage_landing_tests" title="Falcon 9 first-stage landing tests">Booster<br/>landing</a>
# MAGIC </th></tr>
# MAGIC ```
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Next, we just need to iterate through the `<th>` elements and apply the provided `extract_column_from_header()` to extract column name one by one
# MAGIC

# COMMAND ----------

column_names = []
for th in first_launch_table.find_all('th'):
    name = extract_column_from_header(th)
    column_names.append(name)
    if name is not None and len(name) > 0:
        column_names.append(name)

# Apply find_all() function with `th` element on first_launch_table
# Iterate each th element and apply the provided extract_column_from_header() to get a column name
# Append the Non-empty column name (`if name is not None and len(name) > 0`) into a list called column_names


# COMMAND ----------

# MAGIC %md
# MAGIC Check the extracted column names
# MAGIC

# COMMAND ----------

print(column_names)

# COMMAND ----------

# MAGIC %md
# MAGIC ## TASK 3: Create a data frame by parsing the launch HTML tables
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC We will create an empty dictionary with keys from the extracted column names in the previous task. Later, this dictionary will be converted into a Pandas dataframe
# MAGIC

# COMMAND ----------

launch_dict= dict.fromkeys(column_names)

# Remove an irrelvant column
del launch_dict['Date and time ( )']

# Let's initial the launch_dict with each value to be an empty list
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
# Added some new columns
launch_dict['Version Booster']=[]
launch_dict['Booster landing']=[]
launch_dict['Date']=[]
launch_dict['Time']=[]

# COMMAND ----------

# MAGIC %md
# MAGIC Next, we just need to fill up the `launch_dict` with launch records extracted from table rows.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Usually, HTML tables in Wiki pages are likely to contain unexpected annotations and other types of noises, such as reference links `B0004.1[8]`, missing values `N/A [e]`, inconsistent formatting, etc.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC To simplify the parsing process, we have provided an incomplete code snippet below to help you to fill up the `launch_dict`. Please complete the following code snippet with TODOs or you can choose to write your own logic to parse all launch tables:
# MAGIC

# COMMAND ----------

extracted_row = 0
#Extract each table 
for table_number,table in enumerate(soup.find_all('table',"wikitable plainrowheaders collapsible")):
   # get table row 
    for rows in table.find_all("tr"):
        #check to see if first table heading is as number corresponding to launch a number 
        if rows.th:
            if rows.th.string:
                flight_number=rows.th.string.strip()
                flag=flight_number.isdigit()
        else:
            flag=False
        #get table element 
        row=rows.find_all('td')
        #if it is number save cells in a dictonary 
        if flag:
            extracted_row += 1
            # Flight Number value
            # TODO: Append the flight_number into launch_dict with key `Flight No.`
            launch_dict['Flight No.'].append(flight_number)
            #print(flight_number)
            datatimelist=date_time(row[0])
            
            # Date value
            # TODO: Append the date into launch_dict with key `Date`
            date = datatimelist[0].strip(',')
            launch_dict['Date'].append(date)
            #print(date)
            
            # Time value
            # TODO: Append the time into launch_dict with key `Time`
            time = datatimelist[1]
            launch_dict['Time'].append(time)
            #print(time)
              
            # Booster version
            # TODO: Append the bv into launch_dict with key `Version Booster`
            bv=booster_version(row[1])
            if not(bv):
                bv=row[1].a.string
            launch_dict['Version Booster'].append(bv)
            #print(bv)
            
            # Launch Site
            # TODO: Append the launch_site into launch_dict with key `Launch Site`
            launch_site = row[2].a.string if row[2].a else row[2].text.strip()
            launch_dict['Launch site'].append(launch_site)
            #print(launch_site)
            
            # Payload
            # TODO: Append the payload into launch_dict with key `Payload`
            payload = row[3].a.string if row[3].a else row[3].text.strip()
            launch_dict['Payload'].append(payload)
            #print(payload)
            
            # Payload Mass
            # TODO: Append the payload_mass into launch_dict with key `Payload mass`
            payload_mass = get_mass(row[4])
            launch_dict['Payload mass'].append(payload_mass)
            #print(payload_mass)
            
            # Orbit
            # TODO: Append the orbit into launch_dict with key `Orbit`
            orbit = row[5].a.string if row[5].a else row[5].text.strip()
            launch_dict['Orbit'].append(orbit)
            #print(orbit)
            
            # Customer
            # TODO: Append the customer into launch_dict with key `Customer`
            customer = row[6].a.string if row[6].a else row[6].text.strip()
            launch_dict['Customer'].append(customer)
            #print(customer)
            
            # Launch outcome
            # TODO: Append the launch_outcome into launch_dict with key `Launch outcome`
            launch_outcome = list(row[7].strings)[0]
            launch_dict['Launch outcome'].append(launch_outcome)
            #print(launch_outcome)
            
            # Booster landing
            # TODO: Append the booster_landing into launch_dict with key `Booster landing`
            booster_landing = landing_status(row[8])
            launch_dict['Booster landing'].append(booster_landing)
            #print(booster_landing)

# COMMAND ----------

# MAGIC %md
# MAGIC After you have fill in the parsed launch record values into `launch_dict`, you can create a dataframe from it.
# MAGIC

# COMMAND ----------

df= pd.DataFrame({ key:pd.Series(value) for key, value in launch_dict.items() })

# COMMAND ----------

df.head()

# COMMAND ----------

# MAGIC %md
# MAGIC We can now export it to a <b>CSV</b> for the next section, but to make the answers consistent and in case you have difficulties finishing this lab. 
# MAGIC
# MAGIC Following labs will be using a provided dataset to make each lab independent. 
# MAGIC

# COMMAND ----------

df.to_csv('/Workspace/Users/jkgonzalezp@gmail.com/Ciencia de datos IBM - Coursera/Applied Data Science Capstone/module_1/spacex_web_scraped.csv', index=False)

# COMMAND ----------

# MAGIC %md
# MAGIC <code>df.to_csv('spacex_web_scraped.csv', index=False)</code>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Authors
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <a href="https://www.linkedin.com/in/yan-luo-96288783/">Yan Luo</a>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <a href="https://www.linkedin.com/in/nayefaboutayoun/">Nayef Abou Tayoun</a>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <!--
# MAGIC ## Change Log
# MAGIC -->
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <!--
# MAGIC | Date (YYYY-MM-DD) | Version | Changed By | Change Description      |
# MAGIC | ----------------- | ------- | ---------- | ----------------------- |
# MAGIC | 2021-06-09        | 1.0     | Yan Luo    | Tasks updates           |
# MAGIC | 2020-11-10        | 1.0     | Nayef      | Created the initial version |
# MAGIC -->
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Copyright © 2021 IBM Corporation. All rights reserved.
# MAGIC