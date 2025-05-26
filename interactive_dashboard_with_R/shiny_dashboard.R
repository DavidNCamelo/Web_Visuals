# SHINY Dashboard documentarion Example
# This is the basic structure abour how to use this library

# Required Library
library(shiny)
library(shinydashboard)
#App
shinyApp(
  ui = dashboardPage(
    dashboardHeader(
      title = "Dashboard with Shiny"
    ),
    dashboardSidebar(),
    dashboardBody(),
  ),
  server = function(input, output) { }
)

