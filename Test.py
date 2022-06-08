import camelot #Requires Ghostscript and Tkinter to be installed
import pandas as pd
import tabula
# import requests
# from urllib.request import urlretrieve  #NOTE: urllib is in standard library
# from bs4 import BeautifulSoup
URL = "C:/Mountaintop/Yearly_Asthma_Files/08/RaceEth.pdf"
path = "C:/Mountaintop/Yearly_Asthma_Files/08/RaceEth.csv"


table = tabula.read_pdf(URL, pages="all", lattice=True, multiple_tables=False)
df = table[0]

if (isinstance(df, pd.DataFrame)):
    print("df is pandas")

print(df.iloc[:, 0])

#Converting pdf into CSV file w/ same name
#tabula.convert_into(URL, path, lattice=True, pages="all")

if (df.iloc[:, 0].isnull().values.any()):
    print("ERROR ----> Tabula messed up, trying Camelot")
    tables = camelot.read_pdf(URL, pages="all", multiple_tables=False)
    print("Total tables extracted:", tables.n)
    # tables.export("C:/Mountaintop/Yearly_Asthma_Files/2017/RaceEth.csv", f="csv", compress=True)

    dataFrame = pd.concat([tables[i].df for i in range(tables.n)])
    dataFrame.reset_index(drop=True, inplace=True)
    dataFrame = dataFrame.replace([r'\n'],'', regex=True)
    dataFrame.to_csv(path, index=False)
else:
    df.to_csv(path, index=False)