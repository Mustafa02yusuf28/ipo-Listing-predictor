import os
import json
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from ipo_logger import log_prediction, update_actual_price, get_prediction_history
import logging
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Configure CORS to allow requests from all origins for API routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

def calculate_predicted_price(issue_price, gmp, market_cap, roce, roe, industry_growth):
    """
    Calculate predicted listing price based on financial factors.
    Focused on GMP, market cap, and financial metrics.
    
    Args:
        issue_price (float): IPO issue price in ₹
        gmp (float): Grey Market Premium in ₹
        market_cap (float): Market capitalization in Cr
        roce (float): Return on Capital Employed in %
        roe (float): Return on Equity in %
        industry_growth (float): Industry growth rate in %
        
    Returns:
        tuple: (predicted_price, calculation_breakdown)
    """
    try:
        # Weights based on historical IPO behavior
        weights = {
            'gmp': 0.60,        # 60% weight - Most important factor
            'market_cap': 0.20, # 20% weight - Inverse relationship
            'roce': 0.10,       # 10% weight
            'roe': 0.05,        # 5% weight
            'industry_growth': 0.05  # 5% weight
        }
        
        # 1. GMP Contribution (capped at 100% gain)
        gmp_percentage = (gmp / issue_price) * 100
        gmp_contribution = min(max(gmp_percentage, -50), 100) * weights['gmp']
        
        # 2. Market Cap Contribution (inverse relationship)
        market_cap_scaling = 2000  # Increased scaling factor
        market_cap_contribution = (1 / max(market_cap, 1)) * market_cap_scaling * weights['market_cap']
        
        # 3. Financial Metrics (ROCE and ROE)
        # Normalize negative values and cap at -50%
        roce_contribution = (max(roce, -50) / 100) * weights['roce'] * 100
        roe_contribution = (max(roe, -50) / 100) * weights['roe'] * 100
        
        # 4. Industry Growth
        industry_growth_contribution = (industry_growth / 100) * weights['industry_growth'] * 100
        
        # Calculate total weighted score
        weighted_score = (
            gmp_contribution +
            market_cap_contribution +
            roce_contribution +
            roe_contribution +
            industry_growth_contribution
        ) / 100  # Convert to decimal
        
        # Small caps protection (bonus for market cap < 500 Cr)
        if market_cap < 500:
            weighted_score *= 1.10  # 10% bonus for small caps
        
        # Clamp final weighted score
        weighted_score = max(-0.5, min(2, weighted_score))  # Limit between -50% and +200%
        
        # Calculate predicted price
        predicted_price = issue_price * (1 + weighted_score)
        
        # Prepare calculation breakdown with actual percentage contributions
        calculation_breakdown = {
            "gmp_contribution": f"{round(gmp_percentage * weights['gmp'], 2)}%",
            "market_cap_contribution": f"{round(market_cap_contribution, 2)}%",
            "roce_contribution": f"{round(roce * weights['roce'], 2)}%",
            "roe_contribution": f"{round(roe * weights['roe'], 2)}%",
            "industry_growth_contribution": f"{round(industry_growth * weights['industry_growth'], 2)}%",
            "small_cap_bonus": "10%" if market_cap < 500 else "0%",
            "total_contribution": f"{round(weighted_score * 100, 2)}%"
        }
        
        return round(predicted_price, 2), calculation_breakdown
        
    except Exception as e:
        logger.error(f"Error calculating predicted price: {str(e)}")
        return None, None

