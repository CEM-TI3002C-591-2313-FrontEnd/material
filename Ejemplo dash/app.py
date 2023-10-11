from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children="Hola mundo"),
    html.P(children="Mi primera página con Dash.")
])

if __name__ == "__main__":
    app.run_server(debug=True)