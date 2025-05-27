# Required libraries
library(dplyr)
library(lubridate)

# Read trips data
#trips <- read.csv("../../Sumz 2023/BikesShare_Analysis/trip_data.csv")


# Read stations data
#stations <- read.csv("../../Sumz 2023/BikesShare_Analysis/station_data.csv")

# Read data when run app from the terminal
trips <- read.csv("../../../Sumz 2023/BikesShare_Analysis/trip_data.csv")
stations <- read.csv("../../../Sumz 2023/BikesShare_Analysis/station_data.csv")

# Required station changes
new_station_codes <- c(`85` = 23, `86` = 25, `87` = 49, `88` = 69, `89` = 72, `90` = 72)

# Clear trips dataset
trips <- trips %>%
  mutate(
    across(
      c(Start.Station, End.Station), ~ ifelse(.x %in% as.integer(names(new_station_codes)),
                                            new_station_codes[as.character(.x)],
                                            .x
                                          )
    )
  )

# Add start station names throgh join files, but just specific columns
trips <- trips %>%
  left_join(stations %>% select(Id, Name, City), by = c("Start.Station" = "Id")) %>% 
  select(-Start.Station) %>%
  rename(
    Start_Station_Name = Name,
    Start_Station_City = City
  )

# Add end station names through join files but just specific columns
trips <- trips %>%
  left_join(stations %>% select(Id, Name, City), by = c("End.Station" = "Id")) %>% 
  select(-End.Station) %>%
  rename(
    End_Station_Name = Name,
    End_Station_City = City
  )

# Changing Date presentation
trips <- trips %>%
  mutate(
    Start.Date = dmy_hm((Start.Date)), # As was reveived as string it's needed to change in date format
    End.Date   = dmy_hm((End.Date)) # As was reveived as string it's needed to change in date format
  ) %>%
  mutate(    # Separate date columns in two components
    Start_Date = as.Date(Start.Date),
    Start_Time = format(Start.Date, "%H:%M:%S"),
    End_Date   = as.Date(End.Date),
    End_Time   = format(End.Date, "%H:%M:%S")
  ) %>%
  select(-c(Start.Date, End.Date))

