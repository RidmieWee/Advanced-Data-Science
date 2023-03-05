# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 11:21:11 2023

@author: Ridmi Weerakotuwa
"""

# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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


# create function for plot line chart
def plot_line_chart(df):
    """ This ia a function to create a lineplot with multiple lines.
    This function takes datafrme as an argument, and use year as x axis
    and the total gdp as y axis and plot lines for each reagion"""

    # create dataframes for plot line graph
    df_asia = df[df["region_name"] == "Asia"]
    df_usa = df[df["region_name"] == "Americas"]
    df_africa = df[df["region_name"] == "Africa"]
    df_europe = df[df["region_name"] == "Europe"]
    df_oceania = df[df["region_name"] == "Oceania"]

    # make the figure
    plt.figure()

    # use multiple x and y for plot multiple graphs
    plt.plot(df_asia["year"], df_asia["total_gdp"], label="Asia")
    plt.plot(df_usa["year"], df_usa["total_gdp"], label="USA")
    plt.plot(df_africa["year"], df_africa["total_gdp"], label="Africa")
    plt.plot(df_europe["year"], df_europe["total_gdp"], label="Europe")
    plt.plot(df_oceania["year"], df_oceania["total_gdp"], label="Oceania")

    # labeling
    plt.xlabel("Year")
    plt.ylabel("Total GDP")

    # add a title and legend
    plt.title("Total GDP by region ")
    plt.legend()

    # save the plot as png
    plt.savefig("line_chart.png")

    # show the plot
    plt.show()

    return


# create a function for bar chart
def plot_bar_graph(df):
    """ This ia a function to create a grouped bar chart.
    This function takes datafrme as anargument, and plot
    multiple bars grouped by year. """

    # create dataframes for plot bar graph
    df_high = df[df["income_group"] == "High"]
    df_low = df[df["income_group"] == "Low"]
    df_low_mid = df[df["income_group"] == "Lower middle"]
    df_upper_mid = df[df["income_group"] == "Upper middle"]

    # make the figure
    plt.figure()

    # create the position of bars
    x_pos = np.arange(len(df_upper_mid))

    # create x labels
    tick_labels = ["2017", "2018", "2019", "2020", "2021"]

    # plot the bars
    plt.bar(x_pos - 0.2,
            df_high["population(million)"],
            width=0.2,
            label='High')
    plt.bar(x_pos,
            df_low["population(million)"],
            width=0.2,
            label='Low')
    plt.bar(x_pos + 0.2,
            df_low_mid["population(million)"],
            width=0.2,
            label='Lower middle')
    plt.bar(x_pos + 0.4,
            df_upper_mid["population(million)"],
            width=0.2,
            label='Upper middle')

    # labeling
    plt.xlabel("Year")
    plt.ylabel("Population (million)")
    plt.xticks(x_pos, tick_labels)

    # add the title and legends
    plt.title("Total population by income group")
    plt.legend(loc='center left',
               bbox_to_anchor=(1, 0.5),
               fancybox=True,
               shadow=True)

    # save the figure as png
    plt.savefig("bar_chart.png")

    # show the plot
    plt.show()

    return


# create a fucntion for boxplots
def plot_boxplot(df):
    """ This ia a function to create boxplot. This function takes datafrme
    as an argument, and plot multiple boxplots for each region. """

    # select useful columns for plot boxplot
    df_pop_growth = df[["region_name",
                        "growth_populaion(%)"]].reset_index(drop=True)

    # create pivot table using selected columns
    df_pop_growth_pivot = df_pop_growth.pivot(columns="region_name",
                                              values="growth_populaion(%)")

    # make the figure
    plt.figure()

    # plot the boxplots without outliers
    df_pop_growth_pivot.plot(kind='box', showfliers=0)

    # labeling and add title
    plt.xlabel("Region")
    plt.ylabel("Population growth rate")
    plt.title("Distribution of population growth rate by region")

    # save the plot as png
    plt.savefig("bxplot.png")

    # show the plot
    plt.show()

    # get the Q1 and Q3 for futher analysis
    lk = df_pop_growth.groupby('region_name').agg([('Upper', lambda x: x.quantile(.75)),
                                                   ('Lower', lambda x: x.quantile(.25))])
    lk.columns = [f"{b}_{a}" for a, b in lk.columns]

    # print the result
    print(lk)

    return


# transform the populations table seperate years columns into one year column
df_population_new = pd.melt(df_population,
                            id_vars=["Country Name",
                                     "Country Code",
                                     "Indicator Name",
                                     "Indicator Code"],
                            value_vars=df_population.iloc[:, 4:-1].columns,
                            var_name="Year",
                            value_name=("Population"))

# explore the new dataframe
print(df_population_new.head())

# remove nan row in population column
df_population_new = df_population_new.dropna(subset=['Population'])

# create two simmilar columns to merge population and countries data
df_population_new["new"] = df_population_new["Country Code"] + \
    "-" + df_population_new["Year"]
df_countries["new"] = df_countries["country_code"].astype(
    str) + "-" + df_countries["year"].astype(str)

# merge population and country data
df_world_pop = df_population_new.merge(df_countries,
                                       left_on=("new"),
                                       right_on=("new"),
                                       how="inner")
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

# explore the chaanges
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

# create a column to calculate population growth rate
df_world_pop["growth_populaion(%)"] = df_world_pop.groupby(['country_name'],
                                                           group_keys=False)['Population'].pct_change()*100

# remove nan row in population growth column
df_world_pop = df_world_pop.dropna(subset=['growth_populaion(%)'])

# explore the new column
print(df_world_pop.info())

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

# create new dataframe containing only last 5 years data
df_world_income_5 = df_world_income[df_world_income["year"].isin(
    [2017, 2018, 2019, 2020, 2021])]

# explore the dataframe
print(df_world_income_5[["year", "income_group", "population(million)"]])


# call the funtions for plot graphs
plot_line_chart(df_region_gdp)
plot_bar_graph(df_world_income_5)
plot_boxplot(df_world_pop)
