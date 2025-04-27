import React, { useState } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  CssBaseline, 
  ThemeProvider, 
  createTheme,
  AppBar,
  Toolbar,
  Paper,
  Tabs,
  Tab
} from '@mui/material';
import PredictorForm from './components/PredictorForm';
import ResultsDisplay from './components/ResultsDisplay';
import UpdateActualPrice from './components/UpdateActualPrice';

// Create a custom theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#f50057',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
  },
});

function App() {
  const [prediction, setPrediction] = useState(null);
  const [activeTab, setActiveTab] = useState(0);

  const handlePredictionComplete = (result) => {
    setPrediction(result);
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1, minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        <AppBar position="static" elevation={0}>
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              IPO Listing Price Predictor
            </Typography>
          </Toolbar>
        </AppBar>
        
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
          <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
            <Typography variant="h4" gutterBottom>
              Predict IPO Listing Price
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              Enter the IPO details below to predict the listing price and expected return.
              Our model uses historical data, market sentiment, and financial metrics to provide accurate predictions.
            </Typography>
            
            <Tabs 
              value={activeTab} 
              onChange={handleTabChange} 
              sx={{ mb: 3 }}
              indicatorColor="primary"
              textColor="primary"
            >
              <Tab label="Predict" />
              <Tab label="Update Actual Price" />
            </Tabs>
            
            {activeTab === 0 ? (
              <PredictorForm onPredictionComplete={handlePredictionComplete} />
            ) : (
              <UpdateActualPrice />
            )}
          </Paper>
          
          {prediction && activeTab === 0 && <ResultsDisplay prediction={prediction} />}
        </Container>
        
        <Box component="footer" sx={{ py: 3, bgcolor: 'background.paper' }}>
          <Container maxWidth="lg">
            <Typography variant="body2" color="text.secondary" align="center">
              © {new Date().getFullYear()} IPO Listing Price Predictor. All rights reserved.
            </Typography>
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App; 