import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import axios from 'axios';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get('http://localhost:8000/dashboard/stats/');
      setStats(response.data);
    } catch (error) {
      setError('Failed to fetch dashboard statistics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Summary Cards */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h6" gutterBottom>
              Total Scans
            </Typography>
            <Typography variant="h3">
              {stats?.total_scans || 0}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h6" gutterBottom>
              Vulnerabilities Found
            </Typography>
            <Typography variant="h3" color="error">
              {stats?.total_vulnerabilities || 0}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h6" gutterBottom>
              Active Scans
            </Typography>
            <Typography variant="h3" color="primary">
              {stats?.active_scans || 0}
            </Typography>
          </Paper>
        </Grid>

        {/* Scan Types Chart */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Scan Types Distribution
            </Typography>
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={stats?.scan_types || []}
                  margin={{
                    top: 20,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="count" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Activity
            </Typography>
            {stats?.recent_activity?.map((activity, index) => (
              <Box key={index} sx={{ mb: 2 }}>
                <Typography variant="body1">
                  {activity.description}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {new Date(activity.timestamp).toLocaleString()}
                </Typography>
              </Box>
            ))}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Dashboard; 