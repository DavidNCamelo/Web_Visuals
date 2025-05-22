# SHINY Dashboard documentarion Example

# Required Library
library(shiny)
library(shinydashboard)
#App
shinyApp(
  ui = dashboardPage(
    dashboardHeader(
      title = "Dashboard with Shiny",
      titlewidth = '100%'
    ),
    dashboardSidebar(disable = TRUE),
    dashboardBody(
      h2("Content")
    ),
    title = "Dashboard example"
  ),
  server = function(input, output) { }
)

