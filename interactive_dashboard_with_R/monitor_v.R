# Monitor v1
# Required libraries
library(shiny)
library(bslib)
library(plotly)

# Creating UI
ui <- page_fluid(  
  
  # Theme
  theme = bs_theme(
    bg = "#e7d1c4",
    fg = "#000000"
  ),

  #Header
  tags$div(
  style = "
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 50px;
    padding: 0 10px;
    border-bottom: 1px solid #ccc;
    position: relative;
    overflow: hidden;
  ",
  # Logo
  tags$div(
    tags$img(
      src = "logo",
      style = "height: 45px;"
    ),
    style = "flex: 0 0 auto;"
  ),
  # Title
  tags$div(
    tags$h1(
      "Dashboard",
      style = "
        font-weight: bold;
        font-size: 36px;
        margin: 0;
        line-height: 45px;
        text-align: center;
      "
    ),
    style = "
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      height: 50px;
      display: flex;
      align-items: center;
      justify-content: center;
    "
    ),
  ),

  # Styling filters
  tags$head(
    tags$style(HTML("
      .custom-container {
        background-color: #f8efda;
        border-radius: 5px;
        padding: 5px 0 0 10px;
        margin-bottom: 10px;
      }

      .custom-container label {
        font-weight: bold;
        color: #000;
      }

      .custom-container select {
        background-color: #f8efda !important;
        color: #000 !important;
        border: 1px solid #859da7 !important;
        border-radius: 4px;
        box-shadow: none !important;
      }

      .custom-container .selectize-control.single .selectize-input {
        background-color: #f8efda !important;
        border: 1px solid #859da7 !important;
        color: #000 !important;
      }
    "))
  ),

  # Filters
  layout_columns(
    div(
      style = "flex: 1; background: #f8efda; padding-left: 10px; border-radius: 5px;
      display: flex; flex-direction: column; justify-content: flex-start;",
      div(class = "custom-container",
        selectInput(
          "seg_year",
          label = tags$strong("Year Filter"),
          choices = c(2023, 2024, 2025),
          selected = max(c(2023, 2024, 2025))
        )
      )
    ),

    div(
      style = "flex: 1; background: #f8efda; padding-left: 10px; border-radius: 5px;
      display: flex; flex-direction: column; justify-content: flex-start;",
      div(class = "custom-container",
          selectInput(
          "seg_c",
          label = tags$strong("Second Slicer"),
          choices = c("Todos" = "ALL", c("cat1", "cat2", "cat3"))
        )
      )
    ),

    div(
      style = "flex: 1; background: #f8efda; padding-left: 10px; border-radius: 5px;
      display: flex; flex-direction: column; justify-content: flex-start;",
      div(class = "custom-container",
          selectInput(
          "seg_s",
          label = tags$strong("Third Slicer"),
          choices = c("Todos" = "ALL", c("subcat1", "subcat2", "subcat3", "subcat4", "subcat5", "subcat6", "subcat7", "subcat8", "subcat9"))
        )
      )
    ),
    
    col_widths = c(4, 4, 4),
    style = "margin-top: 5px; margin-bottom: 5px;"
  ),

  # KPI Row
  fluidRow(
    div(
      style = "display: flex; gap: 10px; margin-bottom: 20px;",
      
      div(
        style = "flex: 1; background: #f8efda; padding: 10px; border-radius: 5px;
                 display: flex; flex-direction: column;
                 align-items: center; justify-content: center;",
        tags$h4("KPI1", style = "font-size: 14px; font-weight: bold; margin: 0;"),
        div(style = "text-align: center; width: 100%;", textOutput("kpi1"))
      ),
      
      div(
        style = "flex: 1; background: #f8efda; padding: 10px; border-radius: 5px;
                 display: flex; flex-direction: column;
                 align-items: center; justify-content: center;",
        tags$h4("KPI2", style = "font-size: 14px; font-weight: bold; margin: 0;"),
        div(style = "text-align: center; width: 100%;", textOutput("kpi2"))
      ),
      
      div(
        style = "flex: 1; background: #f8efda; padding: 10px; border-radius: 5px;
                 display: flex; flex-direction: column;
                 align-items: center; justify-content: center;",
        tags$h4("KPI3", style = "font-size: 14px; font-weight: bold; margin: 0;"),
        div(style = "text-align: center; width: 100%;", textOutput("kpi3"))
      ),
      
      div(
        style = "flex: 1; background: #f8efda; padding: 10px; border-radius: 5px;
                 display: flex; flex-direction: column;
                 align-items: center; justify-content: center;",
        tags$h4("KPI4", style = "font-size: 14px; font-weight: bold; margin: 0;"),
        div(style = "text-align: center; width: 100%;", textOutput("kpi4"))
      )
    ),
    style = "margin-top: 5px; margin-bottom: 5px;"
  ),
  
  # Graph container
  tags$style(HTML("
    .custom-graph-container {
      background-color: #f8efda;
      border-radius: 5px;
      padding: 10px;
      margin-bottom: 10px;
      margin-right: 5px;
      margin-left: 5px;
    }
  ")),

  # Tab panel
  tags$style(HTML("
    /* Drop background and edges */
    .nav-tabs {
      border-bottom: none !important;
    }

    .nav-tabs > li > a {
      border: none !important;
      background-color: transparent !important;
      color: black !important;
      font-weight: normal !important;
    }

    .nav-tabs > li.active > a,
    .nav-tabs > li.active > a:focus,
    .nav-tabs > li.active > a:hover,
    .nav-tabs > li > a.nav-link.active {
      font-weight: bold !important;
      color: black !important;
      border: none !important;
      background-color: transparent !important;
      box-shadow: none !important;
    }
  ")),

  # First graph row
  layout_columns(
    # Graph 1
    div(
      class = 'custom-graph-container',
      style = "padding: 10px; height: 40vh;",
      div("Graph 1", 
          style = "font-weight: bold; font-size: 16px; margin-bottom: 10px;"),
      plotlyOutput("gr1", height = "calc(100% - 30px)")  # adaptative height
    ),
    
    # Tab graph panel
    div(
      class = 'custom-graph-container',
      style = "padding: 5px; height: 40vh;",
      tabsetPanel(
        nav_panel("Graph tab 1", 
          div(
            style = "height: 32vh; overflow-y: auto;",                # Include vertical scroll if needed (for h-bar charts)
            plotlyOutput("tab1") 
          )
        ),
        nav_panel("Graph tab 2", 
          div(
            style = "height: 32vh; overflow-y: auto;",                # Include vertical scroll if needed (for h-bar charts)
            plotlyOutput("tab2")
          )
        )
      )
    ),
    col_widths = c(7, 5),
    style = "margin-top: 5px; margin-bottom: 5px; gap: 5px;"
  ),
  
  # Detailed tables
  div(
    class = 'custom-graph-container',
    layout_columns(
      card(
        full_screen = TRUE,
        card_header("Table"),
        div(
          style = "max-height: 25vh; overflow-y: auto;",  
          tableOutput("tabla")
        )
      ),
      col_widths = 12,
      style = "margin-top: 5px; margin-bottom: 5px;"
    )
  )
)

shinyApp(ui, server = function(input, output, session) {})