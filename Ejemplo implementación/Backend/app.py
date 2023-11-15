from fastapi import FastAPI, status, File, UploadFile
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import pandas as pd
import uvicorn
import joblib

app = FastAPI()

mongoURI = "mongodb://localhost:27017"
model = joblib.load("GaussianNB_model.joblib")

@app.get("/api/attrition_by_department")
async def attrition_by_department():
    try:
        client = MongoClient(mongoURI)
        db = client["employee_attrition"]
        collection = db["employee"]
        
        # Usando pandas para agrupar
        # query = {
        #     "Attrition": "Yes"
        # }
        # cursor = collection.find(query, {"_id": 0})
        # df = pd.DataFrame(cursor)
        # df = df["Department"].value_counts().reset_index()
        # result = df.to_dict('records')
        # return JSONResponse(content = result)
        
        # Usando pymongo para agrupar
        cursor = collection.aggregate(
            [
                {
                    "$group": {
                        "_id": "$Department",
                        "count": {
                            "$sum": 1,
                            },
                        },
                    },
                {
                    "$project": {
                        "_id": 0,
                        "Department": "$_id",
                        "count": 1
                        }
                    }
                ])
        return JSONResponse(content = list(cursor))
        
    except Exception as e:
        print(e)
        return status.HTTP_400_BAD_REQUEST
    
@app.get("/api/attrition_by_stockoptionlevel")
async def attrition_by_stockoptionlevel():
    try:
        client = MongoClient(mongoURI)
        db = client["employee_attrition"]
        collection = db["employee"]
        
        # Usando pandas para agrupar
        # cursor = collection.find({}, {"_id": 0})
        # df = pd.DataFrame(cursor)
        # df = df.groupby(["StockOptionLevel"])["Attrition"].value_counts().reset_index()
        # result = df.to_dict('records')
        # return JSONResponse(content = result) 
        
        # Usando pymongo para agrupar
        cursor = collection.aggregate(
            [
                {
                    "$group": {
                        "_id": {
                            "StockOptionLevel": "$StockOptionLevel",
                            "Attrition": "$Attrition",
                            },
                        "count": {
                            "$sum": 1,
                            },
                        },
                    },
                {
                    "$project": {
                        "_id": 0,
                        "StockOptionLevel": "$_id.StockOptionLevel",
                        "Attrition": "$_id.Attrition",
                        "count": 1,
                        },
                    },
                ])
        return JSONResponse(content = list(cursor))
        
    except Exception as e:
        print(e)
        return status.HTTP_400_BAD_REQUEST
    
@app.get("/api/monthlyincome_by_educationfield/{education_field}")
async def educationlevel(education_field):
    try:
        client = MongoClient(mongoURI)
        db = client["employee_attrition"]
        collection = db["employee"]
        query = {
            "EducationField": education_field
        }
        cursor = collection.find(query, {"_id": 0, "MonthlyIncome": 1, "Attrition": 1})
        
        # Devolviendo resultado con pandas
        # df = pd.DataFrame(cursor)
        # result = df.to_dict('records')
        # return JSONResponse(content = result)
        
        # Devolviendo resultado con pymongo
        return JSONResponse(content = list(cursor))
    except Exception as e:
        print(e)
        return status.HTTP_400_BAD_REQUEST
    
@app.post("/api/prediction_file")
def prediction_file(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        df_pred = pd.get_dummies(df)
        df_pred_columns = pd.DataFrame(columns=model.feature_names_in_, dtype=bool)
        
        df_pred_columns, df_pred = df_pred_columns.align(df_pred, join='left', axis=1, fill_value=False)
        
        df_pred = df_pred[model.feature_names_in_]
        df["Attrition"] = model.predict(df_pred)
        
        # Para insertar los datos en una colección en MongoDB
        
        # client = MongoClient(mongoURI)
        # db = client["employee_attrition"]
        # collection = db["employee"]
        
        # collection.insert_many(df.to_dict('records'))
        
        return JSONResponse(content = df.to_dict('records'))
        
    except Exception as e:
        print(e)
        return status.HTTP_400_BAD_REQUEST

if __name__ == "__main__":
    uvicorn.run(app, port=8000)