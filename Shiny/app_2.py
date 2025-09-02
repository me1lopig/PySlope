# Crear una aplicación Shiny con calculadora básica
from shiny import App, ui, render

# Definir la interfaz de usuario (UI)
app_ui = ui.page_fluid(
    ui.h2("Calculadora Básica con Shiny"),
    ui.br(),
    
    # Entradas numéricas
    ui.row(
        ui.column(6, ui.input_numeric("num1", "Primer número:", value=10)),
        ui.column(6, ui.input_numeric("num2", "Segundo número:", value=5))
    ),
    
    ui.br(),
    ui.h4("Resultados de las operaciones:"),
    ui.hr(),
    
    # Salidas de las operaciones
    ui.row(
        ui.column(6,
            ui.h5("Suma:"),
            ui.output_text("suma"),
            ui.br(),
            ui.h5("Resta:"),
            ui.output_text("resta"),
            ui.br(),
            ui.h5("Multiplicación:"),
            ui.output_text("multiplicacion")
        ),
        ui.column(6,
            ui.h5("División:"),
            ui.output_text("division"),
            ui.br(),
            ui.h5("Potencia:"),
            ui.output_text("potencia")
        )
    )
)

# Definir la lógica del servidor
def server(input, output, session):
    
    @render.text
    def suma():
        try:
            resultado = input.num1() + input.num2()
            return f"{input.num1()} + {input.num2()} = {resultado}"
        except:
            return "Error en el cálculo"
    
    @render.text
    def resta():
        try:
            resultado = input.num1() - input.num2()
            return f"{input.num1()} - {input.num2()} = {resultado}"
        except:
            return "Error en el cálculo"
    
    @render.text
    def multiplicacion():
        try:
            resultado = input.num1() * input.num2()
            return f"{input.num1()} × {input.num2()} = {resultado}"
        except:
            return "Error en el cálculo"
    
    @render.text
    def division():
        try:
            if input.num2() == 0:
                return f"{input.num1()} ÷ {input.num2()} = Error: División por cero"
            resultado = input.num1() / input.num2()
            return f"{input.num1()} ÷ {input.num2()} = {resultado:.4f}"
        except:
            return "Error en el cálculo"
    
    @render.text
    def potencia():
        try:
            resultado = input.num1() ** input.num2()
            return f"{input.num1()}^{input.num2()} = {resultado}"
        except:
            return "Error en el cálculo"

# Crear la aplicación
app = App(app_ui, server)

