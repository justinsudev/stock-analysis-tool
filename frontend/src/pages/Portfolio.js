import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
} from '@mui/material';
import Plot from 'react-plotly.js';

const Portfolio = () => {
  const [portfolioData, setPortfolioData] = useState(null);

  useEffect(() => {
    // Simulate loading portfolio data
    setPortfolioData({
      name: 'AAPL Portfolio',
      initialCapital: 10000,
      currentValue: 11250,
      totalReturn: 12.5,
      cash: 2500,
      positions: [
        {
          ticker: 'AAPL',
          shares: 50,
          avgPrice: 150,
          currentPrice: 175,
          marketValue: 8750,
          unrealizedPnl: 1250,
          unrealizedPnlPct: 16.67,
        },
        {
          ticker: 'MSFT',
          shares: 25,
          avgPrice: 280,
          currentPrice: 300,
          marketValue: 7500,
          unrealizedPnl: 500,
          unrealizedPnlPct: 7.14,
        },
      ],
      trades: [
        {
          date: '2024-01-15',
          ticker: 'AAPL',
          action: 'Buy',
          shares: 50,
          price: 150,
          value: 7500,
        },
        {
          date: '2024-01-20',
          ticker: 'MSFT',
          action: 'Buy',
          shares: 25,
          price: 280,
          value: 7000,
        },
        {
          date: '2024-01-25',
          ticker: 'AAPL',
          action: 'Sell',
          shares: 10,
          price: 170,
          value: 1700,
        },
      ],
      performanceData: {
        dates: ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
        values: [10000, 10100, 10250, 10800, 11250],
      },
    });
  }, []);

  if (!portfolioData) {
    return <Typography>Loading portfolio data...</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Portfolio Management
      </Typography>

      {/* Portfolio Summary */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Portfolio Value
              </Typography>
              <Typography variant="h4" component="div">
                ${portfolioData.currentValue.toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Return
              </Typography>
              <Typography variant="h4" component="div" color="primary">
                {portfolioData.totalReturn}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Cash
              </Typography>
              <Typography variant="h4" component="div">
                ${portfolioData.cash.toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Positions
              </Typography>
              <Typography variant="h4" component="div">
                {portfolioData.positions.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Portfolio Performance Chart */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Portfolio Performance
            </Typography>
            <Plot
              data={[
                {
                  x: portfolioData.performanceData.dates,
                  y: portfolioData.performanceData.values,
                  type: 'scatter',
                  mode: 'lines+markers',
                  name: 'Portfolio Value',
                  line: { color: '#2196f3' },
                },
              ]}
              layout={{
                title: 'Portfolio Value Over Time',
                xaxis: { title: 'Date' },
                yaxis: { title: 'Value ($)' },
                height: 400,
                showlegend: false,
              }}
              config={{ displayModeBar: false }}
            />
          </Paper>
        </Grid>

        {/* Current Positions */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Current Positions
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Ticker</TableCell>
                    <TableCell>Shares</TableCell>
                    <TableCell>Value</TableCell>
                    <TableCell>P&L</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {portfolioData.positions.map((position) => (
                    <TableRow key={position.ticker}>
                      <TableCell>{position.ticker}</TableCell>
                      <TableCell>{position.shares}</TableCell>
                      <TableCell>${position.marketValue.toLocaleString()}</TableCell>
                      <TableCell>
                        <Chip
                          label={`${position.unrealizedPnlPct > 0 ? '+' : ''}${position.unrealizedPnlPct}%`}
                          color={position.unrealizedPnlPct > 0 ? 'success' : 'error'}
                          size="small"
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>

        {/* Trade History */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Trade History
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Date</TableCell>
                    <TableCell>Ticker</TableCell>
                    <TableCell>Action</TableCell>
                    <TableCell>Shares</TableCell>
                    <TableCell>Price</TableCell>
                    <TableCell>Value</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {portfolioData.trades.map((trade, index) => (
                    <TableRow key={index}>
                      <TableCell>{trade.date}</TableCell>
                      <TableCell>{trade.ticker}</TableCell>
                      <TableCell>
                        <Chip
                          label={trade.action}
                          color={trade.action === 'Buy' ? 'success' : 'error'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{trade.shares}</TableCell>
                      <TableCell>${trade.price}</TableCell>
                      <TableCell>${trade.value.toLocaleString()}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Portfolio; 