# First time implementing shinny with plotly to create interactive dashboards

#Required Libraries
library(shiny)
library(ggplot2)
library(ggiraph)
library(plotly)
library(DT)

# Shiny apps are composed by main components, like de UI and the server

# Creating UI 
ui <- fluidPage(
  titlePanel("Interactive Dashboard"),                                                # Title for the page
  sidebarLayout(                                                                     # Create a layout for a side page panel
    sidebarPanel( 
      selectInput("var", "Selecting Variable:",                                      # Create a slicer
                  choices = c("mpg", "hp", "wt"),                                    # Include options
                  selected = "mpg")                                                  # Default value 
    ),
    mainPanel(                                                                       # Create a main paned for the dashboard
      tabsetPanel(
        tabPanel("Interactive chart with ggirapg", girafeOutput("plot_ggiraph")),    # Add tab where will be located a plot created with ggiraph and mark the id
        tabPanel("Interactive chart with plotly", plotlyOutput("plot_plotly")),      # Add tab where will be located a plot created with plotly and mark the id
        tabPanel("Interactive Table", DTOutput("table"))                             # Add tab where will be located a table created with DT and mark the id
      )
    )
  )
)

#Creatin server section

server <- function(input, output) {

  # interactive chart with ggiraph
  output$plot_ggiraph <- renderGirafe({
    p <- ggplot(mtcars, aes_string(x = 'wt', y = input$var, color = "factor(cyl)")) +
      geom_point_interactive(aes(tooltip = paste("Value:", input$var))) +              # Add a personalized tooltip
      labs(title =  "Interactive chart with ggiraph")
    girafe(ggobj =  p)
  })

  # Interactive chart with plotly
  output$plot_plotly <- renderPlotly({
    p2 <- ggplot(mtcars, aes_string(x = "wt", y= input$var, color = "factor(cyl)")) + 
      geom_point(size = 4) +
      labs(title = "Plotly chart")
    ggplotly(p2)
  })

  #interavtive table
  output$table <- renderDT({
    datatable(mtcars, options = list(pageLength = 5))
  })
}

# Render the final dashboard
shinyApp(ui, server)
