import pandas as pd
import numpy as np
from pathlib import Path

from verify_work_dir import verify_work_dir

def _export_yearly(file: str, begin: int, end: int):
    """Import given file, separate and transpose data for each year, then export each yearly data as CSV.

    Args:
        file (str): BEA Economics file to read in
        begin (int): Beginning year of data
        end (int): Ending year of data
    """
    #Importing file as Pandas df
    df = pd.read_csv(file, sep=',', header=None)
    
    #Identify year span
    year_range = end - begin + 1
    
    #Remove unecessary rows
    df = df[df.iloc[:, 1].notna()]
    df = df[df.iloc[:, 1].str.match('(.*, PA)|GeoName')]
    df.reset_index(drop=True, inplace=True)
    df.columns = df.iloc[0, :]
    df = df.iloc[1:, :]
    df.reset_index(drop=True, inplace=True)

    #Create base directory if it does not already exist
    base_dir = './PASS_Data/Econ/Yearly'
    Path(base_dir).mkdir(parents=True, exist_ok=True)


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
        
        #NOTE: FIX (Consider better ways to get this info into dataset) <--- Isolates FIPS and County name columns
        id_cols = df.iloc[lambda x: x.index % 35 == 0, 0:2]
        id_cols.reset_index(drop=True, inplace=True)
        fips_col = id_cols.iloc[:, 0]
        county_col = id_cols.iloc[:, 1]

        #Add county column and FIPS columns back to dataframe
        yearly_df.insert(0, "GeoFIPS", fips_col)
        yearly_df.insert(0, "GeoName", county_col)

        #Export csv for each county separately
        yearly_df.to_csv(f"{base_dir}/{year}.csv", index=False)
        print(year)

def econ_year_filter(files: list[str] = ['./Raw_Data/Econ_Files/Economy_Income_2003-2010.csv',
                                         './Raw_Data/Econ_Files/Economy_Income_2010-2019.csv'],
                     years: list[tuple[int, int]] = [(2003, 2010), (2010, 2019)]):
    """Import, clean, and separate BEA Economics data from given files.

    Args:
        files (list[str], optional): Files to read in. Defaults to ['./Raw_Data/Econ_Files/Economy_Income_2003-2010.csv', 
                                                                    './Raw_Data/Econ_Files/Economy_Income_2010-2019.csv'].
        years (list[tuple[int, int]], optional): Correlating beginning and end years for each file.
                                                 Defaults to [(2003, 2010), (2010, 2019)].
    """
    #Verify working directory
    verify_work_dir(__file__)
    
    try:
        for index, file in enumerate(files):
            begin, end = years[index]
            _export_yearly(file, begin, end)
    except FileNotFoundError as e:
        print("Given BEA Econ files not found...Exiting")
        exit(1)
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    files = ['./Raw_Data/Econ_Files/Economy_Income_2003-2010.csv',
             './Raw_Data/Econ_Files/Economy_Income_2010-2019.csv']
    years = [(2003, 2010), (2010, 2019)]
    econ_year_filter(files, years)