# Shiny app
# required libraries
library(shiny)
library(dplyr)
library(plotly)
library(ggplot2)
library(lubridate)

# Data
source('./interactive_dashboard_with_R/rent_trip.R')

# Listing started points
start_stations <- unique(trips$Start_Station_Name)
start_cities <- unique(trips$Start_Station_City)

# Listing ended points
end_stations <- unique(trips$End_Station_Name)
end_cities <- unique(trips$End_Station_City)

# list all Years
years <- sort(unique(format(as.Date(trips$Start_Date), "%Y")))

# Date Range
min_date <- min(trips$Start_Date, na.rm = TRUE)
max_date <- max(trips$Start_Date, na.rm = TRUE)

# Create the UI
ui <- fluidPage(
  ## App Title
  tags$div(
    tags$h2(HTML("BikeShare Analysis dash <br>(now with R)")),
    style = "text-align:center;"
  ),

  fluidRow(
    column(
      width = 1,
      selectInput(
        "year",
        "Year",
        choices = c("All" = "ALL", years)
      )
    ),
    column(
      width = 2,
      dateRangeInput(
        "date_range",
        "Date Range",
        start = min_date,
        end = max_date
      )
    ),
    column(
      width = 2,
      selectInput(
        "start_city",
        "Start City",
        choices = c("All" = "ALL", start_cities),
        multiple = TRUE,
        selected = "ALL"
      )
    ),
    column(
      width = 2,
      selectInput(
        "start_station",
        "Start Station",
        choices = c("All" = "ALL", start_stations),
        multiple = TRUE,
        selected = "ALL"
      )
    ),
    column(
      width = 2,
      selectInput(
        "end_city",
        "End Station",
        choices = c("All" = "ALL", end_cities),
        multiple = TRUE
      )
    ),
    column(
      width = 2,
      selectInput(
        "end_station",
        "End Station",
        choices = c("All" = "ALL", end_stations),
        multiple = TRUE,
        selected = "ALL"
      )
    )
  ),

  fluidRow(
    column(6,
      plotlyOutput(
        outputId = "start_trips_st",
        width = "100%",
        height = "50%"
      )
    ),

    column(6,
      plotlyOutput(
        outputId = "end_trips_st",
        width = "100%",
        height = "50%"
      )
    )
  ),

  fluidRow(
    column(6,
      plotOutput(
        outputId = "start_trips_ph",
        width = "100%",
        height = "50%"
      )
    ),

    column(6,
      plotOutput(
        outputId = "end_trips_ph",
        width = "100%",
        height = "50%"
      )
    )
 )
)

# Create the server
server <- function(input, output, session) {

  # Crear el reactive de input$years
  year_filter <- reactive({
    if(input$year != "ALL") {
      trips %>%
        filter(year(Start_Date) == as.numeric(input$year))
    } else {
      trips
    }
  })

  date_range_filter <- reactive({
    year_filter() %>%
      filter(
        Start_Date >= input$date_range[1],
        Start_Date <= input$date_range[2]
      )
  })

  start_city_filter <- reactive({
    if(input$start_city == "ALL") {
      year_filter()
    } else {
      year_filter() %>%
        filter(Start_Station_City == input$start_city)
    }    
  })

  start_station_filter <- reactive({
    if(input$start_station == "ALL") {
      start_city_filter()
    } else {
      start_city_filter() %>%
        filter(Start_Station_Name == input$start_station)
    }    
  })

  end_station_filter <- reactive({
    start_station_filter() %>%
      filter(End_Station_Name == input$end_station)
  })

  # Graphic charts

  # Start Trips per station chart
  output$start_trips_st <- renderPlotly ({
    # First counting the started trips by station
    started_trips_st <- start_station_filter() %>%
      count(Start_Station_Name, name = "started_trips")

    # Create the chart
    plot_ly(
      data = started_trips_st,
      x = ~started_trips,
      y = ~reorder(Start_Station_Name, started_trips),
      type = "bar",
      orientation = "h"
    ) |>
      layout(
        title = "Started Trips per Station",
        xaxis = list(title = "Started Trips"),
        yaxis = list(title = "Start Station")
      )
  })

  # Ended Trips per station chart
  output$end_trips_st <- renderPlotly ({
    # First counting the started trips by station
    ended_trips_st <- start_station_filter() %>%
      count(End_Station_Name, name = "ended_trips")

    # Create the chart
    plot_ly(
      data = ended_trips_st,
      x = ~ended_trips,
      y = ~reorder(End_Station_Name, ended_trips),
      type = "bar",
      orientation = "h"
    ) |>
      layout(
        title = "Ended Trips per Station",
        xaxis = list(title = "Ended Trips"),
        yaxis = list(title = "End Station")
      )
  })
}

shinyApp(ui, server)

