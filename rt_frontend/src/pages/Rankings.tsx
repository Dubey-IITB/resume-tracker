import { useState, useEffect } from 'react'
import {
    Box,
    Typography,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Button,
    Chip,
    CircularProgress,
    Alert,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    IconButton,
    Tooltip,
    LinearProgress,
    Collapse,
    Stack,
} from '@mui/material'
import {
    Leaderboard as LeaderboardIcon,
    BookmarkAdd as SaveIcon,
    Block as RejectIcon,
    Restore as RestoreIcon,
    ExpandMore as ExpandIcon,
    ExpandLess as CollapseIcon,
} from '@mui/icons-material'
import { jobsApi, rankingsApi } from '../services/api'
import { Job, RankingResult } from '../types'

// Score chip with color coding
function ScoreChip({ score, label }: { score: number; label: string }) {
    const pct = Math.round(score * 100)
    let color: 'success' | 'warning' | 'error' = 'error'
    if (score >= 0.7) color = 'success'
    else if (score >= 0.4) color = 'warning'

    return (
        <Tooltip title={label}>
            <Chip
                label={`${pct}%`}
                color={color}
                size="small"
                variant="filled"
                sx={{ fontWeight: 700, minWidth: 56 }}
            />
        </Tooltip>
    )
}

// Score bar for visual representation
function ScoreBar({ score, label }: { score: number; label: string }) {
    const pct = Math.round(score * 100)
    let barColor = '#ef5350'
    if (score >= 0.7) barColor = '#66bb6a'
    else if (score >= 0.4) barColor = '#ffa726'

    return (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, minWidth: 140 }}>
            <Typography variant="caption" sx={{ color: '#666', minWidth: 44 }}>
                {label}
            </Typography>
            <Box sx={{ flex: 1 }}>
                <LinearProgress
                    variant="determinate"
                    value={pct}
                    sx={{
                        height: 8,
                        borderRadius: 4,
                        bgcolor: '#e0e0e0',
                        '& .MuiLinearProgress-bar': { bgcolor: barColor, borderRadius: 4 },
                    }}
                />
            </Box>
            <Typography variant="caption" sx={{ fontWeight: 700, minWidth: 32 }}>
                {pct}%
            </Typography>
        </Box>
    )
}

