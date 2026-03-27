'use client';

import React, { useCallback } from 'react';
import { Box, Typography, IconButton, Button } from '@mui/material';
import { CloudUpload, Close, PhotoLibrary } from '@mui/icons-material';

interface ImageUploaderProps {
  onImageSelected: (file: File) => void;
  previewUrl: string | null;
  onClear: () => void;
}

export default function ImageUploader({ onImageSelected, previewUrl, onClear }: ImageUploaderProps) {
  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      if (e.dataTransfer.files[0].type.startsWith('image/')) {
        onImageSelected(e.dataTransfer.files[0]);
      }
    }
  }, [onImageSelected]);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      if (e.target.files[0].type.startsWith('image/')) {
        onImageSelected(e.target.files[0]);
      }
    }
  };

  return (
    <Box sx={{ width: '100%' }}>
      {!previewUrl ? (
        <Box
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: { xs: 200, sm: 320 },
            border: '2px dashed',
            borderColor: 'grey.300',
            borderRadius: 4,
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            bgcolor: 'white',
            '&:hover': {
              borderColor: 'primary.main',
              bgcolor: 'primary.50',
              transform: 'translateY(-2px)',
              boxShadow: '0 12px 20px -10px rgba(37, 99, 235, 0.15)',
            },
            p: { xs: 3, sm: 4 },
            textAlign: 'center',
            overflow: 'hidden'
          }}
        >
          <Box sx={{ 
            width: 64, 
            height: 64, 
            borderRadius: '50%', 
            bgcolor: 'primary.50', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            mb: 2,
            color: 'primary.main'
          }}>
            <CloudUpload sx={{ fontSize: 32 }} />
          </Box>
          <Typography variant="h6" sx={{ mb: 1, fontWeight: 700, color: '#1e293b' }}>
            Upload Room Photo
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3, maxWidth: 240, mx: 'auto' }}>
            Choose a clear photo of your room for the best results
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', justifyContent: 'center' }}>
            <Button
              variant="contained"
              component="label"
              startIcon={<PhotoLibrary />}
              sx={{ 
                borderRadius: '10px', 
                boxShadow: 'none',
                px: 3,
                '&:hover': { boxShadow: '0 4px 12px rgba(37, 99, 235, 0.2)' }
              }}
            >
              Select Image
              <input
                type="file"
                hidden
                onChange={handleFileInput}
                accept="image/*"
              />
            </Button>
          </Box>
        </Box>
      ) : (
        <Box sx={{ 
          position: 'relative', 
          width: '100%', 
          height: { xs: 250, sm: 320 }, 
          borderRadius: 4, 
          overflow: 'hidden', 
          bgcolor: '#0f172a',
          boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)'
        }}>
          <img
            src={previewUrl}
            alt="Room preview"
            style={{ width: '100%', height: '100%', objectFit: 'contain' }}
          />
          <IconButton
            onClick={onClear}
            sx={{
              position: 'absolute',
              top: 12,
              right: 12,
              bgcolor: 'rgba(0, 0, 0, 0.5)',
              color: 'white',
              backdropFilter: 'blur(10px)',
              '&:hover': { bgcolor: 'rgba(211, 47, 47, 0.9)' },
            }}
            size="small"
          >
            <Close fontSize="small" />
          </IconButton>
        </Box>
      )}
    </Box>
  );
}
