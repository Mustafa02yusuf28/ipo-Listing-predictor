from flask import Flask, request, jsonify
from flask_cors import CORS
from predictor import predict_ipo_listing_price
from sentiment_analysis import fetch_combined_news, analyze_sentiment
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/api/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        # Get data from request
        data = request.get_json()
        logger.info(f"Received prediction request for {data.get('company_name', 'Unknown Company')}")
        
        # Validate required fields
        required_fields = ['company_name', 'issue_price', 'market_cap', 'gmp', 'roce', 'roe', 'industry_growth']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
                
        # Convert numeric fields
        try:
            numeric_data = {
                'issue_price': float(data['issue_price']),
                'market_cap': float(data['market_cap']),
                'gmp': float(data['gmp']),
                'roce': float(data['roce']),
                'roe': float(data['roe']),
                'industry_growth': float(data['industry_growth'])
            }
        except ValueError as e:
            return jsonify({'error': f'Invalid numeric value: {str(e)}'}), 400
            
        # Fetch and analyze news
        news_articles = fetch_combined_news(data['company_name'])
        analyzed_articles, sentiment_score = analyze_sentiment(news_articles)
        
        # Make prediction
        prediction = predict_ipo_listing_price(
            issue_price=numeric_data['issue_price'],
            market_cap=numeric_data['market_cap'],
            gmp=numeric_data['gmp'],
            roce=numeric_data['roce'],
            roe=numeric_data['roe'],
            industry_growth=numeric_data['industry_growth'],
            sentiment_score=sentiment_score
        )
        
        # Prepare response with default values if prediction fails
        response = {
            'predicted_price': prediction.get('predicted_price', 0),
            'expected_return': prediction.get('expected_return', 0),
            'sentiment_score': sentiment_score,
            'news_articles': analyzed_articles or [],
            'gmp_contribution': prediction.get('gmp_contribution', 0),
            'market_cap_contribution': prediction.get('market_cap_contribution', 0),
            'roce_contribution': prediction.get('roce_contribution', 0),
            'roe_contribution': prediction.get('roe_contribution', 0),
            'industry_growth_contribution': prediction.get('industry_growth_contribution', 0),
            'sentiment_contribution': prediction.get('sentiment_contribution', 0)
        }
        
        logger.info(f"Prediction completed for {data['company_name']}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'An error occurred while making the prediction'}), 500

if __name__ == '__main__':
    app.run(debug=True) 