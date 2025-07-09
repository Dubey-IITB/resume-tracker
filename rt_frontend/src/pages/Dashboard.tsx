import { Grid, Paper, Typography } from '@mui/material'
import { useAuth } from '../contexts/AuthContext'

export default function Dashboard() {
  const { user } = useAuth()

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h4" gutterBottom>
            Welcome, {user?.name}!
          </Typography>
          <Typography variant="body1">
            This is your dashboard. Here you can see an overview of your resume tracking activities.
          </Typography>
        </Paper>
      </Grid>
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Recent Applications
          </Typography>
          <Typography variant="body2" color="text.secondary">
            No recent applications to show.
          </Typography>
        </Paper>
      </Grid>
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Upcoming Interviews
          </Typography>
          <Typography variant="body2" color="text.secondary">
            No upcoming interviews scheduled.
          </Typography>
        </Paper>
      </Grid>
    </Grid>
  )
} 