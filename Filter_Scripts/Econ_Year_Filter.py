from os.path import exists, dirname, abspath
from os import mkdir, chdir, getcwd

import pandas as pd
import numpy as np


def verify_work_dir():
    """Set the working directory to one level above this file's directory, then verify with user."""
    #Set working dir
    workDir = dirname(dirname(abspath(__file__)))
    chdir(workDir)

    #Verify working dir
    verify = input("Working dir is '" + getcwd() + "'. Proceed? (Y/N): ")
    if (not (verify == 'Y' or verify == 'y')):
        verify = input("Change work dir? (Y|N): ")
        if (verify == 'Y' or verify == 'y'):
            workDir = input("Enter new work dir: ")
            if (not exists(workDir)):
                print("Dir entered does not exist...exiting")
                exit(1)
            chdir(workDir)
        else:
            print("Exiting...")
            exit(1)



def exportYearly(df, begin, end):
    """Import BEA Economics File, separate and transpose data for each year, then export each yearly data as CSV.

    Args:
        df (Pandas Dataframe): Pandas DF with Economics data
        begin (int): Beginning year of data
        end (int): Ending year of data
    """
    #Identify year span
    year_range = end - begin + 1
    
    #Remove unecessary rows
    df = df[df.iloc[:, 1].notna()]
    df = df[df.iloc[:, 1].str.match('(.*, PA)|GeoName')]
    df.reset_index(drop=True, inplace=True)
    df.columns = df.iloc[0, :]
    df = df.iloc[1:, :]
    df.reset_index(drop=True, inplace=True)

    #Check if directory exists; if not, create new dir
    base_file_path = './PASS_Data/Econ/Yearly'
    if (not exists(base_file_path)):
        mkdir(base_file_path)


    for i in range(year_range):
        counties_list = []
        counter = 0
        for j in range (67):
            #Isolate each county's data
            county_df = df.iloc[counter:counter+35, [3, 4 + i]]
            county_df.set_index("Description", inplace=True)

            #Transpose the table and ensure year(s) are included
            counties_list.append(county_df.transpose())
            counties_list[j].rename_axis(columns="Variables", inplace=True)
            
            #Drop year column
            counties_list[j].reset_index(drop=True, inplace=True)

            #Each county has 35 rows of data
            counter += 35

        year = begin + i
        yearly_df = pd.concat([counties_list[k] for k in range (67)])
        yearly_df.reset_index(drop=True, inplace=True)
        
        #NOTE: FIX (Consider better ways to get this info into dataset) <---- Isolates FIPS and County name columns
        id_cols = df.iloc[lambda x: x.index % 35 == 0, 0:2]
        id_cols.reset_index(drop=True, inplace=True)
        fips_col = id_cols.iloc[:, 0]
        county_col = id_cols.iloc[:, 1]

        #Add county column and FIPS columns back to dataframe
        yearly_df.insert(0, "GeoFIPS", fips_col)
        yearly_df.insert(0, "GeoName", county_col)

        #Export csv for each county separately
        yearly_df.to_csv(f"{base_file_path}/{year}.csv", index=False)
        print(year)


#Read in data file (csv)
if __name__ == "__main__":
    verify_work_dir()
    df = pd.read_csv('./Raw_Data/Econ_Files/Economy_Income_2003-2010.csv', sep=",", header=None)
    exportYearly(df, 2003, 2010)
    df = pd.read_csv('./Raw_Data/Econ_Files/Economy_Income_2010-2019.csv', sep=',', header=None)
    exportYearly(df, 2010, 2019)
    print("-----Done-----")