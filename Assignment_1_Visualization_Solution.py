# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 11:21:11 2023

@author: Ridmi Weerakotuwa
"""

# import libraries
import pandas as pd
import matplotlib.pyplot as plt

# load country data into dataframe
df_countries = pd.read_csv("C:/Users/Ridmi Weerakotuwa/OneDrive - University of Hertfordshire/UH/ADS/Assignment 1/Advanced-Data-Science/countries_gdp_hist.csv", sep=";")

# load country data into dataframe
df_organization = pd.read_csv("C:/Users/Ridmi Weerakotuwa/OneDrive - University of Hertfordshire/UH/ADS/Assignment 1/Advanced-Data-Science/organizations_gdp_hist.csv")

# get the first rows
print(df_countries.head())
print(df_organization.head())

# get the information about data
print(df_countries.info())
print(df_organization.info())


