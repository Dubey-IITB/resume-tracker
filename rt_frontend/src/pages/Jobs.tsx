import { useState, useEffect } from 'react'
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
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  IconButton,
  Tooltip,
  MenuItem,
} from '@mui/material'
import {
  Add as AddIcon,
  Refresh as RefreshIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material'
import { jobsApi } from '../services/api'
import { Job, JobCreate } from '../types'

export default function Jobs() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Create job dialog state
  const [dialogOpen, setDialogOpen] = useState(false)
  const [saving, setSaving] = useState(false)
  const [formTitle, setFormTitle] = useState('')
  const [formDesc, setFormDesc] = useState('')
  const [formMinBudget, setFormMinBudget] = useState('')
  const [formMaxBudget, setFormMaxBudget] = useState('')
  const [formStatus, setFormStatus] = useState('active')

  const fetchJobs = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await jobsApi.getAll()
      setJobs(data)
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to fetch jobs'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchJobs()
  }, [])

  const handleCreate = async () => {
    setSaving(true)
    try {
      const payload: JobCreate = {
        title: formTitle,
        description: formDesc || undefined,
        min_budget: formMinBudget ? parseFloat(formMinBudget) : undefined,
        max_budget: formMaxBudget ? parseFloat(formMaxBudget) : undefined,
        status: formStatus,
      }
      await jobsApi.create(payload)
      setDialogOpen(false)
      resetForm()
      fetchJobs()
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to create job'
      setError(msg)
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (id: number) => {
    try {
      await jobsApi.delete(id)
      fetchJobs()
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to delete job'
      setError(msg)
    }
  }

  const resetForm = () => {
    setFormTitle('')
    setFormDesc('')
    setFormMinBudget('')
    setFormMaxBudget('')
    setFormStatus('active')
  }

  const formatDate = (dateStr: string) =>
    new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })

  const formatCurrency = (amount: number) =>
    new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(amount)

  const statusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success'
      case 'closed': return 'error'
      case 'draft': return 'warning'
      default: return 'default'
    }
  }

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600 }}>
          Jobs
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Tooltip title="Refresh">
            <IconButton onClick={fetchJobs} color="primary">
              <RefreshIcon />
            </IconButton>
          </Tooltip>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setDialogOpen(true)}
            sx={{
              background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
              boxShadow: '0 3px 5px 2px rgba(102, 126, 234, .3)',
            }}
          >
            Post Job
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {jobs.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No jobs posted yet
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Create your first job posting to start matching candidates.
          </Typography>
          <Button variant="outlined" startIcon={<AddIcon />} onClick={() => setDialogOpen(true)}>
            Post Job
          </Button>
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {jobs.map((job) => (
            <Grid item xs={12} md={6} key={job.id}>
              <Card sx={{ borderRadius: 2, boxShadow: 2, transition: 'box-shadow 0.2s', '&:hover': { boxShadow: 4 } }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                      {job.title}
                    </Typography>
                    <Chip
                      label={job.status}
                      size="small"
                      color={statusColor(job.status) as any}
                    />
                  </Box>
                  {job.description && (
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1.5, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                      {job.description}
                    </Typography>
                  )}
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 1 }}>
                    {job.min_budget != null && (
                      <Chip label={`Min: ${formatCurrency(job.min_budget)}`} size="small" variant="outlined" />
                    )}
                    {job.max_budget != null && (
                      <Chip label={`Max: ${formatCurrency(job.max_budget)}`} size="small" variant="outlined" color="primary" />
                    )}
                  </Box>
                  <Typography variant="caption" color="text.secondary">
                    Posted {job.created_at ? formatDate(job.created_at) : 'N/A'}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Tooltip title="Delete">
                    <IconButton size="small" color="error" onClick={() => handleDelete(job.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </Tooltip>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Create Job Dialog */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ fontWeight: 600 }}>Post New Job</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 1, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Job Title"
              fullWidth
              required
              value={formTitle}
              onChange={(e) => setFormTitle(e.target.value)}
            />
            <TextField
              label="Description"
              fullWidth
              multiline
              rows={3}
              value={formDesc}
              onChange={(e) => setFormDesc(e.target.value)}
            />
            <Box sx={{ display: 'flex', gap: 2 }}>
              <TextField
                label="Min Budget (INR)"
                type="number"
                fullWidth
                value={formMinBudget}
                onChange={(e) => setFormMinBudget(e.target.value)}
              />
              <TextField
                label="Max Budget (INR)"
                type="number"
                fullWidth
                value={formMaxBudget}
                onChange={(e) => setFormMaxBudget(e.target.value)}
              />
            </Box>
            <TextField
              label="Status"
              select
              fullWidth
              value={formStatus}
              onChange={(e) => setFormStatus(e.target.value)}
            >
              <MenuItem value="active">Active</MenuItem>
              <MenuItem value="draft">Draft</MenuItem>
              <MenuItem value="closed">Closed</MenuItem>
            </TextField>
          </Box>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setDialogOpen(false)} disabled={saving}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleCreate}
            disabled={saving || !formTitle.trim()}
            startIcon={saving ? <CircularProgress size={20} /> : <AddIcon />}
          >
            {saving ? 'Creating...' : 'Create Job'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}