import requests
import re
import tabula
from urllib.request import urlretrieve  #NOTE: urllib is in standard library
from bs4 import BeautifulSoup

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

#Iterate through every viable year (2003-2019)
for i in range(0, len(years)):
    for j in range (0, len(tables)):
        #Finding link for data table
        properIndex = len(years) - i - 1
        if (i < 8): #2003 - 2010, URl contains '/lifetime/' AND does NOT have '_'
            URL = BASEURL + "/asthma/brfss/" + str(years[properIndex]) + "/lifetime/" + tables[j].replace("_", "")
        elif (i < 14): #2011 - 2016, URL does NOT have '_'
            URL = BASEURL + links[properIndex].replace("default.htm", tables[j].replace("_", ""))
        else:
            URL = BASEURL + links[properIndex].replace("default.htm", tables[j])
        
        #New pdf/CSV file name and location on local drive
        newURL = "C:/Mountaintop/Yearly_Asthma_Files/" + years[len(years) - i - 1] + "/" + names[j]

        #Printing info (for debugging)
        print("--- Number, Year:\t" + str(i) + ", " + years[properIndex] + " ---")
        print("URL:\t" + URL)
        print("NewURL:\t" + newURL)

        #Entering webpage w/ pdf link
        tempPage = requests.get(URL)

        if (tempPage.status_code == 200): #If webpage responded successfully
            print("Reached webpage!")
        else: #Specifically for 2015 (html is weird)
            URL = URL.replace("html", "htm")
            print("ERROR --------> New URL:\t" + URL)
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
        
        #Converting pdf into CSV file w/ same name
        tabula.convert_into(newURL + ".pdf", newURL + ".csv", lattice=True, pages="all")