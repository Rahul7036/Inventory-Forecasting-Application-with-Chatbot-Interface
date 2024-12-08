import pandas as pd
import numpy as np
from .models import ForecastParameters, ForecastResult
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA

def generate_forecast(data: pd.DataFrame, params: ForecastParameters):
    """
    Generate forecast based on historical data and parameters
    """
    try:
        # Ensure data is sorted by date
        if 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'])
            data = data.sort_values('date')

        # Use only recent months if specified
        if params.recent_months:
            data = data.tail(params.recent_months * 30)

        if params.method == "moving_average":
            values = data['sales'].rolling(window=7).mean()
            last_value = values.iloc[-1]
            forecast = [last_value] * params.horizon
            
        elif params.method == "exponential_smoothing":
            model = ExponentialSmoothing(
                data['sales'],
                seasonal_periods=7,
                trend='add',
                seasonal='add'
            )
            fitted_model = model.fit()
            forecast = fitted_model.forecast(params.horizon)
            
        elif params.method == "arima":
            model = ARIMA(data['sales'], order=(1, 1, 1))
            fitted_model = model.fit()
            forecast = fitted_model.forecast(params.horizon)
            
        else:
            raise ValueError(f"Unsupported forecasting method: {params.method}")
            
        return {
            "forecast": forecast.tolist(),
            "method": params.method,
            "horizon": params.horizon
        }

    except Exception as e:
        raise Exception(f"Error generating forecast: {str(e)}")