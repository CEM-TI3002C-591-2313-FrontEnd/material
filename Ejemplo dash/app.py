from dash import Dash, html, dash_table, dcc, Input, Output, State, callback
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

def load_dataset():
    return pd.read_csv("datos.csv")

def get_histogram():
    fig = px.histogram(df, x="JobSatisfaction", nbins=5)
    return fig

def get_scatter1():
    fig = px.scatter(df, x="JobSatisfaction", y="MonthlyIncome")
    fig.update_layout(
        xaxis = {
            "tickmode": "linear",
            "tick0": 1, # en qué valor inicia el eje x
            "dtick": 1 # de cuánto en cuánto se increementa el valor en el eje x
        }
    )
    return fig

def get_scatter2():
    fig = px.scatter(df, x="JobSatisfaction", y="MonthlyIncome", color="Attrition", size="DailyRate")
    fig.update_layout(
        xaxis = {
            "title": "Satisfacción del empleado",
            "tickmode": "array",
            "tickvals": [1,2,3,4,5],
            "ticktext": [
                "Muy poco satisfecho",
                "Poco satisfecho",
                "Satisfecho",
                "Algo satisfecho",
                "Muy satisfecho"
            ]
        }
    )
    return fig

def get_bar():
    df_montlyincome = df.groupby(["JobSatisfaction", "Attrition"])["MonthlyIncome"].mean().reset_index()
    fig = px.bar(df_montlyincome, 
                 x="JobSatisfaction", 
                 y="MonthlyIncome", 
                 color="Attrition", 
                 pattern_shape="Attrition",
                 pattern_shape_sequence=["x", "+"],
                 barmode="group")
    fig.update_layout(
        xaxis = {
            "title": "Satisfacción del empleado",
            "tickmode": "array",
            "tickvals": [1,2,3,4,5],
            "ticktext": [
                "Muy poco satisfecho",
                "Poco satisfecho",
                "Satisfecho",
                "Algo satisfecho",
                "Muy satisfecho"
            ]
        },
        yaxis = {
            "title": "Ingreso mensual promedio",
            "tickprefix": "$",
            "ticksuffix": " USD",
            "tickformat": ",.0f"
        }
    )
    return fig

def get_line():
    fig = px.line(df, y="DailyRate", color="Department", title="Gráfica de líneas") # x="EscalaTiempo"
    return fig

def get_pie():
    fig = px.pie(df, values="MonthlyIncome", names="Department", hole=0.5)
    return fig

def get_boxplot():
    fig = px.box(df, y="MonthlyIncome")
    return fig

def get_violin():
    fig = px.violin(df, y="MonthlyIncome", color="Attrition", box=True)
    return fig

def get_chart(tipo_grafica : str, columna : str) -> object:
    if tipo_grafica == "hist":
        fig = px.histogram(df, y=columna)
    elif tipo_grafica == "violin":
        fig = px.violin(df, y=columna)
    return fig

df = load_dataset()
histogram = get_histogram()
scatter1 = get_scatter1()
scatter2 = get_scatter2()
bar = get_bar()
line = get_line()
pie = get_pie()
boxplot = get_boxplot()
violin = get_violin()

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
    dcc.Graph(figure=histogram),
    dcc.Graph(figure=scatter1),
    dcc.Graph(figure=scatter2),
    dcc.Graph(figure=bar),
    dcc.Graph(figure=line),
    dcc.Graph(figure=pie),
    dcc.Graph(figure=boxplot),
    dcc.Graph(figure=violin),
    dcc.Checklist(options=[
        {"label": "Uno", "value": "1"},
        {"label": "Dos", "value": "2"},
        {"label": "Tres", "value": "3"},
    ], id="checklist"),
    dcc.Input(type="text", id="input texto"),
    dcc.RadioItems([
        {"label": "Histograma", "value": "hist"},
        {"label": "Violín", "value": "violin"}
    ], value="hist", id="radio tipo gráfica"),
    dcc.Dropdown(options = [
        {"label": "Edad", "value": "Age"},
        {"label": "Tasa diaria", "value": "DailyRate"},
        {"label": "Educación", "value": "Education"}
    ], value="Age", id="dropdown columna"),
    html.Div(id="contenedor gráfica")
], className="container")

@callback(
    Output("contenedor gráfica", "children"),
    Input("radio tipo gráfica", "value"),
    Input("dropdown columna", "value")
)
def mi_funcion(radio_tipo_grafica, dropdown_columna):
    return dcc.Graph(figure=get_chart(radio_tipo_grafica, dropdown_columna))
        

if __name__ == "__main__":
    app.run_server(debug=True)