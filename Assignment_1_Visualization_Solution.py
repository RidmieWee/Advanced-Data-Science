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

# load population data into dataframe
df_population = pd.read_csv("Population.csv")

# explore the first rows
print(df_countries.head())
print(df_population.head())

# explore the information about data
print(df_countries.info())
print(df_population.info())

# transform the populations table seperate years columns into one year column
df_population_new = pd.melt(df_population,
                        id_vars = ["Country Name",
                                   "Country Code",
                                   "Indicator Name",
                                   "Indicator Code"],
                        value_vars = df_population.iloc[:, 4:-1].columns,
                        var_name = "Year",
                        value_name = ("Population"))

# explore the new dataframe
print(df_population_new.head())

# create two simmilar columns to merge population and countries data
df_population_new["new"] = df_population_new["Country Code"] + "-" + df_population_new["Year"]
df_countries["new"] = df_countries["country_code"].astype(str) + "-" + df_countries["year"].astype(str)

# merge population and country data
df_world_pop = df_population_new.merge(df_countries,
                                       left_on = ("new"),
                                       right_on = ("new"),
                                       how = "inner")
# explore the new dataframe
print(df_world_pop.info())

# select usefull columns
df_world_pop = df_world_pop[["country_name",
                             "country_code",
                             "year",
                             "Population",
                             "region_name",
                             "income_group",
                             "total_gdp",
                             "total_gdp_million",
                             "gdp_variation"]]

# add new column
df_world_pop["population(million)"] = df_world_pop["Population"]/1000000
print(df_world_pop.info())

# explore the unique income groups
print(df_world_pop["income_group"].unique())

# change spanish terms in income group to english terms
df_world_pop["income_group"] = df_world_pop["income_group"].replace(["Ingreso alto",
                                                                     "Países de ingreso bajo",
                                                                     "Países de ingreso mediano bajo",
                                                                     "Ingreso mediano alto",
                                                                     "No clasificado"],
                                                                    ["High",
                                                                     "Low",
                                                                     "Lower middle",
                                                                     "Upper middle",
                                                                     "Other"])

# explore the changes
print(df_world_pop["income_group"].unique())

# group the data using year and region
df_region_gdp = df_world_pop\
                .groupby(["region_name", "year"])[["gdp_variation", "total_gdp"]]\
                .sum().reset_index()

# explore the new dataframe
print(df_region_gdp)

# group the data using year and income group
df_world_income = df_world_pop[df_world_pop["income_group"] != "Other"]\
                .groupby(["income_group", "year"])[["population(million)", "total_gdp"]]\
                .sum().reset_index()

# explore the new dataframe
print(df_world_income)

# create new dataframe containing only last 6 years data
df_world_income_5 = df_world_income[df_world_income["year"].isin([2015, 2016, 2017, 2018, 2019, 2020, 2021])]

#explore the dataframe
print(df_world_income_5[["year","income_group","population(million)"]])

# create dataframes for plot line graph
df_asia = df_region_gdp[df_region_gdp["region_name"]=="Asia"]
df_usa = df_region_gdp[df_region_gdp["region_name"]=="Americas"]
df_africa = df_region_gdp[df_region_gdp["region_name"]=="Africa"]
df_europe = df_region_gdp[df_region_gdp["region_name"]=="Europe"]
df_oceania = df_region_gdp[df_region_gdp["region_name"]=="Oceania"]

# create function for plot line chart
def plot_line_chart():
    """ plot the line graph using above created data frames """

    plt.figure()

    plt.plot(df_asia["year"], df_asia["total_gdp"], label = "Asia")
    plt.plot(df_usa["year"], df_usa["total_gdp"], label = "USA")
    plt.plot(df_africa["year"], df_africa["total_gdp"], label = "Africa")
    plt.plot(df_europe["year"], df_europe["total_gdp"], label = "Europe")
    plt.plot(df_oceania["year"], df_oceania["total_gdp"], label = "Oceania")

    plt.xlabel("Year")
    plt.ylabel("Total GDP")
    plt.title("Total GDP by continents ")
    plt.legend()

    plt.savefig("line_chart.png")
    plt.show()

# call the plot_line_chart function
plot_line_chart()

# create dataframes for plot bar graph
df_high = df_world_income_5[df_world_income_5["income_group"]=="High"]
df_low = df_world_income_5[df_world_income_5["income_group"]=="Low"]

# create a function for bar chart
def plot_bar_graph(x,y):
    """ plot the bar graph using given parameters """

    plt.figure()

    plt.bar(df_high["year"], df_high["population(million)"], color=["#003f5c", "#58508d", "#bc5090", "#ff6361", "#ffa600"])

    plt.xlabel("Income group")
    plt.ylabel("Population (million)")
    plt.xticks(rotation = 90)
    plt.title("Total population by income group")

    plt.savefig("bar_chart.png")
    plt.show()

# call the function
plot_bar_graph(df_world_income_5["income_group"], df_world_income_5["population(million)"])

# create a function for histogram
def plot_histogram():
    plt.figure()

    plt.hist(df_asia["gdp_variation"], bins=5, label = "Asia", density = (True), alpha = 0.7)
    plt.hist(df_africa["gdp_variation"], bins=5, label = "Africa", density = (True), alpha = 0.7)

    plt.xlabel("h")
    plt.show()

#plot_histogram()

