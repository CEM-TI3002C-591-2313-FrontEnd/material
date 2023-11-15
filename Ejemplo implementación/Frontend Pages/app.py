import dash
from dash import Dash, html, dcc

backend_url = "http://localhost:8000/api"

external_stylesheets = [
    {
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",
        "crossorigin": "anonymous"
    }
]
external_scripts = [
    {
        "src": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL",
        "crossorigin":"anonymous"
    }
]

app = Dash(__name__,
           external_stylesheets=external_stylesheets,
           external_scripts=external_scripts,
           use_pages=True)
    
app.layout = html.Div([
    html.Nav([
        html.Div([
            dcc.Link([
                html.Img(src="assets/liverpool-logo.svg", alt="Logo de Liverpool"),
                ], href="/", className="navbar-brand"),
            html.Button([
                html.Span(className="navbar-toggler-icon")
            ], className="navbar-toggler", 
                        type="button", 
                        **{"data-bs-toggle": "collapse", 
                           "data-bs-target": "#navbarNav", 
                           "aria-controls": "navbarNav", 
                           "aria-expanded": "false", 
                           "aria-label": "Toggle navigation"}),
            html.Div([
                html.Div([
                    dcc.Link("Contexto", href="/", className="nav-link text-light"),
                    dcc.Link("Hallazgos", href="/hallazgos", className="nav-link text-light"),
                    dcc.Link("Predicciones", href="/predicciones", className="nav-link text-light"),
                    ], className="navbar-nav ms-auto"),
            ], className="collapse navbar-collapse", id="navbarNav"),
            ], className="container-fluid"),
        ], className="navbar navbar-expand-lg encabezado"),
    dash.page_container,
    html.Footer([
        html.P("Ejemplo frontend", className="text-center text-body-secondary")
    ], className="border-top py-3 my-4")
])

if __name__ == "__main__":
    app.run_server(debug=True)
    # app.run(host="0.0.0.0")
