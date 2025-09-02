# Crear una versión más simple y directa
from shiny import App, ui, render

# UI simple con deslizadera y casillero
app_ui = ui.page_fluid(
    ui.h3("Deslizadera"),
    
    # Deslizadera de 0 a 100
    ui.input_slider("mi_slider", "Valor:", min=0, max=100, value=50),
    
    # Casillero que muestra el valor
    ui.h4("Valor actual:"),
    ui.output_text("mi_casillero")
)

# Servidor que conecta la deslizadera con el casillero
def server(input, output, session):
    @render.text
    def mi_casillero():
        return str(input.mi_slider())

# Crear y ejecutar la app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()


