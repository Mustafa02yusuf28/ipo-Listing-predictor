import React, { useState } from 'react';
import {
  TextField,
  Button,
  Typography,
  Box,
  Paper,
  Grid,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Link,
  Chip
} from '@mui/material';

const PredictorForm = () => {
  const [formData, setFormData] = useState({
    company_name: '',
    issue_price: '',
    market_cap: '',
    gmp: '',
    roce: '',
    roe: '',
    industry_growth: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [prediction, setPrediction] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPrediction(null);

    try {
      // Parse numeric values
      const numericData = {
        ...formData,
        issue_price: parseFloat(formData.issue_price),
        market_cap: parseFloat(formData.market_cap),
        gmp: parseFloat(formData.gmp),
        roce: parseFloat(formData.roce),
        roe: parseFloat(formData.roe),
        industry_growth: parseFloat(formData.industry_growth)
      };

      const response = await fetch('https://ipo-listing-predictor.onrender.com/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(numericData),
      });

      if (!response.ok) {
        throw new Error('Failed to get prediction');
      }

      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      setError(err.message || 'An error occurred while making the prediction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Predict IPO Listing Price
        </Typography>
        <Typography variant="body1" paragraph>
          Enter the IPO details below to predict the listing price and expected return. 
          Our model uses historical data, market sentiment, and financial metrics to provide accurate predictions.
        </Typography>

        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Company Name"
                name="company_name"
                value={formData.company_name}
                onChange={handleChange}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Issue Price (₹)"
                name="issue_price"
                type="number"
                value={formData.issue_price}
                onChange={handleChange}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Market Cap (Cr)"
                name="market_cap"
                type="number"
                value={formData.market_cap}
                onChange={handleChange}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Grey Market Premium (₹)"
                name="gmp"
                type="number"
                value={formData.gmp}
                onChange={handleChange}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="ROCE (%)"
                name="roce"
                type="number"
                value={formData.roce}
                onChange={handleChange}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="ROE (%)"
                name="roe"
                type="number"
                value={formData.roe}
                onChange={handleChange}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Industry Growth Rate (%)"
                name="industry_growth"
                type="number"
                value={formData.industry_growth}
                onChange={handleChange}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Predict'}
              </Button>
            </Grid>
          </Grid>
        </form>

        {error && (
          <Typography color="error" sx={{ mt: 2 }}>
            {error}
          </Typography>
        )}

        {prediction && (
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Prediction Results
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Paper elevation={2} sx={{ p: 2 }}>
                  <Typography variant="subtitle1">Predicted Listing Price</Typography>
                  <Typography variant="h5">
                    ₹{typeof prediction.predicted_price === 'number' ? prediction.predicted_price.toFixed(2) : '0.00'}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Paper elevation={2} sx={{ p: 2 }}>
                  <Typography variant="subtitle1">Expected Return</Typography>
                  <Typography 
                    variant="h5" 
                    color={prediction.expected_return >= 0 ? 'success.main' : 'error.main'}
                  >
                    {typeof prediction.expected_return === 'number' ? prediction.expected_return.toFixed(2) : '0.00'}%
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default PredictorForm; 