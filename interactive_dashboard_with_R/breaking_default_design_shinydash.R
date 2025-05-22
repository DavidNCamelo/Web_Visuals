library(shiny)
library(shinydashboard)

ui <- dashboardPage(
  dashboardHeader(
    title = "Dashboard with Shiny",
    titleWidth = "100%"
  ),
  dashboardSidebar(disable = TRUE),
  dashboardBody(
    tags$head(
      tags$style(HTML("
        /* Forzar visibilidad del título y centrarlo */
        .main-header .logo {
          display: block !important;
          float: none;
          width: 100% !important;
          text-align: center;
          font-size: 24px;
          font-weight: bold;
          line-height: 50px;
          color: white;
        }
        .main-header .navbar {
          margin-left: 0;
        }

        /* Eliminar espacio del sidebar completamente */
        .main-sidebar {
          display: none !important;
        }
        .content-wrapper, .main-footer, .right-side {
          margin-left: 0 !important;
        }
      "))
    ),
    h2("Contenido principal sin sidebar")
  ),
  title = "Mi Dashboard"
)

server <- function(input, output) {}

shinyApp(ui, server)
