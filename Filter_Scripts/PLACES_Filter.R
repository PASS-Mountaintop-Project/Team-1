#Reading in csv file(s)
places_ce_2021 <- read.csv("./Raw_Data/PLACES_Files/PLACES__Local_Data_for_Better_Health__Census_Tract_Data_2021_release.csv")
places_ce_2020 <- read.csv("./Raw_Data/PLACES_Files/PLACES__Local_Data_for_Better_Health__Census_Tract_Data_2020_release.csv")

places_co_2021 <- read.csv("./Raw_Data/PLACES_Files/PLACES__Local_Data_for_Better_Health__County_Data_2021_release.csv")
places_co_2020 <- read.csv("./Raw_Data/PLACES_Files/PLACES__Local_Data_for_Better_Health__County_Data_2020_release.csv")


#Selecting relevant rows
places_ce_2021 <- dplyr::filter(places_ce_2021, StateDesc == "Pennsylvania")
places_co_2021 <- dplyr::filter(places_co_2021, StateDesc == "Pennsylvania")

# Removing necessary columns
places_ce_2021 <- subset(places_ce_2021, select = -c(StateAbbr, StateDesc, DataSource, Measure, Data_Value_Footnote_Symbol,
                                              Data_Value_Footnote, Data_Value_Unit, LocationName, Category, Short_Question_Text,
                                              Data_Value_Type, DataValueTypeID))

places_co_2021 <- subset(places_co_2021, select = -c(StateAbbr, StateDesc, DataSource, Measure, Data_Value_Footnote_Symbol,
                                              Data_Value_Footnote, Data_Value_Unit, Category, Short_Question_Text,
                                              Data_Value_Type))

#Separating longitude and latitude into 2 columns
places_ce_2021 <- tidyr::extract(places_ce_2021, Geolocation, c("Latitude", "Longitude"), "(\\d{2}.\\d{1,}) (\\d{2}.\\d{1,})")
places_co_2021 <- tidyr::extract(places_co_2021, Geolocation, c("Latitude", "Longitude"), "(\\d{2}.\\d{1,}) (\\d{2}.\\d{1,})")

#Making sure rows are in alphabetical order
places_co_2021 <- places_co_2021[order(places_co_2021$LocationName), ]


#Separate Categories
types <- list("CASTHMA", "PREVENT", "RISKBEH")

#For each category, separate out data and create new csv
for (type in types) {
  if (type == "CASTHMA") {
    places_temp <- dplyr::filter(places_ce_2021, MeasureId == "CASTHMA")
    places_temp <- subset(places_temp, select = -c(MeasureId))
  } else {
    places_temp <- dplyr::filter(places_ce_2021, CategoryID == type)
  }

  places_temp <- subset(places_temp, select = -c(CategoryID))
  write.csv(places_temp, file = paste("./PASS_Data/CDC/PLACES/PLACES_Ce_", type, "_2021.csv", sep = ""), row.names = FALSE)
}

for (type in types) {
  if (type == "CASTHMA") {
    places_temp <- dplyr::filter(places_co_2021, MeasureId == "CASTHMA")
    places_temp <- subset(places_temp, select = -c(MeasureId))
  } else {
    places_temp <- dplyr::filter(places_co_2021, CategoryID == type)
  }

  places_temp <- subset(places_temp, select = -c(CategoryID))
  write.csv(places_temp, file = paste("./PASS_Data/CDC/PLACES/PLACES_Co_", type, "_2021.csv", sep = ""), row.names = FALSE)
}