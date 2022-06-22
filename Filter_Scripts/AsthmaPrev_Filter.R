#Read in file paths (divided by each year)
files <- list.files(path = "./Raw_Data/Yearly_Asthma_Files", full.names = TRUE)


#dataSets will hold everything, tDataSet will hold each year's data sets
dataSets <- list()
tDataSet <- list()
yearDirs <- c()

#Loop through every directory and read in each CSV file, adding to dataSets
for (i in 1:length(files)) {
  yearDirs[i] <- str_extract(files[i], "\\d{2,}") #Collect year names
  csvFiles <- list.files(path = files[i], full.names = TRUE, pattern = ".csv$")
  for (j in 1:length(csvFiles)) {
    tDataSet[[j]] <- read.csv(csvFiles[j], header=FALSE)
  }
  dataSets[[i]] <- tDataSet
}

#Variables to use in loop
dropIndex = 1
rowsDrop = c() #Vector of rows to drop
headFound = FALSE #Used to find header
csvNames <- c("Age", "Edu", "Income", "Race", "RaceEth", "Sex(N)", "Sex(P)") #Names of tables
basePath = "./PASS_Data/Asthma_Prevalence/" #Base file path to upload filtered csv
baseFileName = "PASS_" #Base file name for csv file

#Filter out only header and PA data for every data set
for (i in 1:length(dataSets)) { #Each year
  for (j in 1:length(dataSets[[i]])) { #Each table
    for (k in 1:nrow(dataSets[[i]][[j]])) { #Each row
      
      #item == state name abbreviation
      item = dataSets[[i]][[j]][c(k), c(1)]
      
      #In case item is null
      if (is.na(item)) {
        item = dataSets[[i]][[j]][c(k), c(2)]
      }
      
      #If item is not PA or is null
      if (is.null(item) | item != "PA") {
        #If item is "State" and header not found yet, that row (only) is the header
        if (item == "State" & !headFound) {
          headFound = TRUE
        }
        else { #Otherwise, add that row to rowsDrop
          rowsDrop[dropIndex] = k
          dropIndex = dropIndex + 1
        }
      }
    }
    dataSets[[i]][[j]] <- dataSets[[i]][[j]][-rowsDrop,] #Drop all useless rows
    
    names(dataSets[[i]][[j]]) <- dataSets[[i]][[j]][1,] #Converting first row into header
    dataSets[[i]][[j]] <- dataSets[[i]][[j]][-1,]
    
    rownames(dataSets[[i]][[j]]) <- NULL #Reset row indices
    
    #Reset all variables
    rowsDrop = c()
    dropIndex = 1
    headFound = FALSE
    
    #Create file paths for dir's (by year) and csv's
    fPath = paste(basePath, yearDirs[i], sep="")
    csvPath = paste(fPath, "/", baseFileName, csvNames[j], "_", yearDirs[i], ".csv", sep="")

    #Create new dir if nonexistent
    if (!file.exists(fPath)) {
      dir.create(fPath)
    }
    
    #Create csv from data set in correct path
    write.csv(dataSets[[i]][[j]], file=csvPath, row.names = FALSE)
  }
}









