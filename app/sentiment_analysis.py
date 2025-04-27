import os
from dotenv import load_dotenv
from gnews import GNews
from textblob import TextBlob
import logging
import time
from datetime import datetime, timedelta
import json
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables and verify API keys
load_dotenv()

def verify_api_keys():
    """Verify that all required API keys are present in .env file."""
    required_keys = ['NEWS_API_KEY']
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        logger.error(f"Missing required API keys in .env file: {', '.join(missing_keys)}")
        return False
    return True

@lru_cache(maxsize=100)
def parse_gnews_date(date_str):
    """
    Parse GNews date string into a formatted date with caching.
    """
    if not date_str:
        return ''
        
    try:
        date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        return date_obj.strftime('%Y-%m-%d %H:%M')
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            return date_obj.strftime('%Y-%m-%d %H:%M')
        except ValueError:
            return ''

@lru_cache(maxsize=100)
def fetch_ipo_news(company_name):
    """
    Fetch IPO-related news articles from GNews API with caching.
    """
    try:
        logger.info(f"Fetching news for {company_name}")
        
        # Initialize GNews with optimized settings
        google_news = GNews(
            language='en',
            country='IN',
            period='3d',  # Reduced to 3 days
            max_results=5  # Reduced to 5 articles
        )
        
        # Optimized search query
        query = f"{company_name} IPO listing"
        articles = google_news.get_news(query)
        
        if not articles:
            logger.warning(f"No articles found for {company_name}")
            return []
            
        processed_articles = []
        seen_titles = set()
        
        for article in articles:
            if not article.get('title') or not article.get('description'):
                continue
                
            title = article.get('title', '').lower()
            if title in seen_titles:
                continue
            seen_titles.add(title)
            
            processed_articles.append({
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'date': parse_gnews_date(article.get('published date', '')),
                'url': article.get('url', ''),
                'source': article.get('publisher', {}).get('title', '')
            })
            
        return processed_articles
        
    except Exception as e:
        logger.error(f"Error in fetch_ipo_news: {str(e)}")
        return []

def analyze_sentiment(articles):
    """
    Analyze sentiment of news articles with optimized processing.
    """
    if not articles:
        return [], 0.0
        
    analyzed_articles = []
    total_sentiment = 0
    valid_articles = 0
    
    for article in articles:
        try:
            # Combine title and description for analysis
            text = f"{article['title']} {article['description']}"
            
            # Skip if text is too short
            if len(text.strip()) < 20:
                continue
                
            # Analyze sentiment
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity
            
            # Categorize sentiment
            if sentiment > 0.2:
                sentiment_category = "Positive"
            elif sentiment < -0.2:
                sentiment_category = "Negative"
            else:
                sentiment_category = "Neutral"
                
            analyzed_article = {
                **article,
                'sentiment_score': round(sentiment, 2),
                'sentiment': sentiment_category
            }
            analyzed_articles.append(analyzed_article)
            
            total_sentiment += sentiment
            valid_articles += 1
            
        except Exception as e:
            logger.error(f"Error analyzing article: {str(e)}")
            continue
    
    average_sentiment = round(total_sentiment / valid_articles, 2) if valid_articles > 0 else 0.0
    return analyzed_articles, average_sentiment

def get_news_sentiment(company_name):
    """
    Main function to get news sentiment with optimized performance.
    """
    try:
        start_time = time.time()
        
        # Fetch and analyze news
        articles = fetch_ipo_news(company_name)
        analyzed_articles, average_sentiment = analyze_sentiment(articles)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        logger.info(f"News analysis completed in {processing_time:.2f} seconds")
        
        return {
            'articles': analyzed_articles,
            'average_sentiment': average_sentiment,
            'processing_time': round(processing_time, 2)
        }
        
    except Exception as e:
        logger.error(f"Error in get_news_sentiment: {str(e)}")
        return {
            'articles': [],
            'average_sentiment': 0.0,
            'processing_time': 0.0
        }
