import React, { useState } from 'react';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Grid,
  Card,
  CardContent,
  Alert,
  CircularProgress,
} from '@mui/material';
import Plot from 'react-plotly.js';
import axios from 'axios';

const StockAnalysis = () => {
  const [formData, setFormData] = useState({
    ticker: '',
    startDate: '',
    endDate: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [analysisData, setAnalysisData] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // This would call your Python backend API
      const response = await axios.post('/api/analyze-stock', formData);
      setAnalysisData(response.data);
    } catch (err) {
      setError('Failed to analyze stock. Please check your inputs and try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Sample data for demonstration
  const sampleData = {
    ticker: 'AAPL',
    results: {
      initial_capital: 10000,
      final_capital: 11250,
      total_return_pct: 12.5,
      total_trades: 8,
      profitable_trades: 6,
      accuracy_pct: 75.0,
    },
    chartData: {
      x: ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
      y: [150, 152, 148, 155, 158],
      rsi: [65, 68, 45, 72, 75],
      bb_upper: [160, 162, 158, 165, 168],
      bb_lower: [140, 142, 138, 145, 148],
    },
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Stock Analysis
      </Typography>

      {/* Analysis Form */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Analyze Stock
        </Typography>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="Stock Ticker"
                name="ticker"
                value={formData.ticker}
                onChange={handleInputChange}
                placeholder="e.g., AAPL"
                required
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="Start Date"
                name="startDate"
                type="date"
                value={formData.startDate}
                onChange={handleInputChange}
                InputLabelProps={{ shrink: true }}
                required
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="End Date"
                name="endDate"
                type="date"
                value={formData.endDate}
                onChange={handleInputChange}
                InputLabelProps={{ shrink: true }}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                disabled={loading}
                sx={{ mt: 1 }}
              >
                {loading ? <CircularProgress size={24} /> : 'Analyze Stock'}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Analysis Results */}
      {analysisData && (
        <Grid container spacing={3}>
          {/* Performance Metrics */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Performance Metrics
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Initial Capital: ${sampleData.results.initial_capital.toLocaleString()}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Final Capital: ${sampleData.results.final_capital.toLocaleString()}
                </Typography>
                <Typography variant="h5" color="primary" sx={{ mt: 1 }}>
                  Total Return: {sampleData.results.total_return_pct}%
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Total Trades: {sampleData.results.total_trades}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Accuracy: {sampleData.results.accuracy_pct}%
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Technical Analysis Chart */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Technical Analysis - {sampleData.ticker}
              </Typography>
              <Plot
                data={[
                  {
                    x: sampleData.chartData.x,
                    y: sampleData.chartData.y,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: 'Price',
                    line: { color: '#2196f3' },
                  },
                  {
                    x: sampleData.chartData.x,
                    y: sampleData.chartData.bb_upper,
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Bollinger Upper',
                    line: { color: '#f50057', dash: 'dash' },
                  },
                  {
                    x: sampleData.chartData.x,
                    y: sampleData.chartData.bb_lower,
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Bollinger Lower',
                    line: { color: '#f50057', dash: 'dash' },
                    fill: 'tonexty',
                  },
                ]}
                layout={{
                  title: `${sampleData.ticker} Technical Analysis`,
                  xaxis: { title: 'Date' },
                  yaxis: { title: 'Price ($)' },
                  height: 400,
                  showlegend: true,
                }}
                config={{ displayModeBar: false }}
              />
            </Paper>
          </Grid>

          {/* RSI Chart */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                RSI Indicator
              </Typography>
              <Plot
                data={[
                  {
                    x: sampleData.chartData.x,
                    y: sampleData.chartData.rsi,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: 'RSI',
                    line: { color: '#9c27b0' },
                  },
                ]}
                layout={{
                  title: 'Relative Strength Index (RSI)',
                  xaxis: { title: 'Date' },
                  yaxis: { title: 'RSI', range: [0, 100] },
                  height: 300,
                  shapes: [
                    {
                      type: 'line',
                      x0: sampleData.chartData.x[0],
                      x1: sampleData.chartData.x[sampleData.chartData.x.length - 1],
                      y0: 70,
                      y1: 70,
                      line: { color: 'red', dash: 'dash' },
                    },
                    {
                      type: 'line',
                      x0: sampleData.chartData.x[0],
                      x1: sampleData.chartData.x[sampleData.chartData.x.length - 1],
                      y0: 30,
                      y1: 30,
                      line: { color: 'green', dash: 'dash' },
                    },
                  ],
                }}
                config={{ displayModeBar: false }}
              />
            </Paper>
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

export default StockAnalysis; 