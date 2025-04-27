# IPO Listing Price Predictor

A machine learning-based web application that predicts the listing price of Initial Public Offerings (IPOs) in the Indian stock market.

## Overview

This project helps investors and traders predict the potential listing price of upcoming IPOs by analyzing various financial metrics and market indicators. The prediction model considers multiple factors including:

- Grey Market Premium (GMP)
- Market Capitalization
- Return on Capital Employed (ROCE)
- Return on Equity (ROE)
- Industry Growth Rate

## Features

- **Real-time Predictions**: Get instant predictions for upcoming IPOs
- **Financial Analysis**: Comprehensive analysis of company financials
- **User-friendly Interface**: Simple and intuitive web interface
- **Historical Data**: Track and analyze past predictions
- **Accuracy Tracking**: Monitor the accuracy of predictions over time

## Technical Stack

### Backend
- Python 3.8+
- Flask (Web Framework)
- scikit-learn (Machine Learning)
- pandas (Data Analysis)
- numpy (Numerical Computing)

### Frontend
- React.js
- Material-UI
- Axios (API Calls)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ipo-predictor.git
cd ipo-predictor
```

2. Install backend dependencies:
```bash
cd app
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

## Running the Application

1. Start the backend server:
```bash
cd app
python api.py
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

The application will be available at `http://localhost:3000`

## Usage

1. Enter the IPO details:
   - Company Name
   - Issue Price
   - Market Capitalization
   - Grey Market Premium
   - ROCE
   - ROE
   - Industry Growth Rate

2. Click "Predict" to get the listing price prediction

3. View the results:
   - Predicted Listing Price
   - Expected Return

## Prediction Model

The prediction model uses a weighted scoring system based on historical IPO data:

- GMP Contribution: 60%
- Market Cap Contribution: 20%
- ROCE Contribution: 10%
- ROE Contribution: 5%
- Industry Growth Contribution: 5%

Additional factors:
- Small Cap Bonus: 10% bonus for companies with market cap < 500 Cr
- Negative Value Protection: Caps negative contributions at -50%

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and informational purposes only. The predictions are based on historical data and current market conditions, and should not be considered as financial advice. Always do your own research before making investment decisions.