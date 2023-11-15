import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_ag_grid as dag
import plotly.express as px
import base64
import io
import json
import requests

dash.register_page(__name__,
                   path="/predicciones",
                   title="Predicciones",
                   name="Predicciones")

backend_url = "http://localhost:8000/api"

def layout():
    return html.Div([
        html.Div([
            dcc.Store(id="predictions-store"),
            html.H2("Predicciones"),
            html.P("Para poder llevar a cabo las predicciones, se debe proporcionar un archivo csv que debe contener los siguientes campos", className="parrafo"),
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Campo"),
                        html.Th("Contenido")
                    ])
                ]),
                html.Tbody(
                    [html.Tr([html.Td(f"Campo {x}"), html.Td(f"Contenido {x}")]) for x in range(1, 6)]
                    ),
                ], className="table table-striped table-hover table-bordered mt-3 mb-5")
        ], className="row"),
        html.Div([
            html.Div([
                dcc.Upload(id="uploaded-data", children=
                           html.Div([
                               "Arrastra o ", 
                               html.A("selecciona el archivo",
                                      className="link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover link-archivo")]), 
                           className="text-center p-3 border border-2 rounded-3")
                ], className="col-4")
            ], className="row mb-3 justify-content-md-center"),
        html.Div(id="predicciones-container", className="row"),
        html.Div([
            html.Div([
                html.Button("Descargar archivo de predicciones", id="download-predictions-btn", className="btn btn-primary btn-lg mt-3 mb-5"),
                dcc.Download(id="download-predictions")
            ], className="col-4 text-center")
            ],
                 id="download-predictions-container",
                 className="row justify-content-center invisible")
        ], className="container mt-3")
    
@callback(
    [Output("predicciones-container", "children"),
     Output("download-predictions-container", "className"),
     Output("predictions-store", "data")],
    Input("uploaded-data", "contents"),
    State("uploaded-data", "filename"),
    prevent_initial_call=True)
def upload_prediction(content, filename):
    if content is not None:
        try:
            content_type, content_string = content.split(",")
            decoded = base64.b64decode(content_string)
            if "csv" in filename:
                df_predictions = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
                # Revisar que las columnas se encuentren en el dataframe
                columnas = ["Age", "BusinessTravel", "DailyRate", "Department", 
                            "DistanceFromHome", "Education", "EducationField", "EmployeeCount", 
                            "EnvironmentSatisfaction", "Gender", "HourlyRate", "JobInvolvement", 
                            "JobLevel", "JobRole", "JobSatisfaction", "MaritalStatus", "MonthlyIncome", 
                            "MonthlyRate", "NumCompaniesWorked", "Over18", "OverTime", "PercentSalaryHike", 
                            "PerformanceRating", "RelationshipSatisfaction", "StandardHours", "StockOptionLevel", 
                            "TotalWorkingYears", "TrainingTimesLastYear", "WorkLifeBalance", "YearsAtCompany", 
                            "YearsInCurrentRole", "YearsSinceLastPromotion", "YearsWithCurrManager"]
                for col in columnas:
                    if col not in df_predictions.columns:
                        return html.Div([
                            f"El archivo no contiene la columna {col}"
                        ], className="alert alert-danger"), "row justify-content-center invisible", None
                df_predictions = df_predictions[columnas]
                
                try:
                    url = f"{backend_url}/prediction_file"
                    response = requests.post(url, files={
                        "file": decoded
                        })
                    json_response = json.loads(response.text)
                    df_predictions = pd.DataFrame(json_response)
                except Exception as e:
                    print(e)
                    df_predictions["Attrition"] = "NA"
                
                df_predictions_pie = df_predictions["Attrition"].value_counts().reset_index()
                fig = px.pie(df_predictions_pie, 
                        values="count", 
                        names="Attrition", 
                        title="Porcentaje de renuncias según predicción", 
                        color_discrete_sequence=px.colors.sequential.Agsunset)
                    
                return html.Div([
                    html.Div([
                        html.H3("Datos para predicción"),
                        dag.AgGrid(rowData=df_predictions.to_dict("records"),
                                columnDefs=[{"field": col, "sortable": True, "filter": True} for col in df_predictions.columns],
                                dashGridOptions= {"pagination": True, "pageSize": 10}),
                    ], className="row mb-5"),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H5("Predicciones de renuncias", className="card-title"),
                                html.P("Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, voluptatum.", className="card-text"),
                                dcc.Graph(id="predictions-pie-chart", figure=fig)
                            ], className="card-body")
                        ], className="card")
                    ], className="row mb-5"),
                ]), "row justify-content-center", df_predictions.to_json(orient="split")
            else:
                return html.Div([
                    "El archivo debe ser de tipo csv"
                ], className="alert alert-danger"), "row justify-content-center invisible", None
        except Exception as e:
            return html.Div([
                "Hubo un error al procesar el archivo"
            ], className="alert alert-danger"), "row justify-content-center invisible", None
            
@callback(
    Output("download-predictions", "data"),
    Input("download-predictions-btn", "n_clicks"),
    State("predictions-store", "data"),
    prevent_initial_call=True)
def download_predictions(n_clicks, data):
    if data is not None:
        df = pd.read_json(io.StringIO(data), orient="split")
        return dcc.send_data_frame(df.to_csv, "predictions.csv", index=False)