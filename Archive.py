#NOTE: Using pdfkit and wkhtmltopdf
# import pdfkit
# path_wkhtmltopdf = r'C:\Python310\wkhtmltopdf\bin\wkhtmltopdf.exe'
# config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
# pdfkit.from_url(URL, newURL, configuration=config)

# pdfkit.from_url(URL, "yo.pdf", configuration=config)
# df = tabula.read_pdf("yo.pdf", lattice=True, pages="all")[0]
# tabula.convert_into("yo.pdf", "fff.csv", output_format="csv", lattice=True, pages="all")


#NOTE: Pages originally used to find PA in pdf's
# pages = [(2), (2), (15, 16), (10, 11), (12, 13), (10, 11), (12, 13)]


# ------ Another method to get info from page (NOTE: BE CAREFUL ABOUT ENCODING!!) ----------- 
# with open("WebInfo.html", "w", encoding="utf-8") as f:
#     f.write(page.text)
# soup = BeautifulSoup(open("WebInfo.html", "r", encoding="utf-8"), "html.parser")


# counter = 0
# years.append((2003 + counter)) (NOTE: Another way to add the years)
# counter += 1


# #Finding link for data table
# properIndex = len(years) - i - 1
# if (i < 8): #2003 - 2010, URl contains '/lifetime/' AND does NOT have '_'
#     URL = BASEURL + "/asthma/brfss/" + str(years[properIndex]) + "/lifetime/" + tables[j].replace("_", "")
# elif (i < 14): #2011 - 2016, URL does NOT have '_'
#     # URL = BASEURL + re.sub("default.htm", tables[j].replace("_", ""), links[properIndex])
#     URL = BASEURL + links[properIndex].replace("default.htm", tables[j].replace("_", ""))
# else:
#     # URL = BASEURL + re.sub("default.htm", tables[j], links[properIndex])
#     URL = BASEURL + links[properIndex].replace("default.htm", tables[j])


#NOTE: Camelot, tabula
# tables.export("C:/Mountaintop/Yearly_Asthma_Files/2017/RaceEth.csv", f="csv", compress=True)
#Converting pdf into CSV file w/ same name
# tabula.convert_into(newURL + ".pdf", newURL + ".csv", lattice=True, pages="all")