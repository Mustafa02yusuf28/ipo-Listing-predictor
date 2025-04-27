import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  Alert,
  Divider
} from '@mui/material';

const ResultsDisplay = ({ prediction }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch('https://ipo-listing-predictor.onrender.com/api/prediction-history');
        const data = await response.json();
        
        if (!response.ok) {
          throw new Error(data.error || 'Failed to fetch prediction history');
        }
        
        setHistory(data.history || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const formatCurrency = (value) => {
    if (value === null || value === undefined) return '-';
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 2
    }).format(value);
  };

  const formatPercentage = (value) => {
    if (value === null || value === undefined) return '-';
    return `${value.toFixed(2)}%`;
  };

  const calculateAccuracy = (predicted, actual) => {
    if (!predicted || !actual) return null;
    const diff = Math.abs(predicted - actual);
    const accuracy = 100 - (diff / actual * 100);
    return accuracy;
  };

  const calculateReturn = (issue, actual) => {
    if (!issue || !actual) return null;
    return ((actual - issue) / issue) * 100;
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Prediction Results
        </Typography>
        
        <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 2 }}>
          <Box>
            <Typography variant="subtitle2" color="text.secondary">
              Predicted Listing Price
            </Typography>
            <Typography variant="h4" color="primary">
              {formatCurrency(prediction.predicted_price)}
            </Typography>
          </Box>
          
          <Box>
            <Typography variant="subtitle2" color="text.secondary">
              Expected Return
            </Typography>
            <Typography 
              variant="h4" 
              color={prediction.expected_return >= 0 ? 'success.main' : 'error.main'}
            >
              {formatPercentage(prediction.expected_return)}
            </Typography>
          </Box>
        </Box>

        <Divider sx={{ my: 3 }} />

        <Typography variant="subtitle1" gutterBottom>
          Sentiment Analysis
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Sentiment Score: {prediction.sentiment_score?.toFixed(2) || 'N/A'}
        </Typography>
      </Paper>

      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Prediction History
        </Typography>

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Alert severity="error">{error}</Alert>
        ) : (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Company</TableCell>
                  <TableCell align="right">Issue Price</TableCell>
                  <TableCell align="right">Predicted Price</TableCell>
                  <TableCell align="right">Actual Price</TableCell>
                  <TableCell align="right">Return</TableCell>
                  <TableCell align="right">Accuracy</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {history.map((row, index) => {
                  const accuracy = calculateAccuracy(row.predicted_price, row.actual_price);
                  const returnPct = calculateReturn(row.issue_price, row.actual_price);
                  
                  return (
                    <TableRow key={index}>
                      <TableCell>{row.company_name}</TableCell>
                      <TableCell align="right">{formatCurrency(row.issue_price)}</TableCell>
                      <TableCell align="right">{formatCurrency(row.predicted_price)}</TableCell>
                      <TableCell align="right">
                        {row.actual_price ? formatCurrency(row.actual_price) : '-'}
                      </TableCell>
                      <TableCell align="right">
                        {returnPct !== null ? formatPercentage(returnPct) : '-'}
                      </TableCell>
                      <TableCell align="right">
                        {accuracy !== null ? formatPercentage(accuracy) : '-'}
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>
    </Box>
  );
};

export default ResultsDisplay; 