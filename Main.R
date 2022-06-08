#Reading in csv file(s)
FIVE_CASTHMA <- read.csv("PLACES_Files/500_Cities__Current_asthma_among_adults_aged___18_years(1).csv")
PLACES_DATA <- read.csv("PLACES_Files/PLACES__Local_Data_for_Better_Health__Census_Tract_Data_2021_release.csv")

#Selecting rows
FIVE_CASTHMA <- dplyr::filter(FIVE_CASTHMA, StateDesc=="Pennsylvania")
PLACES_DATA = dplyr::filter(PLACES_DATA, StateDesc=="Pennsylvania")

#Removing columns
FIVE_CASTHMA = subset(FIVE_CASTHMA, select = -c(StateDesc, StateAbbr, Category, Measure, DataValueTypeID,
                                                Data_Value_Footnote_Symbol, Data_Value_Footnote, DataSource,
                                                CategoryID, MeasureId, Short_Question_Text))

PLACES_DATA = subset(PLACES_DATA, select = -c(StateAbbr, StateDesc, DataSource, Measure,
                                              Data_Value_Footnote_Symbol, Data_Value_Footnote))

types = list("CASTHMA", "PREVENT", "RISKBEH")


#Writing to file
write.csv(FIVE_CASTHMA, file="PASS_Files/PASS_500Cities_Current_Asthma.csv")

for (type in types) {
  if (type == "CASTHMA") {
    PLACES_TEMP <- dplyr::filter(PLACES_DATA, MeasureId=="CASTHMA")
    PLACES_TEMP <- subset(PLACES_TEMP, select=-c(Category, CategoryID))
  }
  else {
    PLACES_TEMP = dplyr::filter(PLACES_DATA, CategoryID==type)
  }
  
  write.csv(PLACES_TEMP, file=paste("PASS_Files/PASS_PLACES_", type, ".csv", sep=""))
}



files <- list.files(path = "C:/Mountaintop/Yearly_Asthma_Files", full.names = TRUE)




dataSets <- list()
tDataSet <- list()
for (i in 1:length(files)) {
  csvFiles <- list.files(path = files[i], full.names = TRUE, pattern = ".csv$")
  for (j in 1:length(csvFiles)) {
    print(csvFiles[j])
    tDataSet[[j]] <- read.csv(csvFiles[j], header=FALSE)
  }
  dataSets[[i]] <- tDataSet
}
