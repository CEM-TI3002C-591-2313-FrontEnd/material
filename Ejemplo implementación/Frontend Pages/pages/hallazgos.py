import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import json
import requests

dash.register_page(__name__,
                   path="/hallazgos",
                   title="Hallazgos",
                   name="Hallazgos")

backend_url = "http://localhost:8000/api"

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

def layout():
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
    
@callback(
    Output("educationfield-violin-chart-container", "children"),
    Input("educationfield-dropdown", "value"))
def update_educationfield_violin_chart(education_fields):
    if isinstance(education_fields, str):
        education_fields = [education_fields]
    return [dcc.Graph(id=f"educationfield-violin-{x}-chart", figure=educationlevel_violin_chart(x)) for x in education_fields]