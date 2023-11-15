import pandas as pd
from dash import Dash, html, dcc, callback, Input, Output, State
import dash_ag_grid as dag
import plotly.express as px
import base64
import io
import json
import requests

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

# df = pd.read_csv("datos.csv")

app = Dash(__name__,
           external_stylesheets=external_stylesheets,
           external_scripts=external_scripts)

def contexto():
    return html.Div([
        html.H2("Objetivo del proyecto"),
        html.Div([
            html.Div([
                html.P("""Lorem, ipsum dolor sit amet consectetur adipisicing elit. Placeat temporibus porro perferendis consectetur quam eius voluptates eaque voluptas laudantium, animi rem illum neque earum iusto ea tenetur dignissimos reprehenderit quasi?
Officia omnis, beatae magnam nihil laudantium sed, eum fuga laborum ipsum dolorem natus voluptas veritatis atque praesentium. Amet veniam soluta, minima maxime praesentium veritatis asperiores numquam modi sapiente ad molestias!
Enim rerum aperiam explicabo praesentium corrupti quibusdam debitis, mollitia quo ea esse expedita nam quisquam natus, sit ex cumque corporis veniam libero aspernatur voluptatem quas. Quaerat cupiditate qui consectetur porro?
Quisquam quasi, quod sapiente dolorum, alias nihil inventore odio doloribus eaque optio molestias similique obcaecati voluptates, corrupti incidunt totam facere. Quidem deleniti incidunt iusto? At, eveniet impedit! Voluptas, nostrum repellat.""", className="parrafo")
                ], className="col-6"),
            html.Div([
                html.Img(src="assets/tienda.jpg", alt="Ejemplo de una tienda de Liverpool", className="img-fluid")
                ], className="col-6"),
            ], className="row mb-5"),
        html.Div([
            html.Div([
                html.Img(src="assets/renuncias.jpg", alt="Empleado sale con sus pertenencias después de renunciar.", className="img-fluid")
                ], className="col-4"),
            html.Div([
                html.P("""Lorem, ipsum dolor sit amet consectetur adipisicing elit. Placeat temporibus porro perferendis consectetur quam eius voluptates eaque voluptas laudantium, animi rem illum neque earum iusto ea tenetur dignissimos reprehenderit quasi?
Officia omnis, beatae magnam nihil laudantium sed, eum fuga laborum ipsum dolorem natus voluptas veritatis atque praesentium. Amet veniam soluta, minima maxime praesentium veritatis asperiores numquam modi sapiente ad molestias!
Enim rerum aperiam explicabo praesentium corrupti quibusdam debitis, mollitia quo ea esse expedita nam quisquam natus, sit ex cumque corporis veniam libero aspernatur voluptatem quas. Quaerat cupiditate qui consectetur porro?
Quisquam quasi, quod sapiente dolorum, alias nihil inventore odio doloribus eaque optio molestias similique obcaecati voluptates, corrupti incidunt totam facere. Quidem deleniti incidunt iusto? At, eveniet impedit! Voluptas, nostrum repellat.""", className="parrafo")
                ], className="col-8"),
            ], className="row mb-5"),
        ], className="container mt-3")
    
def department_pie_chart():
    try:
        # df_department = df[df["Attrition"] == "Yes"]["Department"].value_counts().reset_index()
        url = f"{backend_url}/attrition_by_department"
        response = requests.get(url)
        json_response = json.loads(response.text)
        df_department = pd.DataFrame(json_response)
        fig = px.pie(df_department, 
                     values="count", 
                     names="Department", 
                     title="Renuncias según departamento", 
                     color_discrete_sequence=px.colors.sequential.Agsunset)
        return fig
    except Exception as e:
        print(e)
        return None

def stock_bar_chart():
    try:
        # df_stock = df.groupby(["StockOptionLevel"])["Attrition"].value_counts().reset_index()
        url = f"{backend_url}/attrition_by_stockoptionlevel"
        response = requests.get(url)
        json_response = json.loads(response.text)
        df_stock = pd.DataFrame(json_response)
        fig = px.bar(df_stock, 
                    x="StockOptionLevel", 
                    y="count", 
                    color="Attrition", 
                    barmode="group", 
                    title="Renuncias según opciones de compra de acciones", 
                    labels={"StockOptionLevel": "Opciones de compra de acciones", "count": "Número de renuncias", "Attrition": "Renuncias"},
                    color_discrete_sequence=px.colors.sequential.Agsunset)
        fig.update_layout(
            xaxis = {
                "tickmode": "array",
                "tickvals": [0, 1, 2, 3],
                "ticktext": ["Ninguna", "Baja", "Media", "Alta"]
            },            
        )
        return fig
    except Exception as e:
        print(e)
        return None

