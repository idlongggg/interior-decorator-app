'use client';

import React from 'react';
import { Box, Typography, Card, CardMedia, CardContent, CardActionArea, Grid } from '@mui/material';

interface StyleSelectorProps {
  selectedStyle: string;
  onStyleSelect: (style: string) => void;
}

const STYLES = [
  { id: 'Minimalist', name: 'Minimalist', desc: 'Clean & Simple', img: '/styles/minimalist.png' },
  { id: 'Scandi', name: 'Scandinavian', desc: 'Cozy & Natural', img: '/styles/scandi.png' },
  { id: 'Indochine', name: 'Indochine', desc: 'Tropical & Dark', img: '/styles/indochine.png' },
  { id: 'Modern', name: 'Modern', desc: 'Sleek & Luxury', img: '/styles/modern.png' },
  { id: 'Custom', name: 'Custom', desc: 'Your Own Style', img: '/styles/custom.png' },
];

export default function StyleSelector({ selectedStyle, onStyleSelect }: StyleSelectorProps) {
  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 500 }}>
        Select Design Style
      </Typography>
      <Grid container spacing={2}>
        {STYLES.map((style) => (
          <Grid key={style.id} size={{ xs: 4, sm: 4, md: 2.4 }}>
            <Card 
              sx={{ 
                border: selectedStyle === style.id ? '2px solid #1976d2' : '2px solid transparent',
                transition: 'all 0.2s',
                '&:hover': { transform: 'translateY(-4px)' }
              }}
            >
              <CardActionArea onClick={() => onStyleSelect(style.id)}>
                <CardMedia
                  component="img"
                  sx={{ height: { xs: 70, sm: 100 } }}
                  image={style.img}
                  alt={style.name}
                />
                <CardContent sx={{ p: { xs: 0.5, sm: 1 }, textAlign: 'center' }}>
                  <Typography variant="body2" sx={{ fontWeight: 600, fontSize: { xs: '0.75rem', sm: '0.875rem' } }}>
                    {style.name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary" sx={{ display: { xs: 'none', sm: 'block' }, fontSize: '0.7rem' }}>
                    {style.desc}
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
