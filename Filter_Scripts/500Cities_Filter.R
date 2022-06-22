#Reading in csv file(s)
FIVE_CASTHMA <- read.csv("./Raw_Data/500Cities_Files/500_Cities__Current_asthma_among_adults_aged___18_years(1).csv")

#Removing columns
FIVE_CASTHMA = subset(FIVE_CASTHMA, select = -c(StateDesc, StateAbbr, Category, Measure, DataValueTypeID,
                                                Data_Value_Footnote_Symbol, Data_Value_Footnote, DataSource,
                                                CategoryID, MeasureId, Short_Question_Text))

#Writing to file
write.csv(FIVE_CASTHMA, file="./PASS_Data/CDC/500Cities/PASS_500Cities_Current_Asthma.csv")
