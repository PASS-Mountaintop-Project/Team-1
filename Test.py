import pdfkit
import tabula
from wkhtmltopdf.utils import wkhtmltopdf
#path_wkhtmltopdf = r'C:\Python310\wkhtmltopdf\bin\wkhtmltopdf.exe'
#config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
URL = "https://www.cdc.gov/asthma/brfss/2012/tableL3.htm"

pages = [2, 2, 15, 10, (12, 13), (10, 11), (12-14)]

wkhtmltopdf("https://www.cdc.gov/asthma/brfss/2012/tableL3.htm", output="work.pdf")


#wkhtmltopdf.wkhtmltopdf(url = "https://www.cdc.gov/asthma/brfss/2012/tableL3.htm", output_file = "Hello.pdf")

# pdfkit.from_url(URL, "yo.pdf", configuration=config)
# tabula.convert_into("yo.pdf", "fff.csv", output_format="csv", lattice=True, pages="all")