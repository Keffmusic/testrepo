# Databricks notebook source
# MAGIC %md
# MAGIC <p style="text-align:center">
# MAGIC     <a href="https://skills.network" target="_blank">
# MAGIC     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo">
# MAGIC     </a>
# MAGIC </p>
# MAGIC
# MAGIC <h1 align=center><font size = 5>Assignment: SQL Notebook for Peer Assignment</font></h1>
# MAGIC
# MAGIC Estimated time needed: **60** minutes.
# MAGIC
# MAGIC ## Introduction
# MAGIC Using this Python notebook you will:
# MAGIC
# MAGIC 1.  Understand the Spacex DataSet
# MAGIC 2.  Load the dataset  into the corresponding table in a Db2 database
# MAGIC 3.  Execute SQL queries to answer assignment questions 
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Overview of the DataSet
# MAGIC
# MAGIC SpaceX has gained worldwide attention for a series of historic milestones. 
# MAGIC
# MAGIC It is the only private company ever to return a spacecraft from low-earth orbit, which it first accomplished in December 2010.
# MAGIC SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars wheras other providers cost upward of 165 million dollars each, much of the savings is because Space X can reuse the first stage. 
# MAGIC
# MAGIC
# MAGIC Therefore if we can determine if the first stage will land, we can determine the cost of a launch. 
# MAGIC
# MAGIC This information can be used if an alternate company wants to bid against SpaceX for a rocket launch.
# MAGIC
# MAGIC This dataset includes a record for each payload carried during a SpaceX mission into outer space.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Download the datasets
# MAGIC
# MAGIC This assignment requires you to load the spacex dataset.
# MAGIC
# MAGIC In many cases the dataset to be analyzed is available as a .CSV (comma separated values) file, perhaps on the internet. Click on the link below to download and save the dataset (.CSV file):
# MAGIC
# MAGIC  <a href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv" target="_blank">Spacex DataSet</a>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Configurar base de datos SQLite
# MAGIC
# MAGIC Vamos a crear una base de datos SQLite y cargar los datos de SpaceX. Luego usaremos **pandas con `pd.read_sql()`** para ejecutar consultas SQL.

# COMMAND ----------

import sqlite3
import pandas as pd
import os

# Limpiar base de datos previa si existe
if os.path.exists("my_data1.db"):
    os.remove("my_data1.db")

# Crear base de datos y conexión
con = sqlite3.connect("my_data1.db")

# Cargar datos desde CSV
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")

# Crear tabla SPACEXTBL (todos los datos)
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False, method="multi")

# Crear tabla SPACEXTABLE (sin valores nulos en Date)
df_filtered = df[df['Date'].notna()]
df_filtered.to_sql("SPACEXTABLE", con, if_exists='replace', index=False, method="multi")

print(f"✓ SPACEXTBL creada: {len(df)} filas")
print(f"✓ SPACEXTABLE creada: {len(df_filtered)} filas")
print("\n✅ Base de datos lista. Usa pd.read_sql(query, con) para ejecutar consultas SQL")

# COMMAND ----------

# DBTITLE 1,📌 Plantilla para ejecutar SQL
# ========================================
# CÓMO EJECUTAR CONSULTAS SQL CON PANDAS
# ========================================

# Plantilla para ejecutar tus consultas SQL:
"""
query = '''
SELECT columna1, columna2, COUNT(*) as total
FROM SPACEXTABLE
WHERE condicion
GROUP BY columna1, columna2
ORDER BY total DESC
'''

resultado = pd.read_sql(query, con)
display(resultado)
"""

