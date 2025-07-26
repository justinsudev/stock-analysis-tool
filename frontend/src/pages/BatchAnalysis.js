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

const BatchAnalysis = () => {
  const [analysisType, setAnalysisType] = useState('sp500');
  const [customTickers, setCustomTickers] = useState('');
  const [dateRange, setDateRange] = useState({
    startDate: '',
    endDate: '',
  });
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleAnalyze = async () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setResults({
        totalStocks: 500,
        analyzedStocks: 487,
        averageReturn: 8.5,
        averageAccuracy: 76.2,
        bestPerformer: 'NVDA',
        worstPerformer: 'META',
        returnsDistribution: [5, 15, 25, 35, 20],
        accuracyDistribution: [10, 20, 30, 25, 15],
        topPerformers: [
          { ticker: 'NVDA', return: 45.2, accuracy: 82.1 },
          { ticker: 'TSLA', return: 32.8, accuracy: 78.5 },
          { ticker: 'AAPL', return: 28.4, accuracy: 75.2 },
          { ticker: 'MSFT', return: 25.1, accuracy: 73.8 },
          { ticker: 'GOOGL', return: 22.7, accuracy: 71.4 },
        ],
      });
      setLoading(false);
    }, 2000);
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
                  {results.analyzedStocks}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  of {results.totalStocks} total
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
                  {results.averageReturn}%
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
                  {results.averageAccuracy}%
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
                  {results.bestPerformer}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Returns Distribution Chart */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Returns Distribution
              </Typography>
              <Plot
                data={[
                  {
                    x: ['-20% to -10%', '-10% to 0%', '0% to 10%', '10% to 20%', '20%+'],
                    y: results.returnsDistribution,
                    type: 'bar',
                    marker: { color: '#2196f3' },
                  },
                ]}
                layout={{
                  title: 'Distribution of Returns',
                  xaxis: { title: 'Return Range' },
                  yaxis: { title: 'Number of Stocks' },
                  height: 300,
                }}
                config={{ displayModeBar: false }}
              />
            </Paper>
          </Grid>

          {/* Accuracy vs Returns Scatter */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Top Performers
              </Typography>
              <Plot
                data={[
                  {
                    x: results.topPerformers.map(p => p.accuracy),
                    y: results.topPerformers.map(p => p.return),
                    mode: 'markers+text',
                    type: 'scatter',
                    text: results.topPerformers.map(p => p.ticker),
                    textposition: 'top center',
                    marker: { 
                      size: 12,
                      color: results.topPerformers.map(p => p.return),
                      colorscale: 'Viridis',
                    },
                  },
                ]}
                layout={{
                  title: 'Accuracy vs Returns',
                  xaxis: { title: 'Accuracy (%)' },
                  yaxis: { title: 'Return (%)' },
                  height: 300,
                }}
                config={{ displayModeBar: false }}
              />
            </Paper>
          </Grid>

          {/* Top Performers Table */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Top 10 Performers
              </Typography>
              <Grid container spacing={2}>
                {results.topPerformers.map((performer, index) => (
                  <Grid item xs={12} sm={6} md={4} lg={2} key={index}>
                    <Card>
                      <CardContent sx={{ textAlign: 'center' }}>
                        <Typography variant="h6" component="div">
                          {performer.ticker}
                        </Typography>
                        <Typography variant="h5" color="primary">
                          {performer.return}%
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          {performer.accuracy}% accuracy
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Paper>
          </Grid>
        </Grid>
      )}

      {loading && (
        <Alert severity="info" sx={{ mt: 2 }}>
          Analyzing stocks... This may take a few minutes for large datasets.
        </Alert>
      )}
    </Box>
  );
};

export default BatchAnalysis; 