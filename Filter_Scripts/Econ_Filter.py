import pandas as pd
import numpy as np
import re
from os.path import exists, dirname, abspath
from os import mkdir, chdir, getcwd
import os

#Set working dir
workDir = dirname(dirname(abspath(__file__)))
chdir(workDir)

#Verify working dir
verify = input("Working dir is '" + getcwd() + "'. Proceed? (Y/N): ")
if (not (verify == 'Y' or verify == 'y')):
    print('Exiting...')
    exit(1)

#Read in data file (csv)
df = pd.read_csv('./Raw_data/Econ_Files/Economy_Income_2010-2019.csv', header=None)

#Remove unecessary rows
df = df[df.iloc[:, 1].notna()]
df = df[df.iloc[:, 1].str.match('(.*, PA)|GeoName')]
df.reset_index(drop=True, inplace=True)
df.columns = df.iloc[0, :]
df = df.iloc[1:, :]
df.reset_index(drop=True, inplace=True)
# print(df)


base_file_path = './PASS_Data/Econ'
#Check if directory exists; if not, create new dir
if (not exists(base_file_path)):
    mkdir(base_file_path)


counties_list = []
counter = 0
for i in range(67):
    #Isolate each county's data
    county_df = df.iloc[counter:(counter+35), 3:]
    county_df.set_index("Description", inplace=True)

    #Transpose the table and ensure year(s) are included
    counties_list.append(county_df.transpose())
    counties_list[i].rename_axis(index="Year", columns="Variables", inplace=True)
    counties_list[i].reset_index(inplace=True)

    #NOTE: FIX (Consider better ways to get this info into dataset) <---- Isolates FIPS and County name columns
    id_cols = df.iloc[counter:(counter+11), 0:2]
    id_cols.reset_index(drop=True, inplace=True)
    fips_col = id_cols.iloc[:, 0]
    county_col = id_cols.iloc[:, 1]
    county_name = str(county_col[0]).replace(', PA', "") #Get county name for csv file name

    #Add county column and FIPS columns back to dataframe
    # counties_list[i].insert(0, "GeoFIPS", fips_col)
    # counties_list[i].insert(0, "GeoName", county_col)

    #Export csv for each county separately
    counties_list[i].to_csv(base_file_path + "/" + county_name + ".csv", index=False)

    #Each county has 35 rows of data
    counter += 35

print ("Done")