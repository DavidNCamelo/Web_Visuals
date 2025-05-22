## Monitor 
# Librerías requeridas
library(shiny)
library(bslib)
library(plotly)

# Crear UI
ui <- page_fluid(  
  
  # Título del monitor
  tags$div(
    tags$h1(HTML("Monitor")),
    style = "text-align:center;"
  ),

  #Fila de filtros
  layout_columns(
    selectInput(
      "año",
      "Año",
      choices = c(2023, 2024, 2025)
    ),

    selectInput(
      "categoria",
      "Categoría",
      choices = c("cat1", "cat2", "cat3")
    ),

    selectInput(
      "subcategoria",
      "Subcategoría",
      choices = c("subcat1", "subcat2", "subcat3", "subcat4", "subcat5", "subcat6", "subcat7", "subcat8", "subcat9")
    ),

    selectInput(
      "producto",
      "Producto",
      choices = c("prod1", "prod2", "prod3", "prod4", "prod5", "prod6", "prod7", "prod8", "prod9", "prod10", "prod11",
                 "prod12", "prod13", "prod14", "prod15")
    ),
    
    col_widths = c(3, 3, 3, 3)
  ),

    
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

shinyApp(ui, server = function(input, output, session) {})
