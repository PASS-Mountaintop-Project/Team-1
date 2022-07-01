import pandas as pd
import numpy as np

from tqdm import tqdm
from pathlib import Path

from verify_work_dir import verify_work_dir


#TYPE;FULLCODE;STATE;COUNTY;TRACT;BLOCK;PLACE;COUSUB;CONCITY;AIANNH;SHEETS
#Block;420010301011000;42;001;301.01;1000;;41672;;;3

def EJScreen_Filter(year):
    #Verifying work directory, making new folder for cleaned files
    work_dir = verify_work_dir(__file__)
    base_dir = f"{work_dir}/PASS_Data/EJScreen/{year}"
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    
    df = pd.read_csv("./Raw_data/EJScreen/2015/EJSCREEN_20150505.csv")  #<------TODO: Change import to be dynamic
    df.query('statename == "Pennsylvania"', inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    cols_drop = []
    for column in tqdm(df.columns, desc="Finding columns to drop"):
        if (df[column].isnull().all()
                or not df[column].apply(str).str.match(".*\\d.*").all()
                or (df[column] == 0).all()):
            cols_drop.append(column)
    df.drop(columns=cols_drop, inplace=True)
    
    #Export clean data as csv
    df.to_csv(f'{base_dir}/EJScreen_{year}.csv', index=False)
    print("---------Done---------")
    
    
    
    
    



if __name__ == "__main__":
    EJScreen_Filter(2015)