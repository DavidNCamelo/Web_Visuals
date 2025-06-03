# Shiny app
# required libraries
library(shiny)
library(dplyr)
library(plotly)
library(ggplot2)
library(lubridate)

# Data
#source('./interactive_dashboard_with_R/rent_trip.R')
# When run from the terminal
source('./rent_trip.R')

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

  # Add filters row
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
        "End City",
        choices = c("All" = "ALL", end_cities),
        multiple = TRUE,
        selected = "ALL"
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

  # Add first charts row
  fluidRow(
    column(6,
      div(
        style = "height: 400px; overflow-y: auto; border: 1px solid #fff; padding: 5px",
        plotlyOutput(
          outputId = "start_trips_st",
          height = "500%"
        )
      )
    ),

    column(6, 
      div(
        style = "height: 400px; overflow-y: auto; border: 1px solid #fff; padding: 5px",
        plotlyOutput(
          outputId = "end_trips_st",
          height = "500%"
        )
      )
    )
  ),

  # Add Second chart row
  fluidRow(
    column(6,
      plotlyOutput(
        outputId = "start_trips_ph",
        width = "100%"
      )
    ),

    column(6,
      plotlyOutput(
        outputId = "end_trips_ph",
        width = "100%"
      )
    )
 )
)

# Create the server
server <- function(input, output, session) {

  # Add click interaction elements
  selected_start_station <- reactiveVal(NULL)

  # Capture the click
  observeEvent(event_data('plotly_click', source = 'start_station_plot'), {
    click_data <- event_data('plotly_click', source = 'start_station_plot')
    if(!is.null(click_data)) {
      selected_station <- click_data$y
      selected_start_station(selected_station)
    }
  })

  # Create the reactive of input$years
  year_filter <- reactive({
    if(input$year != "ALL") {
      trips %>%
        filter(year(Start_Date) == as.numeric(input$year))
    } else {
      trips
    }
  })

  # Reactive for Year and Date Range
  date_range_filter <- reactive({
    year_filter() %>%
      filter(
        Start_Date >= input$date_range[1],
        Start_Date <= input$date_range[2]
      )
  })

  #Add observe event over the date filters
  observeEvent(input$year, {
    # Filtering dates just for the selected year
    if (input$year != "ALL") {
      filtered_dates <- trips %>%
        filter(year(Start_Date) == as.numeric(input$year))
      
      new_min <- min(filtered_dates$Start_Date, na.rm = TRUE)
      new_max <- max(filtered_dates$Start_Date, na.rm = TRUE)
    } else {
      new_min <- min(trips$Start_Date, na.rm = TRUE)
      new_max <- max(trips$Start_Date, na.rm = TRUE)
    }
  
    # Update date range slicer
    updateDateRangeInput(
      session,
      inputId = "date_range",
      start = new_min,
      end = new_max,
      min = new_min,
      max = new_max
    )
  })

  # Reactive for previous filters and the new Start City
  start_city_filter <- reactive({
    if("ALL" %in% input$start_city) {
      date_range_filter()
    } else {
      date_range_filter() %>%
        filter(Start_Station_City %in% input$start_city)
    }    
  })

  # Reactive for previous filters and the new Start Station
  start_station_filter <- reactive({
    if("ALL" %in% input$start_station) {
      start_city_filter()
    } else {
      start_city_filter() %>%
        filter(Start_Station_Name %in% input$start_station)
    }    
  })

  # Oberve events for the last 2 filters
  observeEvent(input$start_city, {
    # Filtering by start city
    filtered_data <- if ("ALL" %in% input$start_city) {
      date_range_filter()
    } else {
      date_range_filter() %>% filter(Start_Station_City %in% input$start_city)
    }
  
    # Extract values
    updated_stations <- sort(unique(filtered_data$Start_Station_Name))
  
    # #Ubdate the start station slicer
    updateSelectInput(
      inputId = "start_station",
      choices = c("All" = "ALL", updated_stations),
      selected = "ALL"
    )
  })
  
  # Reactive for previous filters and the new End City
  end_city_filter <- reactive({
    if("ALL" %in% input$end_city) {
      start_station_filter()
    } else {
      start_station_filter() %>%
        filter(End_Station_City %in% input$end_city)
    }
  })

  end_station_filter <- reactive({
    if("ALL" %in% input$end_station) {
      end_city_filter()
    } else {
      end_city_filter() %>%
        filter(End_Station_Name %in% input$end_station)
    }    
  })

  # Oberve events for the last 2 filters
  observeEvent(input$end_city, {
    # Filtering by start city
    end_ct_filtered_data <- if ("ALL" %in% input$end_city) {
      start_city_filter()
    } else {
      start_city_filter() %>% filter(End_Station_City %in% input$end_city)
    }
  
    # Extract values
    end_updated_stations <- sort(unique(end_ct_filtered_data$End_Station_Name))
  
    # #Ubdate the end station slicer
    updateSelectInput(
      inputId = "end_station",
      choices = c("All" = "ALL", end_updated_stations),
      selected = "ALL"
    )
  })

  # Reactive filter based on click interaction
  click_start_filtered <- reactive({
    data <- end_station_filter()
    if(!is.null(selected_start_station())) {
      data <- data %>% filter(Start_Station_Name == selected_start_station())
    }
    data
  })
  # Graphic charts

  # Start Trips per station chart
  output$start_trips_st <- renderPlotly ({
    # First counting the started trips by station
    started_trips_st <- start_station_filter() %>%
      count(Start_Station_Name, name = "started_trips")

    # Add abreviations into the tootlip
    started_trips_st$label_text <- ifelse(
      started_trips_st$started_trips >= 1000,
      paste0(formatC(started_trips_st$started_trips / 1000, format = "f", digits = 1), "K"),
      as.character(started_trips_st$started_trips)
    )

    # Double row tooltip
    started_trips_st$tooltip_text <- paste0(
      started_trips_st$Start_Station_Name, "<br>",
      format(started_trips_st$started_trips, big.mark = ",")
    )

    # Create the chart
    plot_ly(
      data = started_trips_st,
      x = ~started_trips,
      y = ~reorder(Start_Station_Name, started_trips),
      text = ~label_text,
      textposition = "outside",
      type = "bar",
      orientation = "h",
      hoverinfo = "text",
      hovertext = ~tooltip_text,
      source = 'start_station_plot'
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
    ended_trips_st <- click_start_filtered() %>%
      count(End_Station_Name, name = "ended_trips")

    # Add abreviations into the tootlip
    ended_trips_st$label_text <- ifelse(
      ended_trips_st$ended_trips >= 1000,
      paste0(formatC(ended_trips_st$ended_trips / 1000, format = "f", digits = 1), "K"),
      as.character(ended_trips_st$ended_trips)
    )

    # Double row tooltip
    ended_trips_st$tooltip_text <- paste0(
      ended_trips_st$End_Station_Name, "<br>",
      format(ended_trips_st$ended_trips, big.mark = ",")
    )
    # Create the chart
    plot_ly(
      data = ended_trips_st,
      x = ~ended_trips,
      y = ~reorder(End_Station_Name, ended_trips),
      text = ~label_text,
      type = "bar",
      textposition = "outside",
      orientation = "h",
      hoverinfo = "text",
      hovertext = ~tooltip_text,
      marker = list(color = "orange")
    ) |>
      layout(
        title = "Ended Trips per Station",
        xaxis = list(title = "Ended Trips"),
        yaxis = list(title = "End Station")
      )
  })

  # Started trip per hour
  output$start_trips_ph <- renderPlotly ({
    # Count the started trips per hour
    start_trips_ph <- click_start_filtered() %>%
      mutate(hour = as.integer(substr(Start_Time, 1, 2))) %>%
      count(hour, name = "started_trips_per_hour")

    # Create chart
    started_per_hour <- ggplot(
      start_trips_ph,
      aes(x = hour, y = started_trips_per_hour)) +  
      geom_col(fill = "blue")+
      labs(x = "Start Hour", y = "Started Trips", title =  "Started Trips per Hour")

    ggplotly(started_per_hour) # Add plotlyframe to show tooltip
  })

  # Ended trip per hour
  output$end_trips_ph <- renderPlotly ({
    # Count the started trips per hour
    end_trips_ph <- click_start_filtered() %>%
      mutate(hour = as.integer(substr(End_Time, 1, 2))) %>%
      count(hour, name = "ended_trips_per_hour")

    # Create chart
    ended_per_hour <- ggplot(
      end_trips_ph,
      aes(x = hour, y = ended_trips_per_hour)) +  
      geom_col(fill = "orange")+
      labs(x = "End Hour", y = "Ended Trips", title =  "Started Trips per Hour")

    ggplotly(ended_per_hour) # Add plotlyframe to show tooltip
  })
}

shinyApp(ui, server)

