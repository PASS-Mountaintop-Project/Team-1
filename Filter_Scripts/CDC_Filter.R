#Reading in csv file(s)
PLACES_DATA <- read.csv("./Raw_Data/PLACES_Files/PLACES__Local_Data_for_Better_Health__Census_Tract_Data_2021_release.csv")

#Selecting relevant rows
PLACES_DATA <- dplyr::filter(PLACES_DATA, StateDesc=="Pennsylvania")

#Removing necessary columns
PLACES_DATA = subset(PLACES_DATA, select = -c(StateAbbr, StateDesc, DataSource, Measure, Data_Value_Footnote_Symbol,
                                              Data_Value_Footnote, Data_Value_Unit, LocationName, Category, Short_Question_Text,
                                              Data_Value_Type))

#Separating longitude and latitude into 2 columns
PLACES_DATA <- tidyr::extract(PLACES_DATA, Geolocation, c('Latitude', 'Longitude'), "(\\d{2}.\\d{1,}) (\\d{2}.\\d{1,})")

#Separate Categories
types <- list("CASTHMA", "PREVENT", "RISKBEH")

#For each category, separate out data and create new csv
for (type in types) {
  if (type == "CASTHMA") {
    PLACES_TEMP <- dplyr::filter(PLACES_DATA, MeasureId=="CASTHMA")
    PLACES_TEMP <- subset(PLACES_TEMP, select=-c(MeasureId))
  } else {
    PLACES_TEMP <- dplyr::filter(PLACES_DATA, CategoryID==type)
  }
  
  PLACES_TEMP <- subset(PLACES_TEMP, select=-c(CategoryID))
  write.csv(PLACES_TEMP, file=paste("./PASS_Data/CDC/PLACES/PASS_PLACES_", type, ".csv", sep=""), row.names = FALSE)
}