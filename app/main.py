from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import Optional
import io

from .forecasting import generate_forecast
from .models import ForecastParameters
from .chatbot import process_chat_message

app = FastAPI(title="Inventory Forecasting System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store uploaded data in memory (in a production environment, use a proper database)
global_data = None

@app.post("/upload-data/")
async def upload_data(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        global global_data
        global_data = df
        return {"message": "Data uploaded successfully", "columns": df.columns.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/forecast/")
async def create_forecast(params: ForecastParameters):
    if global_data is None:
        raise HTTPException(status_code=400, detail="No data has been uploaded yet")
    
    try:
        forecast_result = generate_forecast(global_data, params)
        return forecast_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/chat/")
async def chat(message: str):
    try:
        response = process_chat_message(message, global_data)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)