export default function Rankings() {
    const [jobs, setJobs] = useState<Job[]>([])
    const [selectedJobId, setSelectedJobId] = useState<number | ''>('')
    const [rankings, setRankings] = useState<RankingResult[]>([])
    const [loading, setLoading] = useState(false)
    const [ranking, setRanking] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [expandedRow, setExpandedRow] = useState<string | null>(null)

    // Load jobs on mount
    useEffect(() => {
        jobsApi.getAll().then(setJobs).catch(() => setError('Failed to load jobs'))
    }, [])

    // Load cached rankings when job changes
    useEffect(() => {
        if (!selectedJobId) {
            setRankings([])
            return
        }
        setLoading(true)
        rankingsApi
            .getRankings(selectedJobId)
            .then((res) => {
                setRankings(res.rankings)
            })
            .catch(() => setRankings([]))
            .finally(() => setLoading(false))
    }, [selectedJobId])

    // Trigger Ollama ranking
    const handleRank = async () => {
        if (!selectedJobId) return
        setRanking(true)
        setError(null)
        try {
            const res = await rankingsApi.rankByJob(selectedJobId)
            setRankings(res.rankings)
        } catch {
            setError('Ranking failed. Make sure Ollama is running.')
        } finally {
            setRanking(false)
        }
    }

    // Update candidate status
    const handleStatus = async (email: string, status: 'active' | 'saved' | 'rejected') => {
        if (!selectedJobId) return
        try {
            await rankingsApi.updateStatus(email, selectedJobId, status)
            setRankings((prev) =>
                prev.map((r) => (r.candidate_email === email ? { ...r, status } : r))
            )
        } catch {
            setError('Failed to update status')
        }
    }

    const statusColor = (s: string) => {
        if (s === 'saved') return 'success'
        if (s === 'rejected') return 'error'
        return 'default'
    }

    return (
        <Box>
            {/* Header */}
            <Box
                sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    mb: 3,
                }}
            >
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                    Rankings
                </Typography>
            </Box>

            {/* Job Selector + Rank Button */}
            <Paper
                sx={{
                    p: 3,
                    mb: 3,
                    background: 'linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%)',
                    borderRadius: 3,
                }}
            >
                <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} alignItems="center">
                    <FormControl sx={{ minWidth: 300 }}>
                        <InputLabel>Select a Job</InputLabel>
                        <Select
                            value={selectedJobId}
                            label="Select a Job"
                            onChange={(e) => setSelectedJobId(e.target.value as number)}
                            sx={{ bgcolor: '#fff', borderRadius: 2 }}
                        >
                            {jobs.map((job) => (
                                <MenuItem key={job.id} value={job.id}>
                                    {job.title} — ₹{((job.min_budget ?? 0) / 1000).toFixed(0)}K–₹{((job.max_budget ?? 0) / 1000).toFixed(0)}K
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    <Button
                        variant="contained"
                        color="primary"
                        startIcon={ranking ? <CircularProgress size={18} color="inherit" /> : <LeaderboardIcon />}
                        onClick={handleRank}
                        disabled={!selectedJobId || ranking}
                        sx={{
                            px: 4,
                            py: 1.5,
                            borderRadius: 2,
                            fontWeight: 700,
                            textTransform: 'none',
                            fontSize: '1rem',
                            background: 'linear-gradient(135deg, #1976d2, #7c4dff)',
                            '&:hover': { background: 'linear-gradient(135deg, #1565c0, #651fff)' },
                        }}
                    >
                        {ranking ? 'Ranking with Ollama...' : 'Rank Candidates'}
                    </Button>

                    {rankings.length > 0 && (
                        <Chip
                            label={`${rankings.length} candidates ranked`}
                            color="info"
                            variant="outlined"
                            sx={{ fontWeight: 600 }}
                        />
                    )}
                </Stack>

                {ranking && (
                    <Box sx={{ mt: 2 }}>
                        <Alert severity="info" sx={{ borderRadius: 2 }}>
                            🧠 Ollama is analyzing resumes against the job description. This may take 30–60 seconds...
                        </Alert>
                        <LinearProgress sx={{ mt: 1, borderRadius: 2 }} />
                    </Box>
                )}
            </Paper>

            {error && (
                <Alert severity="error" sx={{ mb: 2, borderRadius: 2 }} onClose={() => setError(null)}>
                    {error}
                </Alert>
            )}

            {/* Loading state */}
            {loading && (
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                    <CircularProgress />
                </Box>
            )}

            {/* Rankings Table */}
            {!loading && rankings.length > 0 && (
                <TableContainer component={Paper} sx={{ borderRadius: 3, boxShadow: 3 }}>
                    <Table>
                        <TableHead>
                            <TableRow
                                sx={{
                                    background: 'linear-gradient(135deg, #1976d2, #7c4dff)',
                                    '& th': { color: '#fff', fontWeight: 700, fontSize: '0.9rem' },
                                }}
                            >
                                <TableCell>#</TableCell>
                                <TableCell>Candidate</TableCell>
                                <TableCell align="center">JD Match</TableCell>
                                <TableCell align="center">Comparative</TableCell>
                                <TableCell align="center">Salary Fit</TableCell>
                                <TableCell align="center">Overall</TableCell>
                                <TableCell align="center">Budget</TableCell>
                                <TableCell align="center">Status</TableCell>
                                <TableCell align="center">Actions</TableCell>
                                <TableCell />
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {rankings.map((r, i) => (
                                <>
                                    <TableRow
                                        key={r.candidate_email}
                                        sx={{
                                            bgcolor: r.status === 'rejected' ? '#fce4ec' : r.status === 'saved' ? '#e8f5e9' : 'inherit',
                                            opacity: r.status === 'rejected' ? 0.65 : 1,
                                            '&:hover': { bgcolor: '#f5f5f5' },
                                            transition: 'all 0.2s',
                                        }}
                                    >
                                        <TableCell>
                                            <Typography
                                                variant="h6"
                                                sx={{
                                                    fontWeight: 800,
                                                    color: i === 0 ? '#ffd700' : i === 1 ? '#c0c0c0' : i === 2 ? '#cd7f32' : '#999',
                                                    fontSize: i < 3 ? '1.3rem' : '1rem',
                                                }}
                                            >
                                                {i + 1}
                                            </Typography>
                                        </TableCell>
                                        <TableCell>
                                            <Typography variant="subtitle2" sx={{ fontWeight: 700 }}>
                                                {r.candidate_name}
                                            </Typography>
                                            <Typography variant="caption" color="text.secondary">
                                                {r.candidate_email}
                                            </Typography>
                                            <br />
                                            <Typography variant="caption" color="text.secondary">
                                                CTC: ₹{r.current_ctc?.toLocaleString()} → ₹{r.expected_ctc?.toLocaleString()}
                                            </Typography>
                                        </TableCell>
                                        <TableCell align="center">
                                            <ScoreChip score={r.jd_match_score} label="How well candidate fits the job description" />
                                        </TableCell>
                                        <TableCell align="center">
                                            <ScoreChip score={r.comparative_score} label="How candidate ranks vs other candidates" />
                                        </TableCell>
                                        <TableCell align="center">
                                            <ScoreChip score={r.salary_match_score} label="Salary expectation vs job budget" />
                                        </TableCell>
                                        <TableCell align="center">
                                            <Chip
                                                label={`${Math.round(r.overall_score * 100)}%`}
                                                sx={{
                                                    fontWeight: 800,
                                                    fontSize: '0.95rem',
                                                    minWidth: 64,
                                                    bgcolor:
                                                        r.overall_score >= 0.7
                                                            ? '#2e7d32'
                                                            : r.overall_score >= 0.4
                                                                ? '#ed6c02'
                                                                : '#d32f2f',
                                                    color: '#fff',
                                                }}
                                            />
                                        </TableCell>
                                        <TableCell align="center">
                                            <Chip
                                                label={r.budget_fit}
                                                size="small"
                                                color={
                                                    r.budget_fit === 'Within budget'
                                                        ? 'success'
                                                        : r.budget_fit === 'Slightly above'
                                                            ? 'warning'
                                                            : 'error'
                                                }
                                                variant="outlined"
                                                sx={{ fontWeight: 600 }}
                                            />
                                        </TableCell>
                                        <TableCell align="center">
                                            <Chip
                                                label={r.status.toUpperCase()}
                                                size="small"
                                                color={statusColor(r.status) as 'success' | 'error' | 'default'}
                                                sx={{ fontWeight: 700, minWidth: 80 }}
                                            />
                                        </TableCell>
                                        <TableCell align="center">
                                            <Stack direction="row" spacing={0.5}>
                                                {r.status !== 'saved' && (
                                                    <Tooltip title="Save for later">
                                                        <IconButton
                                                            size="small"
                                                            color="success"
                                                            onClick={() => handleStatus(r.candidate_email, 'saved')}
                                                        >
                                                            <SaveIcon fontSize="small" />
                                                        </IconButton>
                                                    </Tooltip>
                                                )}
                                                {r.status !== 'rejected' && (
                                                    <Tooltip title="Reject">
                                                        <IconButton
                                                            size="small"
                                                            color="error"
                                                            onClick={() => handleStatus(r.candidate_email, 'rejected')}
                                                        >
                                                            <RejectIcon fontSize="small" />
                                                        </IconButton>
                                                    </Tooltip>
                                                )}
                                                {r.status !== 'active' && (
                                                    <Tooltip title="Restore to active">
                                                        <IconButton
                                                            size="small"
                                                            color="primary"
                                                            onClick={() => handleStatus(r.candidate_email, 'active')}
                                                        >
                                                            <RestoreIcon fontSize="small" />
                                                        </IconButton>
                                                    </Tooltip>
                                                )}
                                            </Stack>
                                        </TableCell>
                                        <TableCell>
                                            <IconButton
                                                size="small"
                                                onClick={() =>
                                                    setExpandedRow(expandedRow === r.candidate_email ? null : r.candidate_email)
                                                }
                                            >
                                                {expandedRow === r.candidate_email ? <CollapseIcon /> : <ExpandIcon />}
                                            </IconButton>
                                        </TableCell>
                                    </TableRow>

                                    {/* Expandable detail row */}
                                    <TableRow key={`${r.candidate_email}-detail`}>
                                        <TableCell colSpan={10} sx={{ py: 0, border: 0 }}>
                                            <Collapse in={expandedRow === r.candidate_email}>
                                                <Box sx={{ p: 2, bgcolor: '#fafafa', borderRadius: 2, my: 1 }}>
                                                    <Stack direction={{ xs: 'column', md: 'row' }} spacing={4}>
                                                        <Box sx={{ flex: 1 }}>
                                                            <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 700 }}>
                                                                Score Breakdown
                                                            </Typography>
                                                            <ScoreBar score={r.jd_match_score} label="JD" />
                                                            <ScoreBar score={r.comparative_score} label="Comp" />
                                                            <ScoreBar score={r.salary_match_score} label="Salary" />
                                                            <ScoreBar score={r.overall_score} label="Overall" />
                                                        </Box>
                                                        <Box sx={{ flex: 1 }}>
                                                            <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 700, color: '#2e7d32' }}>
                                                                ✅ Strengths
                                                            </Typography>
                                                            {r.strengths.map((s, idx) => (
                                                                <Chip key={idx} label={s} size="small" color="success" variant="outlined" sx={{ mr: 0.5, mb: 0.5 }} />
                                                            ))}
                                                            <Typography variant="subtitle2" sx={{ mt: 2, mb: 1, fontWeight: 700, color: '#d32f2f' }}>
                                                                ⚠️ Weaknesses
                                                            </Typography>
                                                            {r.weaknesses.map((w, idx) => (
                                                                <Chip key={idx} label={w} size="small" color="error" variant="outlined" sx={{ mr: 0.5, mb: 0.5 }} />
                                                            ))}
                                                        </Box>
                                                        <Box sx={{ flex: 1 }}>
                                                            <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 700 }}>
                                                                💰 Salary Analysis
                                                            </Typography>
                                                            <Typography variant="body2">
                                                                Gap: {r.salary_gap_percentage > 0 ? '+' : ''}{r.salary_gap_percentage}%
                                                            </Typography>
                                                            <Typography variant="body2" sx={{ mt: 1 }}>
                                                                📝 {r.recommendation}
                                                            </Typography>
                                                        </Box>
                                                    </Stack>
                                                </Box>
                                            </Collapse>
                                        </TableCell>
                                    </TableRow>
                                </>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            )}

            {/* Empty state */}
            {!loading && !ranking && rankings.length === 0 && selectedJobId && (
                <Paper sx={{ p: 4, textAlign: 'center', borderRadius: 3 }}>
                    <LeaderboardIcon sx={{ fontSize: 64, color: '#bbb', mb: 2 }} />
                    <Typography variant="h6" color="text.secondary">
                        No rankings yet for this job
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        Click "Rank Candidates" to analyze all candidates against this job description using Ollama
                    </Typography>
                </Paper>
            )}

            {/* Initial state */}
            {!selectedJobId && (
                <Paper sx={{ p: 4, textAlign: 'center', borderRadius: 3 }}>
                    <LeaderboardIcon sx={{ fontSize: 64, color: '#bbb', mb: 2 }} />
                    <Typography variant="h6" color="text.secondary">
                        Select a job to get started
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Choose a job from the dropdown above, then rank candidates against its description
                    </Typography>
                </Paper>
            )}
        </Box>
    )
}
