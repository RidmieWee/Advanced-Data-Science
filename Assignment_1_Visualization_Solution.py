# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 11:21:11 2023

@author: Ridmi Weerakotuwa
"""

# import libraries
import pandas as pd
import matplotlib.pyplot as plt

# load country data into dataframe
df_countries = pd.read_csv("Countries_gdp.csv", sep=";")

# explore the first rows
print(df_countries.head())

# explore the information about data
print(df_countries.info())

# create dataframes for plot line graph
df_china = df_countries[df_countries["country_name"]=="China"]
df_usa = df_countries[df_countries["country_name"]=="United States of America"]
df_japan = df_countries[df_countries["country_name"]=="Japan"]
df_germany = df_countries[df_countries["country_name"]=="Germany"]
df_uk = df_countries[df_countries["country_name"]=="United Kingdom of Great Britain and Northern Ireland"]

# explore the new dataframes
print(df_china)
print(df_usa)
print(df_japan)
print(df_germany)
print(df_uk)

# create function for plot line chart
def make_line_chart():
    """ plot the line graph using above created data frames """

    plt.figure()

    plt.plot(df_china["year"], df_china["total_gdp"], label = "China")
    plt.plot(df_usa["year"], df_usa["total_gdp"], label = "USA")
    plt.plot(df_japan["year"], df_japan["total_gdp"], label = "Japan")
    plt.plot(df_germany["year"], df_germany["total_gdp"], label = "Germany")
    plt.plot(df_uk["year"], df_uk["total_gdp"], label = "UK")

    plt.xlabel("Year")
    plt.ylabel("Total GDP")
    plt.title("Total GDP disribution per year ")
    plt.legend()

    plt.savefig("line_chart.png")
    plt.show()

# call the make_line_chart function
make_line_chart()

print(df_countries["income_group"].unique())




