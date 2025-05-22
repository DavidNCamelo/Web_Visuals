# New app example

library(shiny)
library(plotly)

# Creating ui
ui <- fluidPage(
  numericInput(
    "age",
    "Minimun Age",
    value = 18,
    min = 0,
    max = 100
  ),

  selectInput(
    "country",
    "Country",
    choices = c("All" = "ALL", data$country),
    selected = "ALL"
  ),

  plotlyOutput(
    "plotlyGraph",
    width = "100%"
  ),

  tableOutput(
    "table"
  )
)

# Generate data
data <- data.frame(
  name = c("Giss", "Dav", "Mat", "Kt", "Kr1", "kr2", "X1", "Sof", "Mt"),
  age = c(25, 26, 27, 27, 28, 26, 10, 16, 27),
  country = c("Bra", "Col", "Col", "Usa", "Col", "Fra", "Col", "Col", "Col")
)

# Create server
server <- function(input, output, session) {
  
  # Reactive filter to input$age
  age_filter <- reactive({
    data |>
      dplyr::filter(age >= input$age)
  })

  # Reactive filter to input$region and age_filter
  region_filter <- reactive({
    df <- age_filter()
    if (input$country == "ALL") {
      df
    } else {
      df |> dplyr::filter(country == input$country)
    }
  })

  # Output table
  output$table <- renderTable({
    region_filter() |>
      dplyr::summarise(
        mean = mean(age),
        max = max(age),
        min = min(age)
      )
  })

  #Histogram
  output$plotlyGraph <- renderPlotly({
    plot_ly(
      data = region_filter(),
      x = ~age,
      type = "histogram",
      name = "Age",
      marker = list(color = "red")
    ) |>
      layout(
        title = "Histogram",
        xaxis = list(title = "Age"),
        yaxis = list(title = "Frecuency")
      )
  })
}

shinyApp(ui, server)
