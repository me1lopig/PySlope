from shiny import App, ui, render

# Define UI for application
app_ui = ui.page_fluid(
    ui.input_slider("n", "N", 0, 100, 20),
    ui.output_text("txt")
)

# Define server logic
def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"El valor seleccionado es: {input.n()}"

# Create Shiny app
app = App(app_ui, server)

# Run the app
if __name__ == "__main__":
    app.run()


