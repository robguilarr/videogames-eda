# -*- coding: utf-8 -*-
"""
@author: rober
"""

# ----------------------------------------------------------------------------
# Import Packages
# ----------------------------------------------------------------------------


# To manage Dataframes
import pandas as pd
# To manage the Year column
from datetime import datetime as dt
# To manage number operators
import numpy as np
# To manage plots
import matplotlib.pyplot as plt
# Package for more plots
import seaborn as sns


# ----------------------------------------------------------------------------
# Import Data
# ----------------------------------------------------------------------------

# Import data frame of videogames
dfvg = pd.read_csv("data/vgcomplete.csv", na_values=["N/A", "", " "])

# Load IP developer region data, in the original data Publisher was named as developer
region_ipdf = pd.read_csv("data/video-games-developers.csv", na_values=["N/A", "", " "]) \
                .rename(columns={"Developer": "Publisher_ip"})

# Load IP developer region data, in the original data Publisher was named as developer
region_indf = pd.read_csv("data/indie-games-developers.csv", na_values=["N/A", "", " "]) \
                .rename(columns={"Developer": "Publisher_in"})


# ----------------------------------------------------------------------------
## Merge and clean
# ----------------------------------------------------------------------------

# Merge IP data
dfip = pd.merge(dfvg, region_ipdf[["Publisher_ip", "Country", "City"]], left_on="Publisher",
                right_on="Publisher_ip", how="left", suffixes=("_vg", "_y"))

# New column that contains only the first non na value between the same record
dfip["Publisher_f"] = dfip["Publisher"].combine_first(
    dfip["Publisher_ip"]).astype(str)

# Clean non used columns
dfip = dfip.drop(columns=["Publisher", "Publisher_ip"])


# Merge Indie data
dfin = pd.merge(dfip, region_indf[["Publisher_in", "Country", "City"]], left_on="Publisher_f",
                right_on="Publisher_in", how="left", suffixes=(None, "_in"))

# New column that contains only the first non NA value between the same record
dfin["Publisher"] = dfin["Publisher_f"].combine_first(
    dfin["Publisher_in"]).astype(str)
dfin["Country"] = dfin["Country_in"].combine_first(dfin["Country"]).astype(str)
dfin["City"] = dfin["City_in"].combine_first(dfin["City"]).astype(str)

# Clean non used columns
dfin = dfin.drop(
    columns=["Publisher_f", "Publisher_in", "Country_in", "City_in"])

# Reordering data
df = dfin[['Name', 'Year_of_Release', 'Publisher', 'Country', 'City', 'Developer',
           'Platform', 'Genre', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales',
           'Global_Sales', 'Critic_Score', 'Critic_Count', 'User_Score',
           'User_Count', 'Rating']]

# Cleaning memory environment
del dfin
del dfip
del dfvg
del region_indf
del region_ipdf

# ----------------------------------------------------------------------------
# Missing registry games Data
# ----------------------------------------------------------------------------

# Strongest Tokyo University Shogi
df = df.drop(15959)

# Drop missing titles
df = df.dropna(subset=["Name"])

# ----------------------------------------------------------------------------
# Writing Data
# ----------------------------------------------------------------------------

df.to_csv("data/videogames.csv")
