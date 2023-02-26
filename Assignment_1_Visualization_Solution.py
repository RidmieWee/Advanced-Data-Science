# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 11:21:11 2023

@author: Ridmi Weerakotuwa
"""

# import libraries
import pandas as pd
import matplotlib.pyplot as plt

# load country data into dataframe
df_countries = pd.read_csv("C:/Users/Ridmi Weerakotuwa/OneDrive - University of Hertfordshire/UH/ADS/Assignment 1/Advanced-Data-Science/Countries_gdp.csv", sep=";")

# load organization data into dataframe
df_organization = pd.read_csv("C:/Users/Ridmi Weerakotuwa/OneDrive - University of Hertfordshire/UH/ADS/Assignment 1/Advanced-Data-Science/Organization_gdp.csv")

# load population data into dataframe
df_population = pd.read_csv("C:/Users/Ridmi Weerakotuwa/OneDrive - University of Hertfordshire/UH/ADS/Assignment 1/Advanced-Data-Science/Population.csv")

# explore the first rows
print(df_countries.head())
print(df_organization.head())
print(df_population.head())

# explore the information about data
print(df_countries.info())
print(df_organization.info())
print(df_population.info())

# transform the populations table seperate years columns into one year column
df_population = pd.melt(df_population,
                        id_vars = ["Country Name",
                                   "Country Code",
                                   "Indicator Name",
                                   "Indicator Code"],
                        value_vars = df_population.iloc[:, 4:-1].columns,
                        var_name = "Year",
                        value_name = ("total"))

# explore the new dataframe
print(df_population.head())

# rename the total column into population
df_population = df_population.rename(columns = {"total": "Population"})
print(df_population.info())


df_china = df_population[df_population["Country Name"]=="China"]
df_india = df_population[df_population["Country Name"]=="India"]

print(df_china)

plt.figure()
plt.plot(df_china["Year"], df_china["Population"], label = "China")
plt.plot(df_india["Year"], df_india["Population"], label = "India")
plt.xscale(value="linear")

plt.xlabel("Year")
plt.ylabel("GDP (2015 $)")
plt.legend()
plt.show()


