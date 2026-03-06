'use client';

import React, { useState } from 'react';
import {
  DndContext,
  DragOverlay,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragStartEvent,
  DragEndEvent,
} from '@dnd-kit/core';
import { sortableKeyboardCoordinates } from '@dnd-kit/sortable';

export function BoardDndContext({ children }: { children: React.ReactNode }) {
  const [activeId, setActiveId] = useState<string | null>(null);
  const [activeTitle, setActiveTitle] = useState<string | null>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 5, // minimum 5px drag to start intentionally
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragStart = (event: DragStartEvent) => {
    setActiveId(event.active.id as string);
    setActiveTitle(event.active.data.current?.title);
  };

  const handleDragEnd = (event: DragEndEvent) => {
    setActiveId(null);
    setActiveTitle(null);

    const { active, over } = event;

    if (over) {
      // Handle the drop logic here or relay it via a store/callback
      console.log(`Dropped ${active.id} over ${over.id}`);
      // In a real implementation this would trigger an optimistic state update in Zustand
      // and kick off a React Query mutation to the backend.
    }
  };

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >
      {children}
      <DragOverlay>
        {activeId ? (
          <div className="flex items-center gap-2 p-2 rounded-md border border-primary bg-background shadow-lg opacity-90 text-sm font-medium">
            <span className="truncate">{activeTitle || activeId}</span>
          </div>
        ) : null}
      </DragOverlay>
    </DndContext>
  );
}
