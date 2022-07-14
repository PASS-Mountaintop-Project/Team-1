from os import listdir
import re

#Third party
import pandas as pd
import numpy as np
from tqdm import tqdm
from pathlib import Path

#Local function
from verify_work_dir import verify_work_dir


#TYPE;FULLCODE;STATE;COUNTY;TRACT;BLOCK;PLACE;COUSUB;CONCITY;AIANNH;SHEETS
#Block;420010301011000;42;001;301.01;1000;;41672;;;3
    

def EJScreen_Filter(years: list[int] = [2015, 2016, 2017, 2018,
                                       2019, 2020, 2021]):
    """Clean EJScreen data correlating to a given list of years 

    Args:
        years (list[int], optional): List of years of EJScreen data to clean.
        Defaults to [2015, 2016, 2017, 2018,
                     2019, 2020, 2021].
    """
    
    work_dir = verify_work_dir(__file__)
    for index, year in enumerate(years):
        #Verifying work directory, making new folder for cleaned files
        base_dir = f"{work_dir}/PASS_Data/EJScreen/{year}"
        Path(base_dir).mkdir(parents=True, exist_ok=True)
        
        #Finding data file
        raw_data_dir = f"{work_dir}/Raw_Data/EJScreen/{year}"
        raw_files = listdir(raw_data_dir)
        r = re.compile(f"(EJSCREEN|EJScreen|EJscreen)_{year}.csv")
        data_file = list(filter(r.match, raw_files))[0]
        print(data_file)
        
        #Importing data into Pandas dataframe
        df = pd.read_csv(f"{raw_data_dir}/{data_file}", sep=',', dtype='unicode')
        if ('statename' in df.columns):
            df.query('statename == "Pennsylvania"', inplace=True)
        elif ('STATE_NAME' in df.columns):
            df.query('STATE_NAME == "Pennsylvania"', inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        #Collect columns to drop (useless or unecessary)
        cols_drop = []
        for column in tqdm(df.columns, desc="Finding columns to drop"):
            if (df[column].isnull().all()
                    or (df[column] == 0).all()
                    or not df[column].apply(str).str.match(".*\\d.*").all()
                    or re.match('.*(OBJECTID|REGION|bin|B_|text|T_|Shape|(a|A)rea|AREA|_cnt|_CNT).*', column)):
                cols_drop.append(column)
        
        #Drop useless columns
        df.drop(columns=cols_drop, inplace=True)
        
        #Export clean data as csv
        df.to_csv(f'{base_dir}/EJScreen_{year}.csv', index=False)
        print("---------Done---------")
    
    
    
    
    



if __name__ == "__main__":
    # EJScreen_Filter(years=[2015])
    EJScreen_Filter()