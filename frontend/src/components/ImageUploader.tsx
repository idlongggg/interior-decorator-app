'use client';

import React, { useCallback } from 'react';
import { Box, Typography, IconButton } from '@mui/material';
import { CloudUpload, Close } from '@mui/icons-material';

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
    <Box sx={{ width: '100%', height: '100%' }}>
      {!previewUrl ? (
        <Box
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100%',
            minHeight: 280,
            border: '2px dashed',
            borderColor: 'grey.300',
            borderRadius: 3,
            cursor: 'pointer',
            transition: 'all 0.2s',
            '&:hover': {
              borderColor: 'primary.main',
              bgcolor: 'action.hover',
            },
          }}
        >
          <input
            type="file"
            hidden
            onChange={handleFileInput}
            accept="image/*"
            id="image-upload-input"
          />
          <label htmlFor="image-upload-input" style={{ cursor: 'pointer', width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <CloudUpload sx={{ fontSize: 48, color: 'grey.400', mb: 2 }} />
            <Typography variant="h6" color="text.secondary">
              Upload Room Photo
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Drag & drop or click to browse
            </Typography>
          </label>
        </Box>
      ) : (
        <Box sx={{ position: 'relative', width: '100%', height: '100%', minHeight: 280, borderRadius: 3, overflow: 'hidden' }}>
          <img
            src={previewUrl}
            alt="Room preview"
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
          <IconButton
            onClick={onClear}
            sx={{
              position: 'absolute',
              top: 8,
              right: 8,
              bgcolor: 'error.main',
              color: 'white',
              '&:hover': { bgcolor: 'error.dark' },
            }}
          >
            <Close />
          </IconButton>
        </Box>
      )}
    </Box>
  );
}
