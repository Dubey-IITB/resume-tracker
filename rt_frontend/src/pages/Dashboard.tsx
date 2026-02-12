import { useState, useEffect } from 'react'
import { Grid, Paper, Typography, Box, CircularProgress } from '@mui/material'
import {
  People as PeopleIcon,
  Work as WorkIcon,
  TrendingUp as TrendingIcon,
} from '@mui/icons-material'
import { useAuth } from '../contexts/AuthContext'
import { candidatesApi, jobsApi } from '../services/api'

interface DashboardStats {
  totalCandidates: number
  totalJobs: number
  activeJobs: number
}

export default function Dashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [candidates, jobs] = await Promise.all([
          candidatesApi.getAll(),
          jobsApi.getAll(),
        ])
        setStats({
          totalCandidates: candidates.length,
          totalJobs: jobs.length,
          activeJobs: jobs.filter((j) => j.status === 'active').length,
        })
      } catch (err) {
        console.error('Error fetching dashboard stats:', err)
        setStats({ totalCandidates: 0, totalJobs: 0, activeJobs: 0 })
      } finally {
        setLoading(false)
      }
    }
    fetchStats()
  }, [])

  const statCards = [
    {
      label: 'Total Candidates',
      value: stats?.totalCandidates ?? '–',
      icon: <PeopleIcon sx={{ fontSize: 40, color: '#667eea' }} />,
      bg: 'linear-gradient(135deg, #667eea22, #764ba222)',
    },
    {
      label: 'Total Jobs',
      value: stats?.totalJobs ?? '–',
      icon: <WorkIcon sx={{ fontSize: 40, color: '#f093fb' }} />,
      bg: 'linear-gradient(135deg, #f093fb22, #f5576c22)',
    },
    {
      label: 'Active Jobs',
      value: stats?.activeJobs ?? '–',
      icon: <TrendingIcon sx={{ fontSize: 40, color: '#4facfe' }} />,
      bg: 'linear-gradient(135deg, #4facfe22, #00f2fe22)',
    },
  ]

  return (
    <Box>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Welcome, {user?.full_name || 'User'}!
      </Typography>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 6 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {statCards.map((card) => (
            <Grid item xs={12} sm={6} md={4} key={card.label}>
              <Paper
                sx={{
                  p: 3,
                  borderRadius: 2,
                  background: card.bg,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 2,
                  boxShadow: 2,
                  transition: 'box-shadow 0.2s',
                  '&:hover': { boxShadow: 4 },
                }}
              >
                {card.icon}
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 700 }}>
                    {card.value}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {card.label}
                  </Typography>
                </Box>
              </Paper>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  )
}