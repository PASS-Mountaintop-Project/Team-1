import requests
import json
import pandas as pd
from pathlib import Path
from os import chdir, getcwd
from sodapy import Socrata

from verify_work_dir import verify_work_dir

#Socrata API hosts various government data
Socrata_url = "https://api.us.socrata.com/api/catalog/v1?names={}&domains=chronicdata.cdc.gov"
formats = {"Census Tract": "Ce", "County": "Co"} #"ZCTA": "ZCTA"
categories = ["CASTHMA", "RISKBEH", "PREVENT"]
years = [2021, 2020] #add more when necessary


def get_api_data(ID, form, year):
    #Check if file dir exists; if not, create new dir
    base_dir = f"{work_dir}/Raw_Data/API_PLACES_Files/{year}/{form}"
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    
    client = Socrata("chronicdata.cdc.gov", None)
    results_casthma = client.get(ID, stateabbr="PA", measureid="CASTHMA", limit=10000)
    results_riskbeh = client.get(ID, stateabbr="PA", categoryid= "UNHBEH" if year=="2020" else "RISKBEH", limit=10000)
    results_prevent = client.get(ID, stateabbr="PA", categoryid="PREVENT", limit=10000)

    abbr = formats[form]
    df = pd.DataFrame.from_records(results_casthma)
    df.to_csv(f"{base_dir}/Raw_PLACES_{abbr}_CASTHMA_{year}.csv", index=False)

    df = pd.DataFrame.from_records(results_riskbeh)
    df.to_csv(f"{base_dir}/Raw_PLACES_{abbr}_RISKBEH_{year}.csv", index=False)

    df = pd.DataFrame.from_records(results_prevent)
    df.to_csv(f"{base_dir}/Raw_PLACES_{abbr}_PREVENT_{year}.csv", index=False)

def get_places_data():
    verify_work_dir(__file__)
    
    for form in formats:
        for year in years:
            title = f"PLACES: Local Data for Better Health, {form} Data {year} release"
            response = requests.get(Socrata_url.format(title))
            print(form, year)
            if (response.status_code == 200):
                print('API responded')
                data = response.text
                parsed_json = json.loads(data)
                ID = parsed_json['results'][0]['resource']['id']
                get_api_data(ID, form, str(year))
            else:
                print('ERROR')
                exit(1)



if __name__ == "__main__":
    get_places_data()