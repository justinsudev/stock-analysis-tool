import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Paper,
  Chip,
  LinearProgress,
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import SpeedIcon from '@mui/icons-material/Speed';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalStocks: 5000,
    analyzedStocks: 0,
    averageAccuracy: 0,
    averageReturn: 0,
  });

  useEffect(() => {
    // Simulate loading stats
    setTimeout(() => {
      setStats({
        totalStocks: 5000,
        analyzedStocks: 3247,
        averageAccuracy: 78.5,
        averageReturn: 12.3,
      });
    }, 1000);
  }, []);

  const features = [
    {
      title: 'Real-time Analysis',
      description: 'Analyze over 5,000 equities with technical indicators',
      icon: <TrendingUpIcon sx={{ fontSize: 40 }} />,
      color: '#2196f3',
    },
    {
      title: 'Technical Indicators',
      description: 'RSI, Bollinger Bands, and Moving Averages',
      icon: <AnalyticsIcon sx={{ fontSize: 40 }} />,
      color: '#f50057',
    },
    {
      title: 'Portfolio Tracking',
      description: 'Track trades and portfolio performance',
      icon: <AccountBalanceIcon sx={{ fontSize: 40 }} />,
      color: '#4caf50',
    },
    {
      title: '80% Accuracy',
      description: 'Backtested algorithmic trading signals',
      icon: <SpeedIcon sx={{ fontSize: 40 }} />,
      color: '#ff9800',
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
        Stock Analysis Dashboard
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Stocks
              </Typography>
              <Typography variant="h4" component="div">
                {stats.totalStocks.toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Analyzed Stocks
              </Typography>
              <Typography variant="h4" component="div">
                {stats.analyzedStocks.toLocaleString()}
              </Typography>
              <LinearProgress
                variant="determinate"
                value={(stats.analyzedStocks / stats.totalStocks) * 100}
                sx={{ mt: 1 }}
              />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Average Accuracy
              </Typography>
              <Typography variant="h4" component="div">
                {stats.averageAccuracy}%
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
              <Typography variant="h4" component="div">
                {stats.averageReturn}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Features Grid */}
      <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
        Key Features
      </Typography>
      <Grid container spacing={3}>
        {features.map((feature, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Paper
              sx={{
                p: 3,
                textAlign: 'center',
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                border: `2px solid ${feature.color}`,
                '&:hover': {
                  transform: 'translateY(-4px)',
                  transition: 'transform 0.3s ease-in-out',
                },
              }}
            >
              <Box sx={{ color: feature.color, mb: 2 }}>
                {feature.icon}
              </Box>
              <Typography variant="h6" gutterBottom>
                {feature.title}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {feature.description}
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>

      {/* Quick Actions */}
      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          Quick Actions
        </Typography>
        <Grid container spacing={2}>
          <Grid item>
            <Chip
              label="Analyze Single Stock"
              color="primary"
              variant="outlined"
              clickable
            />
          </Grid>
          <Grid item>
            <Chip
              label="Batch Analysis"
              color="secondary"
              variant="outlined"
              clickable
            />
          </Grid>
          <Grid item>
            <Chip
              label="View Portfolio"
              color="success"
              variant="outlined"
              clickable
            />
          </Grid>
          <Grid item>
            <Chip
              label="Technical Indicators"
              color="warning"
              variant="outlined"
              clickable
            />
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
};

export default Dashboard; 