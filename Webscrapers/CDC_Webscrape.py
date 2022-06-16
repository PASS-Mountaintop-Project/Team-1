import requests
import json
import pandas as pd
import csv
from os.path import exists
from os import mkdir
from sodapy import Socrata

#Socrata API hosts lots of government data
Socrata_base_url = "https://api.us.socrata.com/api/catalog/v1?names={NAME} release&domains=chronicdata.cdc.gov"
CDC_base_url = "https://chronicdata.cdc.gov/resource/{ID}.json"
base_name = "PLACES: Local Data for Better Health, Census Tract Data {YEAR}"
base_file_path = "C:/Mountaintop/API_PLACES_Files" #Change if necessary

fileNames = ["PASS_PLACES_2021"]
filters = {2021:"year=2019", 2020:"year=2020", "PA":"stateabbr=PA", "limit":"$limit=10000"}
years = [2021, 2020] #add more when necessary

#Check if directory exists; if not, create new dir
if (not exists(base_file_path)):
    mkdir(base_file_path)


def getDataSet(api_url, year):
    response_CDC_api = requests.get(api_url)
    if (response_CDC_api.status_code == 200):
        data = response_CDC_api.text
        
        file_path = base_file_path + "/" + fileNames[0] + ".csv"

        df = pd.read_json(data, orient="records")
        df.to_csv(file_path, index=False)

        # parsed_json = json.loads(data)
        # with open(file_path, 'w', encoding='UTF8') as f:
        #     csv_writer = csv.writer(f)
        #     count = 0
        #     for i in parsed_json:
        #         if count == 0:
        #             header = i.keys()
        #             csv_writer.writerow(header)
        #             count += 1
        #         csv_writer.writerow(i.values())
    else:
        print('bruuu')
        exit(1)


def getData(ID):
    client = Socrata("chronicdata.cdc.gov", None)
    results_casthma = client.get(ID, stateabbr="PA", measureid = "CASTHMA", limit=10000)
    results_riskbeh = client.get(ID, stateabbr="PA", categoryid="RISKBEH", limit=10000)
    results_prevent = client.get(ID, stateabbr="PA", categoryid="PREVENT", limit=10000)

    df = pd.DataFrame.from_records(results_casthma)
    df.to_csv(base_file_path + "/PASS_PLACES_CASTHMA.csv", index=False)

    df = pd.DataFrame.from_records(results_riskbeh)
    df.to_csv(base_file_path + "/PASS_PLACES_RISKBEH.csv", index=False)

    df = pd.DataFrame.from_records(results_prevent)
    df.to_csv(base_file_path + "/PASS_PLACES_PREVENT.csv", index=False)

for year in years:
    name = base_name.replace("{YEAR}", str(year))
    response_Socrata_api = requests.get(Socrata_base_url.replace("{NAME}", name))

    if (response_Socrata_api.status_code == 200):
        print('API responded')
        data = response_Socrata_api.text
        parsed_json = json.loads(data)
        ID = parsed_json['results'][0]['resource']['id']
        
        CDC_endpoint_url = CDC_base_url.replace("{ID}", ID) + "?" + filters['PA']
        # getDataSet(CDC_endpoint_url, year)
        getData(ID)
        exit(1)
    else:
        print('bruh')
        exit(1)