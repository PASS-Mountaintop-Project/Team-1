import requests
import re
import tabula
from urllib.request import urlretrieve  #NOTE: urllib is in standard library
from bs4 import BeautifulSoup
import camelot #NOTE: Requires Ghostscript and Tkinter to be installed
import pandas as pd

def useCamelot(pdfURL, filePath):
    try:
        print("ERROR ----> Tabula messed up, trying Camelot...")
        tables = camelot.read_pdf(pdfURL, pages="all", multiple_tables=False)
        print("Total tables extracted:", tables.n)

        df = pd.concat([tables[i].df for i in range(tables.n)])
        df.reset_index(drop=True, inplace=True)
        df = df.replace([r'\n'],'', regex=True)
        df.to_csv(filePath, index=False)

        print("Camelot success!")
        return 1
    except:
        print("ERROR ----> Camelot failed")
        return 0

def useTabula(pdfURL, filePath):
    print("Trying Tabula...")
    try:
        table = tabula.read_pdf(pdfURL, pages="all", lattice=True, multiple_tables=False)
        df = table[0]
        if (df.iloc[:, 0].isnull().values.any()):
            return useCamelot(pdfURL, filePath)  #If Tabula messes up, use Camelot (slower, but more accurate)
        else:
            df.to_csv(filePath, index=False)
            print("Tabula success!")
            return 1
    except:
        return useCamelot(pdfURL, filePath) #If error in Tabula, use Camelot


URL = "https://www.cdc.gov/asthma/brfss/default.htm"
BASEURL = "https://www.cdc.gov"

links = []
years = []
tables = ["tableL2_1.htm", "tableL2_2.htm", "tableL3.htm",
            "tableL4.htm", "tableL5.htm", "tableL6.htm", "tablel7.htm"]
names = ["Sex(P)", "Sex(N)", "Age", "Race", "RaceEth", "Edu", "Income"]

#Enter default page to extract links
page = requests.get(URL)
if (page.status_code != 200):
    print("Webpage down or not found...")
    exit(1)

#Use BeautifulSoup to read in html of webpage
soup = BeautifulSoup(page.content, "html.parser")

#Gets links for 2003 - 2019
for link in soup.find_all('a'):
    #NOTE: If we want 1999 onwards, use regex '^/asthma/brfss/[0-9]{1}.*'
    #NOTE: If we want 2003 onwards, use regex '^/asthma/brfss/(\\d{4}|[0]{1}[3-9]{1}).*'
    linkString = link.get("href")
    if (re.search("^/asthma/brfss/(\\d{2}[0-1]{1}|[0]{1}[3-9]{1}).*", linkString)):
        links.append(linkString)
        years.append(re.findall(r'\d{2,4}', linkString)[0])

#Print for debugging
print("Links:")
print (links)
print("Years:")
print (years)


#NOTE: Ones that often give trouble (For debugging purposes):
#2017 == 14
#2008 == 5
#2014 == 11

#Iterate through every viable year (2003-2019; e.g. range(0, len(years)))
for i in range(len(years)):
    for j in range (0, len(tables)):
        #Finding link for data table
        properIndex = len(years) - i - 1
        if (i < 8): #2003 - 2010, URl contains '/lifetime/' AND does NOT have '_'
            URL = BASEURL + "/asthma/brfss/" + str(years[properIndex]) + "/lifetime/" + tables[j].replace("_", "")
        elif (i < 14): #2011 - 2016, URL does NOT have '_'
            URL = BASEURL + links[properIndex].replace("default.htm", tables[j].replace("_", ""))
        else:
            URL = BASEURL + links[properIndex].replace("default.htm", tables[j])
        
        #New pdf/CSV file name and location on local drive (NOTE: change if necessary)
        newURL = "C:/Mountaintop/Raw_Data/Yearly_Asthma_Files/" + years[len(years) - i - 1] + "/" + names[j]

        #Printing info (for debugging)
        print("--- Number, Year:\t" + str(i) + ", " + years[properIndex] + " ---")
        print("URL:\t" + URL)
        print("NewURL:\t" + newURL)

        #Entering webpage w/ pdf link
        tempPage = requests.get(URL)

        if (tempPage.status_code == 200): #If webpage responded successfully
            print("Reached webpage!") #Print for debugging
        else: #Specifically for 2015 (html is weird)
            URL = URL.replace("html", "htm")
            print("ERROR --------> New URL:\t" + URL) #Print for debugging
            tempPage = requests.get(URL)

        #Use BeautifulSoup to read in html of webpage
        soup = BeautifulSoup(tempPage.content, "html.parser")

        #Finding pdf link for data using BeautifulSoup
        for link in soup.find_all('a'):
            linkString = link.get("href")
            if (re.search("^/asthma/brfss/\\d{2,4}.*", str(linkString))): #regex to find link
                URL = BASEURL + linkString

        #Downloading pdf onto local drive
        urlretrieve(URL, str(newURL + ".pdf"))
        
        useTabula(newURL + ".pdf", newURL + ".csv")