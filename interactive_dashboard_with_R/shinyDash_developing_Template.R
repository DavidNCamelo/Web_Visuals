library(shiny)
library(shinydashboard)
library(bslib)
library(plotly)

ui <- dashboardPage(
  dashboardHeader(
    title = tags$div(
      class = "header-bar",
      tags$div(class = "logo-area", "Company Logo"),
      tags$div(class = "title-area", "Dashboard Title")
    ),
    titleWidth = "100%"
  ),
  dashboardSidebar(disable = TRUE),
  dashboardBody(
    tags$head(
      tags$style(HTML("
        .main-header .navbar {
          display: none;
        }

        .header-bar {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 100%;
          height: 50px;
          background-color:rgb(131, 43, 8);
          padding: 0  10px;
          box-sizing: border-box;
          overflow: hidden;
        }

        .logo-area {
          color: white;
          font-size: 18px;
          font-weight: bold;
          white-space: nowrap;
          flex-shrink: 0;
          margin-right: auto;
        }

        .title-area {
          color: black;
          font-size: 20px;
          font-weight: bold;
          white-space: nowrap;
          text-align: center;
          margin: 0 auto;
          flex-grow: 1;
          min-width: 0;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .main-header .logo {
          width: 100% !important;
        }
      "))
    ),

      #Fila de filtros
    fluidRow(
      column(3, 
        selectInput(
          "año",
          "Año",
          choices = c(2023, 2024, 2025)
        )
      ),

      column(3, 
        selectInput(
          "categoria",
          "Categoría",
          choices = c("cat1", "cat2", "cat3")
        )
      ),

      column(3, 
        selectInput(
          "subcategoria",
          "Subcategoría",
          choices = c("subcat1", "subcat2", "subcat3", "subcat4", "subcat5", "subcat6", "subcat7", "subcat8", "subcat9")
        )
      ),

      column(3, 
        selectInput(
          "producto",
          "Producto",
          choices = c("prod1", "prod2", "prod3", "prod4", "prod5", "prod6", "prod7", "prod8", "prod9", "prod10", "prod11",
                    "prod12", "prod13", "prod14", "prod15")
        )
      )
    ),

    page_fluid(
        # Fila indicadores
      layout_columns(
        value_box(
          "Unids Plan",
          value = textOutput("unids_plan"),
          style = "min-height: 8px; padding: 8px;"
        ),

        value_box(
          "Unids Comp",
          value = textOutput("unids_comp"),
          style = "min-height: 8px; padding: 8px;"
        ),

        value_box(
          "desv",
          value = textOutput("unids_desv"),
          style = "min-height: 8px; padding: 8px;"
        ),

        value_box(
          "Presup Plan",
          value = textOutput("presp_plan"),
          style = "min-height: 8px; padding: 8px;"
        ),

        value_box(
          "Presup Ejec",
          value = textOutput("presp_plan"),
          style = "min-height: 8px; padding: 8px;"
        ),

        value_box(
          "desv Presp",
          value = textOutput("desv_presp"),
          style = "min-height: 8px; padding: 8px;"
        ),

        col_widths = rep(2, 6)
      ),

      # Primera Fila de Gráficos
      layout_columns(
        
        card(
          full_screen = TRUE,
          card_header("Desviación Mes"),
          plotlyOutput(
            "desvmom",
            height = "200px"
          )
        ),

        card(
          full_screen = TRUE,
          card_header("Desviación Cat"),
          plotlyOutput(
            "desvcat",
            height = "200px"
          )
        ),

        col_widths = c(8, 4)
      ),

      # Tabla detalle
      layout_columns(
        card(
          full_screen = TRUE,
          card_header("Resumen de Datos"),
          div(
            style = "min-height: 25vh; overflow-y: auto;",  # Cambia esto según lo que necesites
            tableOutput("tabla")
          )
        ),
        col_widths = 12
      )
    )
    
  )
)

server <- function(input, output) {}

shinyApp(ui, server)