# Ejemplo 1: Ver todas las columnas disponibles
query = "SELECT * FROM SPACEXTABLE LIMIT 3"
resultado = pd.read_sql(query, con)
print("\nEjemplo - Primeras 3 filas:")
display(resultado)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Tasks
# MAGIC
# MAGIC Now write and execute SQL queries to solve the assignment tasks.
# MAGIC
# MAGIC **Note: If the column names are in mixed case enclose it in double quotes
# MAGIC    For Example "Landing_Outcome"**
# MAGIC
# MAGIC ### Task 1
# MAGIC
# MAGIC
# MAGIC
# MAGIC
# MAGIC ##### Display the names of the unique launch sites  in the space mission
# MAGIC

# COMMAND ----------

# Task 1: Display the names of the unique launch sites in the space mission

query = '''
SELECT DISTINCT Launch_Site
FROM SPACEXTABLE
ORDER BY Launch_Site
'''

resultado = pd.read_sql(query, con)
display(resultado)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Task 2
# MAGIC
# MAGIC
# MAGIC #####  Display 5 records where launch sites begin with the string 'CCA' 
# MAGIC

# COMMAND ----------

query = '''
SELECT * 
FROM SPACEXTABLE
WHERE Launch_Site LIKE '%CCA%'
LIMIT 5;
'''

resultado = pd.read_sql(query, con)
display(resultado)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3
# MAGIC
# MAGIC
# MAGIC
# MAGIC
# MAGIC ##### Display the total payload mass carried by boosters launched by NASA (CRS)
# MAGIC

# COMMAND ----------

query = '''
SELECT sum(PAYLOAD_MASS__KG_) as total 
FROM SPACEXTABLE
WHERE Customer = 'NASA (CRS)';
'''

resultado = pd.read_sql(query, con)
display(resultado)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 4
# MAGIC
# MAGIC
# MAGIC
# MAGIC
# MAGIC ##### Display average payload mass carried by booster version F9 v1.1
# MAGIC

# COMMAND ----------

query = '''
SELECT avg(PAYLOAD_MASS__KG_) as mean 
FROM SPACEXTABLE
WHERE Booster_Version = 'F9 v1.1';
'''

resultado = pd.read_sql(query, con)
display(resultado)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 5
# MAGIC
# MAGIC ##### List the date when the first succesful landing outcome in ground pad was acheived.
# MAGIC
# MAGIC
# MAGIC _Hint:Use min function_ 
# MAGIC

# COMMAND ----------

query = '''
SELECT min(Date) as min_date 
FROM SPACEXTABLE
WHERE Landing_Outcome = 'Success';
'''

resultado = pd.read_sql(query, con)
display(resultado)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 6
# MAGIC
# MAGIC ##### List the names of the boosters which have success in drone ship and have payload mass greater than 4000 but less than 6000
# MAGIC

# COMMAND ----------

query = '''
SELECT DISTINCT Landing_Outcome
FROM SPACEXTABLE
ORDER BY Landing_Outcome
'''

resultado = pd.read_sql(query, con)
display(resultado)

# COMMAND ----------

query = '''
SELECT DISTINCT Booster_Version 
FROM SPACEXTABLE
WHERE Landing_Outcome = 'Success (drone ship)'
AND PAYLOAD_MASS__KG_ > 4000 
AND PAYLOAD_MASS__KG_ < 6000
'''

resultado = pd.read_sql(query, con)
display(resultado)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 7
# MAGIC
# MAGIC
# MAGIC
# MAGIC
# MAGIC ##### List the total number of successful and failure mission outcomes
# MAGIC

# COMMAND ----------

query = '''
SELECT Mission_Outcome,
count(Mission_Outcome) as count
FROM SPACEXTABLE
GROUP BY Mission_Outcome
'''

resultado = pd.read_sql(query, con)
display(resultado)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 8
# MAGIC
# MAGIC
# MAGIC
# MAGIC ##### List all the booster_versions that have carried the maximum payload mass, using a subquery with a suitable aggregate function.
# MAGIC

# COMMAND ----------

query = '''
SELECT DISTINCT Booster_Version
FROM SPACEXTABLE
WHERE PAYLOAD_MASS__KG_ = (SELECT max(PAYLOAD_MASS__KG_) FROM SPACEXTABLE)
'''

