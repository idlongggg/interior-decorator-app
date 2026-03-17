'use client';

import React from 'react';
import { FormControl, InputLabel, Select, MenuItem, SelectChangeEvent, Box } from '@mui/material';

interface StyleSelectorProps {
  selectedStyle: string;
  onStyleSelect: (style: string) => void;
}

const STYLES = [
  { id: 'Minimalist', name: 'Minimalist', desc: 'Clean, open, simple' },
  { id: 'Scandi', name: 'Scandinavian', desc: 'Cozy, light wood, natural' },
  { id: 'Indochine', name: 'Indochine', desc: 'Tropical, traditional, dark wood' },
  { id: 'Modern', name: 'Modern', desc: 'Luxury, sleek, elegant' },
];

export default function StyleSelector({ selectedStyle, onStyleSelect }: StyleSelectorProps) {
  const handleChange = (event: SelectChangeEvent) => {
    onStyleSelect(event.target.value);
  };

  return (
    <Box sx={{ mt: 3 }}>
      <FormControl fullWidth size="small">
        <InputLabel id="style-select-label">Design Style</InputLabel>
        <Select
          labelId="style-select-label"
          value={selectedStyle}
          label="Design Style"
          onChange={handleChange}
        >
          {STYLES.map((style) => (
            <MenuItem key={style.id} value={style.id}>
              {style.name} - {style.desc}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  );
}
