'use client';

import { useDraggable } from '@dnd-kit/core';
import { CSS } from '@dnd-kit/utilities';
import { GripVertical } from 'lucide-react';
import { cn } from '@/lib/utils';

interface DraggableTemplateProps {
  id: string;
  title: string;
  type: 'expense' | 'income';
}

function DraggableTemplate({ id, title, type }: DraggableTemplateProps) {
  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({
    id: `template-${id}`,
    data: {
      type: 'template',
      templateType: type,
      title,
    },
  });

  const style = {
    transform: CSS.Translate.toString(transform),
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={cn(
        "flex flex-row items-center gap-2 p-2 rounded-md border text-sm font-medium transition-colors shadow-sm cursor-grab active:cursor-grabbing",
        isDragging ? "opacity-50 border-primary bg-primary/10" : "bg-card hover:bg-accent hover:text-accent-foreground",
        type === 'income' ? "border-green-200 dark:border-green-900" : "border-zinc-200 dark:border-zinc-800"
      )}
      {...listeners}
      {...attributes}
    >
      <GripVertical className="h-4 w-4 text-muted-foreground shrink-0" />
      <span className="truncate">{title}</span>
    </div>
  );
}

interface DraggableTemplateGroupProps {
  title: string;
  items: string[];
  type: 'expense' | 'income';
}

export function DraggableTemplateGroup({ title, items, type }: DraggableTemplateGroupProps) {
  return (
    <div className="space-y-3">
      <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">{title}</h3>
      <div className="grid grid-cols-1 gap-2">
        {items.map((item) => (
          <DraggableTemplate key={item} id={`${type}-${item.toLowerCase().replace(/\s+/g, '-')}`} title={item} type={type} />
        ))}
      </div>
    </div>
  );
}
