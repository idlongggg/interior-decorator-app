'use client';

import React, { useCallback } from 'react';
import { Box, Typography, IconButton, Button } from '@mui/material';
import { CloudUpload, Close, PhotoLibrary, CameraAlt } from '@mui/icons-material';

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
            minHeight: { xs: 200, sm: 280 },
            border: '2px dashed',
            borderColor: 'grey.300',
            borderRadius: 3,
            transition: 'all 0.2s',
            bgcolor: 'grey.50',
            '&:hover': {
              borderColor: 'primary.main',
              bgcolor: 'action.hover',
            },
            p: { xs: 2, sm: 3 },
            textAlign: 'center',
            overflow: 'hidden'
          }}
        >
          <CloudUpload sx={{ fontSize: { xs: 32, sm: 48 }, color: 'grey.400', mb: 1 }} />
          <Typography variant="subtitle1" color="text.secondary" sx={{ mb: 2, fontWeight: 500 }}>
            Upload Room Photo
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 1.5, flexWrap: 'wrap', justifyContent: 'center' }}>
            <Button
              variant="outlined"
              size="small"
              component="label"
              startIcon={<PhotoLibrary />}
              sx={{ borderRadius: 2, bgcolor: 'white' }}
            >
              Gallery
              <input
                type="file"
                hidden
                onChange={handleFileInput}
                accept="image/*"
              />
            </Button>
            
            <Button
              variant="outlined"
              size="small"
              component="label"
              startIcon={<CameraAlt />}
              sx={{ borderRadius: 2, bgcolor: 'white' }}
            >
              Camera
              <input
                type="file"
                hidden
                onChange={handleFileInput}
                accept="image/*"
                capture="environment"
              />
            </Button>
          </Box>
          
          <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: { xs: 'none', sm: 'block' } }}>
            or drag and drop image here
          </Typography>
        </Box>
      ) : (
        <Box sx={{ position: 'relative', width: '100%', height: { xs: 250, sm: 320 }, borderRadius: 3, overflow: 'hidden', bgcolor: 'black' }}>
          <img
            src={previewUrl}
            alt="Room preview"
            style={{ width: '100%', height: '100%', objectFit: 'contain' }}
          />
          <IconButton
            onClick={onClear}
            sx={{
              position: 'absolute',
              top: 8,
              right: 8,
              bgcolor: 'rgba(211, 47, 47, 0.9)',
              color: 'white',
              '&:hover': { bgcolor: 'error.dark' },
              size: 'small'
            }}
          >
            <Close fontSize="small" />
          </IconButton>
        </Box>
      )}
    </Box>
  );
}