def educationlevel_violin_chart(education_field):
    try:
        # df_education = df[df["EducationField"] == education_field]
        url = f"{backend_url}/monthlyincome_by_educationfield/{education_field}"
        response = requests.get(url)
        json_response = json.loads(response.text)
        df_education = pd.DataFrame(json_response)
        fig = px.violin(df_education, 
                        x="MonthlyIncome", 
                        box=True, color="Attrition", 
                        labels={"Attrition": "Renunció", "MonthlyIncome": "Ingreso mensual"},
                        title=f"Salario mensual según campo de educación ({education_field})",
                        color_discrete_sequence=px.colors.sequential.Agsunset)
        return fig
    except Exception as e:
        print(e)
        return None

def hallazgos():
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Departamento al que pertenecen", className="card-title"),
                    html.P("Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, voluptatum.", className="card-text"),
                    dcc.Graph(id="department-pie-chart", figure=department_pie_chart())
                ], className="card-body")
            ], className="card")
        ], className="row mb-5"),
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Años desde el último ascenso", className="card-title"),
                    html.P("Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, voluptatum.", className="card-text"),
                    dcc.Graph(id="stockoption-bar-chart", figure=stock_bar_chart())
                ], className="card-body")
            ], className="card")
        ], className="row mb-5"),
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Salario mensual según campo de educación", className="card-title"),
                    html.P("Selecciona el campo de educación:", className="card-text"),
                    dcc.Dropdown(options=[
                        {"label": "Ciencias de la vida", "value": "Life Sciences"},
                        {"label": "Marketing", "value": "Marketing"},
                        {"label": "Medicina", "value": "Medical"},
                        {"label": "Recursos humanos", "value": "Human Resources"},
                        {"label": "Técnico", "value": "Technical Degree"},
                        {"label": "Otro", "value": "Other"},
                    ], value="Life Sciences", id="educationfield-dropdown", multi=True),
                    html.Div(id="educationfield-violin-chart-container")
                ], className="card-body")
            ], className="card")
        ], className="row mb-5"),
    ], className="container mt-3")
    
def predicciones():
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
    
app.layout = html.Div([
    html.Div([
        html.Img(src="assets/liverpool-logo.svg", alt="Logo de Liverpool"),
    ], className="container-fluid p-3 encabezado"),
    dcc.Tabs(id="tabs", value="tab-1", children=[
        dcc.Tab(label="Contexto", value="tab-1", children=contexto()),
        dcc.Tab(label="Hallazgos", value="tab-2", children=hallazgos()),
        dcc.Tab(label="Predicciones", value="tab-3", children=predicciones()),
    ]),
    html.Div(id="tab-content", className="container mt-3"),
    html.Footer([
        html.P("Ejemplo frontend", className="text-center text-body-secondary")
    ], className="border-top py-3 my-4")
])

@app.callback(
    Output("educationfield-violin-chart-container", "children"),
    Input("educationfield-dropdown", "value"))
def update_educationfield_violin_chart(education_fields):
    if isinstance(education_fields, str):
        education_fields = [education_fields]
    return [dcc.Graph(id=f"educationfield-violin-{x}-chart", figure=educationlevel_violin_chart(x)) for x in education_fields]

@app.callback(
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
            
@app.callback(
    Output("download-predictions", "data"),
    Input("download-predictions-btn", "n_clicks"),
    State("predictions-store", "data"),
    prevent_initial_call=True)
def download_predictions(n_clicks, data):
    if data is not None:
        df = pd.read_json(io.StringIO(data), orient="split")
        return dcc.send_data_frame(df.to_csv, "predictions.csv", index=False)

if __name__ == "__main__":
    app.run_server(debug=True)
    # app.run(host="0.0.0.0")