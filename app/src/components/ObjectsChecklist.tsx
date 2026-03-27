'use client';

import React from 'react';
import { Box, Typography, Chip } from '@mui/material';

interface ObjectItem {
  id: string;
  name: string;
  icon: string;
}

interface ObjectsChecklistProps {
  selectedObjects: string[];
  onObjectsChange: (objects: string[]) => void;
}

const OBJECT_GROUPS: { label: string; items: ObjectItem[] }[] = [
  {
    label: 'Furniture',
    items: [
      { id: 'sofa', name: 'Sofa', icon: '🛋️' },
      { id: 'coffee_table', name: 'Coffee Table', icon: '☕' },
      { id: 'dining_table', name: 'Dining Table', icon: '🍽️' },
      { id: 'chair', name: 'Chair', icon: '🪑' },
      { id: 'armchair', name: 'Armchair', icon: '💺' },
      { id: 'bed', name: 'Bed', icon: '🛏️' },
      { id: 'desk', name: 'Desk', icon: '📝' },
      { id: 'tv_stand', name: 'TV Stand', icon: '📺' },
      { id: 'bookshelf', name: 'Bookshelf', icon: '📚' },
    ],
  },
  {
    label: 'Decor',
    items: [
      { id: 'rug', name: 'Rug', icon: '🟫' },
      { id: 'plant', name: 'Plant', icon: '🌿' },
      { id: 'vase', name: 'Vase', icon: '🏺' },
      { id: 'cushion', name: 'Cushions', icon: '🧸' },
      { id: 'table_lamp', name: 'Table Lamp', icon: '💡' },
      { id: 'floor_lamp', name: 'Floor Lamp', icon: '🪔' },
    ],
  },
  {
    label: 'Wall & Ceiling',
    items: [
      { id: 'mirror', name: 'Mirror', icon: '🪞' },
      { id: 'painting', name: 'Painting', icon: '🖼️' },
      { id: 'wall_shelf', name: 'Wall Shelf', icon: '📦' },
      { id: 'clock', name: 'Clock', icon: '🕐' },
      { id: 'pendant_light', name: 'Pendant Light', icon: '💡' },
      { id: 'chandelier', name: 'Chandelier', icon: '✨' },
    ],
  },
];

export default function ObjectsChecklist({
  selectedObjects,
  onObjectsChange,
}: ObjectsChecklistProps) {
  const toggleObject = (objectId: string) => {
    if (selectedObjects.includes(objectId)) {
      onObjectsChange(selectedObjects.filter((id) => id !== objectId));
    } else {
      onObjectsChange([...selectedObjects, objectId]);
    }
  };

  return (
    <Box sx={{ mt: 2 }}>
      {OBJECT_GROUPS.map((group) => (
        <Box key={group.label} sx={{ mb: 1.5 }}>
          <Typography 
            variant="caption" 
            sx={{ 
              fontWeight: 700, 
              color: 'text.secondary', 
              display: 'block', 
              mb: 0.5,
              textTransform: 'uppercase',
              letterSpacing: 0.5
            }}
          >
            {group.label}
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {group.items.map((item) => {
              const isSelected = selectedObjects.includes(item.id);
              return (
                <Chip
                  key={item.id}
                  label={`${item.icon} ${item.name}`}
                  onClick={() => toggleObject(item.id)}
                  sx={{
                    cursor: 'pointer',
                    borderRadius: '10px',
                    fontWeight: isSelected ? 700 : 500,
                    transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
                    bgcolor: isSelected ? 'primary.main' : 'white',
                    color: isSelected ? 'white' : 'text.primary',
                    border: '1px solid',
                    borderColor: isSelected ? 'primary.main' : 'rgba(0,0,0,0.1)',
                    '&:hover': {
                      transform: 'translateY(-2px)',
                      backgroundColor: isSelected ? 'primary.dark' : 'primary.50',
                      borderColor: 'primary.main'
                    },
                    boxShadow: isSelected ? '0 4px 8px rgba(37, 99, 235, 0.2)' : 'none'
                  }}
                />
              );
            })}
          </Box>
        </Box>
      ))}
      {selectedObjects.length > 0 && (
        <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block', fontStyle: 'italic' }}>
          {selectedObjects.length} items selected for addition
        </Typography>
      )}
    </Box>
  );
}
