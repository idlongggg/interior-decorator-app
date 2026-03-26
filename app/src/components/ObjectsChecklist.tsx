'use client';

import React from 'react';
import { Card } from '@heroui/react';

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
    <div className="mt-2 space-y-3">
      {OBJECT_GROUPS.map((group) => (
        <div key={group.label}>
          <p className="text-[11px] font-bold uppercase tracking-wider text-default-400 mb-1.5">
            {group.label}
          </p>
          <div className="flex flex-wrap gap-1.5">
            {group.items.map((item) => {
              const isSelected = selectedObjects.includes(item.id);
              return (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => toggleObject(item.id)}
                  className="border-0 p-0 bg-transparent"
                >
                  <Card
                    className={`
                      px-2.5 py-1.5 cursor-pointer select-none transition-all duration-200 
                      flex flex-row items-center gap-1.5 text-xs font-medium
                      ${
                        isSelected
                          ? 'bg-primary/10 border-2 border-primary text-primary shadow-sm shadow-primary/20 scale-[1.02]'
                          : 'bg-default-50 border-2 border-transparent text-default-600 hover:bg-default-100 hover:scale-[1.02]'
                      }
                    `}
                  >
                    <span className="text-sm leading-none">{item.icon}</span>
                    <span className="whitespace-nowrap">{item.name}</span>
                  </Card>
                </button>
              );
            })}
          </div>
        </div>
      ))}
      {selectedObjects.length > 0 && (
        <p className="text-[10px] text-default-400 font-medium mt-1">
          {selectedObjects.length} item{selectedObjects.length > 1 ? 's' : ''} selected
        </p>
      )}
    </div>
  );
}