resultado = pd.read_sql(query, con)
display(resultado)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 9
# MAGIC
# MAGIC
# MAGIC ##### List the records which will display the month names, failure landing_outcomes in drone ship ,booster versions, launch_site for the months in year 2015.
# MAGIC
# MAGIC **Note: SQLLite does not support monthnames. So you need to use  substr(Date, 6,2) as month to get the months and substr(Date,0,5)='2015' for year.**
# MAGIC

# COMMAND ----------

# Task 9: List month, failure landing_outcomes in drone ship, booster versions, launch_site for year 2015

query = '''
SELECT substr(Date, 6, 2) as Month,
       Landing_Outcome,
       Booster_Version,
       Launch_Site
FROM SPACEXTABLE
WHERE substr(Date, 1, 4) = '2015'
  AND Landing_Outcome LIKE '%Failure%'
  AND Landing_Outcome LIKE '%drone ship%'
'''

resultado = pd.read_sql(query, con)
display(resultado)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 10
# MAGIC
# MAGIC
# MAGIC
# MAGIC
# MAGIC ##### Rank the count of landing outcomes (such as Failure (drone ship) or Success (ground pad)) between the date 2010-06-04 and 2017-03-20, in descending order.
# MAGIC

# COMMAND ----------

query = "SELECT * FROM SPACEXTABLE LIMIT 3"
resultado = pd.read_sql(query, con)
print("\nEjemplo - Primeras 3 filas:")
display(resultado)

# COMMAND ----------

query = '''
SELECT Landing_Outcome,
       count(Landing_Outcome) as count
FROM SPACEXTABLE
WHERE Date between '2010-06-04' and '2017-03-20'
GROUP BY Landing_Outcome
Order by count(Landing_Outcome) desc
'''

resultado = pd.read_sql(query, con)
display(resultado)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Reference Links
# MAGIC
# MAGIC * <a href ="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/labs/Lab%20-%20String%20Patterns%20-%20Sorting%20-%20Grouping/instructional-labs.md.html?origin=www.coursera.org">Hands-on Lab : String Patterns, Sorting and Grouping</a>  
# MAGIC
# MAGIC *  <a  href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/labs/Lab%20-%20Built-in%20functions%20/Hands-on_Lab__Built-in_Functions.md.html?origin=www.coursera.org">Hands-on Lab: Built-in functions</a>
# MAGIC
# MAGIC *  <a  href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/labs/Lab%20-%20Sub-queries%20and%20Nested%20SELECTs%20/instructional-labs.md.html?origin=www.coursera.org">Hands-on Lab : Sub-queries and Nested SELECT Statements</a>
# MAGIC
# MAGIC *   <a href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Module%205/DB0201EN-Week3-1-3-SQLmagic.ipynb">Hands-on Tutorial: Accessing Databases with SQL magic</a>
# MAGIC
# MAGIC *  <a href= "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Module%205/DB0201EN-Week3-1-4-Analyzing.ipynb">Hands-on Lab: Analyzing a real World Data Set</a>
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Author(s)
# MAGIC
# MAGIC <h4> Lakshmi Holla </h4>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Other Contributors
# MAGIC
# MAGIC <h4> Rav Ahuja </h4>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <!--
# MAGIC ## Change log
# MAGIC | Date | Version | Changed by | Change Description |
# MAGIC |------|--------|--------|---------|
# MAGIC | 2024-07-10 | 1.1 |Anita Verma | Changed Version|
# MAGIC | 2021-07-09 | 0.2 |Lakshmi Holla | Changes made in magic sql|
# MAGIC | 2021-05-20 | 0.1 |Lakshmi Holla | Created Initial Version |
# MAGIC -->
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## <h3 align="center"> © IBM Corporation 2021. All rights reserved. <h3/>
# MAGIC