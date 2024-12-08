import re
from typing import Optional, Dict
import pandas as pd

class ChatbotResponse:
    def __init__(self, message: str, data: Optional[Dict] = None):
        self.message = message
        self.data = data

def process_chat_message(message: str, data: Optional[pd.DataFrame]) -> ChatbotResponse:
    """
    Enhanced chatbot processing with more sophisticated response handling
    """
    message = message.lower()
    
    # Extract forecast parameters from message
    horizon_match = re.search(r'forecast.*?(\d+)\s*(day|week|month)', message)
    if horizon_match:
        days = int(horizon_match.group(1))
        unit = horizon_match.group(2)
        if unit == 'week':
            days *= 7
        elif unit == 'month':
            days *= 30
            
        return ChatbotResponse(
            message="Creating forecast...",
            data={"action": "forecast", "horizon": days}
        )
    
    # Handle different types of queries
    if "help" in message:
        return ChatbotResponse("""I can help you with:
        - Uploading data (ask about 'upload')
        - Creating forecasts (e.g., 'forecast next 7 days')
        - Viewing data statistics (ask about 'stats')
        - Understanding forecast methods (ask about 'methods')""")
        
    elif "methods" in message:
        return ChatbotResponse("""Available forecasting methods:
        1. Moving Average: Simple average of recent values
        2. Exponential Smoothing: Weighted average with more weight on recent data
        3. ARIMA: Advanced time series forecasting""")
    
    elif "stats" in message and data is not None:
        stats = {
            "records": len(data),
            "date_range": f"{data['date'].min()} to {data['date'].max()}",
            "avg_sales": data['sales'].mean()
        }
        return ChatbotResponse("Here are your data statistics:", stats)
        
    return ChatbotResponse("I'm sorry, I don't understand. Type 'help' for available commands.")