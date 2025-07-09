import { useState } from 'react'
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
} from '@mui/material'
import { Add as AddIcon } from '@mui/icons-material'

interface Job {
  id: string
  title: string
  company: string
  location: string
  type: string
  status: 'Open' | 'Closed'
  postedDate: string
}

const mockJobs: Job[] = [
  {
    id: '1',
    title: 'Senior Software Engineer',
    company: 'Tech Corp',
    location: 'San Francisco, CA',
    type: 'Full-time',
    status: 'Open',
    postedDate: '2024-02-20',
  },
  {
    id: '2',
    title: 'Frontend Developer',
    company: 'Web Solutions',
    location: 'Remote',
    type: 'Contract',
    status: 'Open',
    postedDate: '2024-02-19',
  },
]

export default function Jobs() {
  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h4">Jobs</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {/* TODO: Implement add job */}}
        >
          Post Job
        </Button>
      </Box>
      <Grid container spacing={3}>
        {mockJobs.map((job) => (
          <Grid item xs={12} md={6} key={job.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {job.title}
                </Typography>
                <Typography color="text.secondary" gutterBottom>
                  {job.company} • {job.location}
                </Typography>
                <Box sx={{ mt: 1, mb: 1 }}>
                  <Chip
                    label={job.type}
                    size="small"
                    sx={{ mr: 1 }}
                  />
                  <Chip
                    label={job.status}
                    size="small"
                    color={job.status === 'Open' ? 'success' : 'default'}
                  />
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Posted on {job.postedDate}
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small">View Details</Button>
                <Button size="small">Edit</Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  )
} 