# Inventory Forecasting Application

A FastAPI-based application for inventory forecasting with chatbot interface.

## Features

- CSV data upload and processing
- Multiple forecasting methods (Moving Average, Exponential Smoothing, ARIMA)
- Interactive chatbot interface
- Real-time forecasting integration

## Installation

1. Clone the repository
2. Create virtual environment:

2. Access the API documentation at http://localhost:8000/docs

3. Upload your data using the /upload-data/ endpoint

4. Interact with the chatbot using the /chat/ endpoint

5. Generate forecasts using the /forecast/ endpoint

## API Endpoints

- POST /upload-data/: Upload CSV file with historical data
- POST /forecast/: Generate inventory forecasts
- POST /chat/: Interact with the chatbot

## Data Format

The CSV file should contain the following columns:
- date: Date of the record (YYYY-MM-DD)
- sales: Number of units sold
- inventory_level: Current inventory level