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
  { id: 'Custom', name: 'Custom', desc: 'Your Own Style', img: 'https://images.unsplash.com/photo-1594026112284-02bb6f3352fe?auto=format&fit=crop&w=400&q=80' },
];

export default function StyleSelector({ selectedStyle, onStyleSelect }: StyleSelectorProps) {
  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 500 }}>
        Select Design Style
      </Typography>
      <Grid container spacing={2}>
        {STYLES.map((style) => (
          <Grid key={style.id} size={{ xs: 6, sm: 4, md: 2.4 }}>
            <Card 
              sx={{ 
                borderRadius: 3,
                border: '2px solid',
                borderColor: selectedStyle === style.id ? 'primary.main' : 'transparent',
                boxShadow: selectedStyle === style.id 
                  ? '0 10px 15px -3px rgba(37, 99, 235, 0.2)' 
                  : '0 4px 6px -1px rgb(0 0 0 / 0.05)',
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                overflow: 'hidden',
                bgcolor: 'white',
                '&:hover': { 
                  transform: 'translateY(-4px)',
                  boxShadow: '0 12px 20px -5px rgb(0 0 0 / 0.1)',
                  borderColor: selectedStyle === style.id ? 'primary.main' : 'primary.100'
                }
              }}
            >
              <CardActionArea onClick={() => onStyleSelect(style.id)} sx={{ height: '100%' }}>
                <Box sx={{ position: 'relative' }}>
                  <CardMedia
                    component="img"
                    sx={{ height: { xs: 80, sm: 110 }, objectFit: 'cover' }}
                    image={style.img}
                    alt={style.name}
                  />
                  {selectedStyle === style.id && (
                    <Box sx={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      right: 0,
                      bottom: 0,
                      bgcolor: 'rgba(37, 99, 235, 0.1)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      <Box sx={{ 
                        bgcolor: 'primary.main', 
                        color: 'white', 
                        borderRadius: '50%', 
                        width: 24, 
                        height: 24, 
                        display: 'flex', 
                        alignItems: 'center', 
                        justifyContent: 'center',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
                      }}>
                        <Typography variant="caption" sx={{ fontWeight: 800 }}>✓</Typography>
                      </Box>
                    </Box>
                  )}
                </Box>
                <CardContent sx={{ p: 1.5, textAlign: 'center' }}>
                  <Typography variant="body2" sx={{ fontWeight: 700, fontSize: '0.875rem' }}>
                    {style.name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary" sx={{ display: 'block', fontSize: '0.7rem', mt: 0.5 }}>
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
