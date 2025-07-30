import React, { useState } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Paper,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
} from '@mui/material';
import Plot from 'react-plotly.js';
import axios from 'axios';

const BatchAnalysis = () => {
  const [analysisType, setAnalysisType] = useState('sp500');
  const [customTickers, setCustomTickers] = useState('');
  const [dateRange, setDateRange] = useState({
    startDate: '',
    endDate: '',
  });
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!dateRange.startDate || !dateRange.endDate) {
      setError('Please select both start and end dates');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post('/api/batch-analysis', {
        analysisType,
        customTickers,
        startDate: dateRange.startDate,
        endDate: dateRange.endDate,
      });
      
      setResults(response.data);
    } catch (err) {
      setError('Failed to perform batch analysis. Please try again.');
      console.error('Batch analysis error:', err);
      
      // Fallback to sample data if API fails
      setResults({
        totalStocks: 500,
        analyzedStocks: 487,
        averageReturn: 8.5,
        averageAccuracy: 76.2,
        bestPerformer: 'NVDA',
        worstPerformer: 'META',
        results: [
          { ticker: 'NVDA', total_return: 45.2, accuracy: 82.1, total_trades: 12 },
          { ticker: 'TSLA', total_return: 32.8, accuracy: 78.5, total_trades: 10 },
          { ticker: 'AAPL', total_return: 28.4, accuracy: 75.2, total_trades: 8 },
          { ticker: 'MSFT', total_return: 25.1, accuracy: 73.8, total_trades: 9 },
          { ticker: 'GOOGL', total_return: 22.7, accuracy: 71.4, total_trades: 11 },
        ],
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Batch Analysis
      </Typography>

      {/* Analysis Configuration */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Analysis Configuration
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Analysis Type</InputLabel>
              <Select
                value={analysisType}
                label="Analysis Type"
                onChange={(e) => setAnalysisType(e.target.value)}
              >
                <MenuItem value="sp500">S&P 500 Stocks</MenuItem>
                <MenuItem value="custom">Custom Tickers</MenuItem>
                <MenuItem value="nasdaq">NASDAQ 100</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Start Date"
              type="date"
              value={dateRange.startDate}
              onChange={(e) => setDateRange({ ...dateRange, startDate: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="End Date"
              type="date"
              value={dateRange.endDate}
              onChange={(e) => setDateRange({ ...dateRange, endDate: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          {analysisType === 'custom' && (
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Custom Tickers (comma-separated)"
                value={customTickers}
                onChange={(e) => setCustomTickers(e.target.value)}
                placeholder="AAPL,MSFT,GOOGL,TSLA"
                helperText="Enter stock tickers separated by commas"
              />
            </Grid>
          )}
          <Grid item xs={12}>
            <Button
              variant="contained"
              onClick={handleAnalyze}
              disabled={loading}
              size="large"
            >
              {loading ? <CircularProgress size={24} /> : 'Start Batch Analysis'}
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Results */}
      {results && (
        <Grid container spacing={3}>
          {/* Summary Cards */}
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Analyzed Stocks
                </Typography>
                <Typography variant="h4" component="div">
                  {results.analyzed_stocks || results.analyzedStocks}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  of {results.total_stocks || results.totalStocks} total
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Average Return
                </Typography>
                <Typography variant="h4" component="div" color="primary">
                  {(results.average_return || results.averageReturn)?.toFixed(1)}%
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Average Accuracy
                </Typography>
                <Typography variant="h4" component="div" color="success.main">
                  {(results.average_accuracy || results.averageAccuracy)?.toFixed(1)}%
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Best Performer
                </Typography>
                <Typography variant="h4" component="div">
                  {results.best_performer || results.bestPerformer}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Top Performers Table */}
          {results.results && results.results.length > 0 && (
            <Grid item xs={12}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Top Performers
                </Typography>
                <Grid container spacing={2}>
                  {results.results.slice(0, 10).map((performer, index) => (
                    <Grid item xs={12} sm={6} md={4} lg={2} key={index}>
                      <Card>
                        <CardContent sx={{ textAlign: 'center' }}>
                          <Typography variant="h6" component="div">
                            {performer.ticker}
                          </Typography>
                          <Typography variant="h5" color="primary">
                            {performer.total_return?.toFixed(1)}%
                          </Typography>
                          <Typography variant="body2" color="textSecondary">
                            {performer.accuracy?.toFixed(1)}% accuracy
                          </Typography>
                          <Typography variant="body2" color="textSecondary">
                            {performer.total_trades} trades
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </Paper>
            </Grid>
          )}
        </Grid>
      )}

      {loading && (
        <Alert severity="info" sx={{ mt: 2 }}>
          Analyzing stocks... This may take a few minutes for large datasets.
        </Alert>
      )}
      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
};

export default BatchAnalysis; 