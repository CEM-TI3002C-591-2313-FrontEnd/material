from dash import Dash, html, dash_table, dcc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

def load_dataset():
    return pd.read_csv("datos.csv")

df = load_dataset()

fig = px.histogram(df, x="JobSatisfaction", nbins=5)

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
           external_scripts=external_scripts)

app.layout = html.Div(children=[
    html.H1(children="Hola mundo"),
    html.P(children="Mi primera página con Dash.", id="mi primer p", className="text-bg-primary p-3"),
    dash_table.DataTable(data=df.to_dict("records"), page_size=10),
    dag.AgGrid(rowData=df.to_dict("records"),
               columnDefs=[{"field": col, "sortable": True, "filter": True} for col in df.columns],
               dashGridOptions= {"pagination": True, "pageSize": 10}
               ),
    dcc.Graph(figure=fig)
], className="container")

# [
#     {"field": "Age", "editable": True, "sortable": True, "filter": True},
#     {"field": "Attrition", "editable": True, "sortable": True, "filter": True},
#     {"field": "BusinessTravel", "editable": True, "sortable": True, "filter": True},
# ]

# <div>
#     <h1>Hola mundo</h1>
#     <p>Mi primera página con Dash.</p>
# </div>

if __name__ == "__main__":
    app.run_server(debug=True)