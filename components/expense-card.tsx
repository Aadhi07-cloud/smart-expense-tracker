'use client'

import { Trash2 } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface ExpenseCardProps {
  id: string
  title: string
  amount: number
  category: string
  date: string
  onDelete: (id: string) => void
  isDeleting?: boolean
}

const categoryColors: Record<string, string> = {
  food: 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300',
  transport: 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300',
  entertainment: 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300',
  utilities: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300',
  other: 'bg-slate-100 dark:bg-slate-900/30 text-slate-700 dark:text-slate-300',
}

export function ExpenseCard({
  id,
  title,
  amount,
  category,
  date,
  onDelete,
  isDeleting = false,
}: ExpenseCardProps) {
  const categoryColor = categoryColors[category.toLowerCase()] || categoryColors.other
  const formattedDate = new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })

  return (
    <div className="glass p-4 rounded-2xl hover:shadow-lg transition-all duration-300 animate-slide-up">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${categoryColor}`}>
              {category}
            </span>
          </div>
          <h3 className="font-semibold text-foreground mb-1">{title}</h3>
          <p className="text-sm text-muted-foreground">{formattedDate}</p>
        </div>
        <div className="text-right ml-4">
          <p className="text-2xl font-bold text-primary mb-3">
            ${amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onDelete(id)}
            disabled={isDeleting}
            className="text-destructive hover:text-destructive hover:bg-destructive/10"
          >
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}
