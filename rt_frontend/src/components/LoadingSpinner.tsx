import { Box, CircularProgress } from '@mui/material'

interface LoadingSpinnerProps {
  size?: number
  color?: 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning'
}

export default function LoadingSpinner({
  size = 40,
  color = 'primary',
}: LoadingSpinnerProps) {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '200px',
      }}
    >
      <CircularProgress size={size} color={color} />
    </Box>
  )
} 