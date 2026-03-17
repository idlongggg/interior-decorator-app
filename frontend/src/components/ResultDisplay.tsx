'use client';

import React from 'react';
import { Box, Typography, CircularProgress, Button } from '@mui/material';
import { Download } from '@mui/icons-material';

interface ResultDisplayProps {
  originalImage: string | null;
  resultImage: string | null;
  isGenerating: boolean;
}

export default function ResultDisplay({ originalImage, resultImage, isGenerating }: ResultDisplayProps) {
  return (
    <Box
      sx={{
        width: '100%',
        height: '100%',
        minHeight: 280,
        borderRadius: 3,
        overflow: 'hidden',
        bgcolor: 'grey.100',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
      }}
    >
      {isGenerating ? (
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress size={48} sx={{ mb: 2 }} />
          <Typography>Generating...</Typography>
        </Box>
      ) : resultImage ? (
        <Box sx={{ width: '100%', height: '100%', position: 'relative' }}>
          <img
            src={resultImage}
            alt="Generated result"
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
          <Button
            variant="contained"
            startIcon={<Download />}
            href={resultImage}
            download="result.jpg"
            sx={{
              position: 'absolute',
              bottom: 16,
              right: 16,
            }}
          >
            Download
          </Button>
        </Box>
      ) : originalImage ? (
        <Typography color="text.secondary">
          Click "Generate" to see the result
        </Typography>
      ) : (
        <Typography color="text.secondary">
          Upload an image to get started
        </Typography>
      )}
    </Box>
  );
}