def prepare_features(data, sentiment_score):
    """
    Prepare features for prediction.
    
    Args:
        data (dict): Input data from request
        sentiment_score (float): News sentiment score
        
    Returns:
        numpy.ndarray: Prepared features array
    """
    try:
        # Extract and validate numeric values
        issue_price = float(data['issue_price'])
        market_cap = float(data['market_cap'])
        gmp = float(data['gmp'])
        roce = float(data['roce'])
        roe = float(data['roe'])
        industry_growth = float(data['industry_growth'])
        
        # Calculate GMP percentage
        gmp_percentage = (gmp / issue_price) * 100
        
        # Prepare features array
        features = np.array([[
            issue_price,
            market_cap,
            gmp_percentage,
            roce,
            roe,
            industry_growth
        ]])
        
        return features
        
    except Exception as e:
        logger.error(f"Error preparing features: {str(e)}")
        raise

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        logger.info(f"Received prediction request: {data}")
        
        # Validate required fields
        required_fields = ['company_name', 'issue_price', 'market_cap', 'gmp', 'roce', 'roe', 'industry_growth']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Convert all inputs to float
        issue_price = float(data['issue_price'])
        gmp = float(data['gmp'])
        market_cap = float(data['market_cap'])
        roce = float(data['roce'])
        roe = float(data['roe'])
        industry_growth = float(data['industry_growth'])
        
        # Calculate contributions
        gmp_percentage = (gmp / issue_price) * 100
        gmp_contribution = min(max(gmp_percentage, -50), 100) * 0.60
        
        market_cap_contribution = (1 / max(market_cap, 1)) * 2000 * 0.20
        
        roce_contribution = (max(roce, -50) / 100) * 0.10 * 100
        roe_contribution = (max(roe, -50) / 100) * 0.05 * 100
        
        industry_growth_contribution = (industry_growth / 100) * 0.05 * 100
        
        # Calculate total weighted score
        weighted_score = (
            gmp_contribution +
            market_cap_contribution +
            roce_contribution +
            roe_contribution +
            industry_growth_contribution
        ) / 100
        
        # Small caps protection
        if market_cap < 500:
            weighted_score *= 1.10
        
        # Clamp final weighted score
        weighted_score = max(-0.5, min(2, weighted_score))
        
        # Calculate predicted price
        predicted_price = issue_price * (1 + weighted_score)
        
        # Calculate expected return
        expected_return = ((predicted_price - issue_price) / issue_price) * 100
        
        # Prepare calculation breakdown
        calculation_breakdown = {
            "gmp_contribution": round(gmp_contribution, 2),
            "market_cap_contribution": round(market_cap_contribution, 2),
            "roce_contribution": round(roce_contribution, 2),
            "roe_contribution": round(roe_contribution, 2),
            "industry_growth_contribution": round(industry_growth_contribution, 2),
            "small_cap_bonus": "10%" if market_cap < 500 else "0%",
            "total_contribution": round(weighted_score * 100, 2)
        }
        
        logger.info(f"Calculation breakdown: {calculation_breakdown}")
        
        # Log prediction
        prediction_data = {
            "company_name": data['company_name'],
            "issue_price": issue_price,
            "predicted_price": predicted_price,
            "market_cap": market_cap,
            "gmp": gmp,
            "industry_growth": industry_growth,
            "roce": roce,
            "roe": roe
        }
        log_prediction(prediction_data)
        
        return jsonify({
            'predicted_price': round(predicted_price, 2),
            'expected_return': round(expected_return, 2),
            'calculation_breakdown': calculation_breakdown
        })
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/update-price', methods=['POST'])
def update_price():
    try:
        data = request.get_json()
        company_name = data.get('company_name')
        actual_price = float(data.get('actual_price', 0))
        listing_date = data.get('listing_date')
        
        if not company_name or not company_name.strip():
            return jsonify({"error": "Please enter a valid company name."}), 400
        
        if actual_price <= 0:
            return jsonify({"error": "Please enter a valid listing price."}), 400
            
        success, message = update_actual_price(company_name, actual_price, listing_date)
        
        if success:
            return jsonify({"message": message})
        else:
            return jsonify({"error": message}), 404
            
    except Exception as e:
        print(f"Error updating price: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        history = get_prediction_history()
        if history is None:
            return jsonify([])
            
        # Convert DataFrame to list of dictionaries
        history_list = history.to_dict('records')
        
        # Convert NaN values to None for JSON serialization
        for record in history_list:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
        
        return jsonify(history_list)
    except Exception as e:
        logger.error(f"Error fetching prediction history: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # 10000 is Render's default
    app.run(host="0.0.0.0", port=port) 