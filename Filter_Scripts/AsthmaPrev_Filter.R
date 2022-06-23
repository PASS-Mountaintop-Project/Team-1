#Read in file paths (divided by each year)
files <- list.files(path = "./Raw_Data/Yearly_Asthma_Files", full.names = TRUE)

#data_sets will hold everything, temp_set will hold each year's data sets
data_sets <- list()
temp_set <- list()
year_dirs <- c()

#Loop through every directory and read in each CSV file, adding to data_sets
for (i in seq_along(files)) {
  year_dirs[i] <- str_extract(files[i], "\\d{2,}") #Collect year names
  csv_files <- list.files(path = files[i], full.names = TRUE, pattern = ".csv$")
  for (j in seq_along(csv_files)) {
    temp_set[[j]] <- read.csv(csv_files[j], header = FALSE)
  }
  data_sets[[i]] <- temp_set
}

#Variables to use in loop
drop_index <- 1
drop_rows <- c() #Vector of rows to drop
found_head <- FALSE #Used to find header
csv_names <- c("Age", "Edu", "Income", "Race", "RaceEth", "Sex(N)", "Sex(P)") #Names of tables
base_path <- "./PASS_Data/Asthma_Prevalence/" #Base file path to upload filtered csv
base_file_name <- "PASS_" #Base file name for csv file

#Filter out only header and PA data for every data set
for (i in seq_along(data_sets)) { #Each year
  for (j in seq_along(data_sets[[i]])) { #Each table
    for (k in seq_along(nrow(data_sets[[i]][[j]]))) { #Each row

      #item == state name abbreviation
      item <- data_sets[[i]][[j]][c(k), c(1)]

      #In case item is null
      if (is.na(item) || is.null(item)) {
        item <- data_sets[[i]][[j]][c(k), c(2)]
      }

      #If item is not PA or is null
      if (item != "PA") {
        #If item is "State" and header not found yet, that row (only) is the header
        if (item == "State" && !found_head) {
          found_head <- TRUE
        } else { #Otherwise, add that row to drop_rows
          drop_rows[drop_index] <- k
          drop_index <- drop_index + 1
        }
      }
    }
    data_sets[[i]][[j]] <- data_sets[[i]][[j]][-drop_rows, ] #Drop all useless rows

    names(data_sets[[i]][[j]]) <- data_sets[[i]][[j]][1, ] #Converting first row into header
    data_sets[[i]][[j]] <- data_sets[[i]][[j]][-1, ]

    rownames(data_sets[[i]][[j]]) <- NULL #Reset row indices

    #Reset all variables
    drop_rows <- c()
    drop_index <- 1
    found_head <- FALSE

    #Create file paths for dir's (by year) and csv's
    file_path <- paste(base_path, year_dirs[i], sep = "")
    csv_path <- paste(file_path, "/", base_file_name, csv_names[j], "_", year_dirs[i], ".csv", sep = "")

    #Create new dir if nonexistent
    if (!file.exists(file_path)) {
      dir.create(file_path)
    }

    #Create csv from data set in correct path
    write.csv(data_sets[[i]][[j]], file = csv_path, row.names = FALSE)
  }
}