'use client';

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { styled } from '@mui/material/styles';

const ComparisonContainer = styled(Paper)(({ theme }) => ({
  position: 'relative',
  width: '100%',
  overflow: 'hidden',
  borderRadius: 16,
  backgroundColor: '#000',
  aspectRatio: '16/9',
  [theme.breakpoints.down('sm')]: {
    aspectRatio: '4/3',
  },
  cursor: 'col-resize',
  userSelect: 'none',
  boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
}));

const ImageLayer = styled('div')({
  position: 'absolute',
  top: 0,
  left: 0,
  width: '100%',
  height: '100%',
  '& img': {
    width: '100%',
    height: '100%',
    objectFit: 'cover', // Dùng cover để tránh lệch ảnh khi tỉ lệ không khớp hoàn hảo
    display: 'block',
    pointerEvents: 'none',
  },
});

const Label = styled(Typography)(({ theme }) => ({
  position: 'absolute',
  padding: '6px 14px',
  backgroundColor: 'rgba(0,0,0,0.6)',
  color: '#fff',
  borderRadius: 8,
  fontSize: '0.75rem',
  fontWeight: 700,
  backdropFilter: 'blur(8px)',
  zIndex: 10,
  textTransform: 'uppercase',
  letterSpacing: 1,
  pointerEvents: 'none',
  [theme.breakpoints.down('sm')]: {
    fontSize: '0.65rem',
    padding: '4px 10px',
  },
}));

const SliderHandle = styled('div')({
  position: 'absolute',
  top: 0,
  bottom: 0,
  width: 2,
  backgroundColor: '#fff',
  zIndex: 15,
  pointerEvents: 'none',
  '&::after': {
    content: '""',
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 40,
    height: 40,
    backgroundColor: '#fff',
    borderRadius: '50%',
    boxShadow: '0 0 20px rgba(0,0,0,0.2)',
    backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='%232563eb' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m18 8 4 4-4 4M6 8l-4 4 4 4'/%3E%3C/svg%3E")`,
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
  },
});

interface ImageComparisonProps {
  beforeImage: string;
  afterImage: string;
}

export default function ImageComparison({ beforeImage, afterImage }: ImageComparisonProps) {
  const [position, setPosition] = useState(50);
  const containerRef = useRef<HTMLDivElement>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleMove = useCallback((clientX: number) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = Math.max(0, Math.min(clientX - rect.left, rect.width));
    const percent = (x / rect.width) * 100;
    setPosition(percent);
  }, []);

  const onMouseDown = () => setIsDragging(true);
  const onMouseUp = () => setIsDragging(false);

  const onMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    handleMove(e.clientX);
  };

  const onTouchMove = (e: React.TouchEvent) => {
    handleMove(e.touches[0].clientX);
  };

  useEffect(() => {
    const handleWindowMouseUp = () => setIsDragging(false);
    const handleWindowMouseMove = (e: MouseEvent) => {
      if (isDragging) handleMove(e.clientX);
    };

    window.addEventListener('mouseup', handleWindowMouseUp);
    window.addEventListener('mousemove', handleWindowMouseMove);
    return () => {
      window.removeEventListener('mouseup', handleWindowMouseUp);
      window.removeEventListener('mousemove', handleWindowMouseMove);
    };
  }, [isDragging, handleMove]);

  return (
    <ComparisonContainer
      ref={containerRef}
      onMouseDown={onMouseDown}
      onTouchMove={onTouchMove}
      elevation={0}
      sx={{
        cursor: isDragging ? 'grabbing' : 'col-resize',
        '& img': {
          willChange: 'clip-path' // Tối ưu hiệu năng
        }
      }}
    >
      <ImageLayer>
        <img src={beforeImage} alt="Before" />
        <Label sx={{ top: 20, left: 20 }}>Original</Label>
      </ImageLayer>

      <ImageLayer sx={{ clipPath: `inset(0 0 0 ${position}%)`, zIndex: 5 }}>
        <img src={afterImage} alt="After" />
        <Label sx={{ top: 20, right: 20, bgcolor: 'primary.main' }}>Generated</Label>
      </ImageLayer>

      <SliderHandle style={{ left: `${position}%` }} />
    </ComparisonContainer>
  );
}
