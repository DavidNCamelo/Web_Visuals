Implement htmltools instead of renderUI

```R
# In UI:
htmltools::div(
  class = "row",
  htmltools::div(
    class = "col-md-4",
    shiny::textOutput("value1")
  ),
  htmltools::div(
    class = "col-md-4",
    shiny::textOutput("value2")
  ),
  htmltools::div(
    class = "col-md-4",
    shiny::textOutput("value3")
  )
)
```