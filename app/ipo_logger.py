import os
import json
import pandas as pd
from datetime import datetime

# Define the path for the log file
LOG_FILE = "data/ipo_predictions.csv"

def ensure_log_file_exists():
    """Ensure the log file exists, create it if it doesn't"""
    if not os.path.exists(os.path.dirname(LOG_FILE)):
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    if not os.path.exists(LOG_FILE):
        # Create a new log file with headers
        df = pd.DataFrame(columns=[
            "company_name", "issue_price", "predicted_price", "actual_price", 
            "prediction_date", "listing_date", "market_cap", "gmp", 
            "industry_growth", "roce", "roe", "sentiment_score"
        ])
        df.to_csv(LOG_FILE, index=False)
        return df
    else:
        # Load existing log file
        return pd.read_csv(LOG_FILE)

def log_prediction(prediction_data):
    """
    Log a new IPO prediction
    
    Args:
        prediction_data (dict): Dictionary containing prediction details
    """
    df = ensure_log_file_exists()
    
    # Create a new row with the prediction data
    new_row = {
        "company_name": prediction_data.get("company_name", ""),
        "issue_price": prediction_data.get("issue_price", 0),
        "predicted_price": prediction_data.get("predicted_price", 0),
        "actual_price": None,  # Will be updated when listing price is known
        "prediction_date": datetime.now().strftime("%Y-%m-%d"),
        "listing_date": None,  # Will be updated when listing date is known
        "market_cap": prediction_data.get("market_cap", 0),
        "gmp": prediction_data.get("gmp", 0),
        "industry_growth": prediction_data.get("industry_growth", 0),
        "roce": prediction_data.get("roce", 0),
        "roe": prediction_data.get("roe", 0),
        "sentiment_score": prediction_data.get("sentiment_score", 0)
    }
    
    # Append the new row to the dataframe
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Save the updated dataframe
    df.to_csv(LOG_FILE, index=False)
    
    return new_row

def update_actual_price(company_name, actual_price, listing_date=None):
    """
    Update the actual listing price for a company
    
    Args:
        company_name (str): Name of the company
        actual_price (float): Actual listing price
        listing_date (str, optional): Date of listing in YYYY-MM-DD format
    """
    df = ensure_log_file_exists()
    
    # Find the row with the matching company name
    mask = df["company_name"] == company_name
    
    if not any(mask):
        return False, "Company not found in logs"
    
    # Update the actual price and listing date
    df.loc[mask, "actual_price"] = actual_price
    
    if listing_date:
        df.loc[mask, "listing_date"] = listing_date
    
    # Save the updated dataframe
    df.to_csv(LOG_FILE, index=False)
    
    return True, "Actual price updated successfully"

def get_prediction_history():
    """
    Get the history of all predictions
    
    Returns:
        list: List of dictionaries containing prediction history
    """
    df = ensure_log_file_exists()
    return df.to_dict(orient="records") 