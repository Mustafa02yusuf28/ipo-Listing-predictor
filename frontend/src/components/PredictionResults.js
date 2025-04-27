import React from 'react';
import { Box, Paper, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginTop: theme.spacing(2),
  backgroundColor: theme.palette.background.paper,
}));

const PredictionResults = ({ prediction }) => {
  if (!prediction) return null;

  const {
    predicted_price,
    expected_return
  } = prediction;

  return (
    <StyledPaper elevation={3}>
      <Typography variant="h5" gutterBottom>
        Prediction Results
      </Typography>

      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" color="primary">
          Predicted Listing Price: ₹{predicted_price}
        </Typography>
        <Typography 
          variant="subtitle1" 
          color={expected_return >= 0 ? 'success.main' : 'error.main'}
        >
          Expected Return: {expected_return}%
        </Typography>
      </Box>
    </StyledPaper>
  );
};

export default PredictionResults; 