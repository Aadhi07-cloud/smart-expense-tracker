'use client'

import { TrendingUp, Wallet } from 'lucide-react'

interface SummaryCardProps {
  title: string
  amount: number
  currency?: string
  icon?: React.ReactNode
  className?: string
  gradient?: 'lime' | 'orange' | 'blue' | 'purple'
}

export function SummaryCard({
  title,
  amount,
  currency = '$',
  icon,
  className = '',
  gradient = 'lime',
}: SummaryCardProps) {
  const gradients = {
    lime: 'from-lime-300 to-lime-100 dark:from-lime-500 dark:to-lime-600',
    orange: 'from-orange-300 to-orange-100 dark:from-orange-500 dark:to-orange-600',
    blue: 'from-blue-300 to-blue-100 dark:from-blue-500 dark:to-blue-600',
    purple: 'from-purple-300 to-purple-100 dark:from-purple-500 dark:to-purple-600',
  }

  return (
    <div
      className={`relative overflow-hidden rounded-3xl p-6 ${gradients[gradient]} shadow-lg transition-transform duration-300 hover:scale-105 ${className}`}
    >
      {/* Decorative dot pattern */}
      <div className="absolute top-4 right-4 w-24 h-24 opacity-20 pointer-events-none">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <circle cx="6" cy="6" r="1.5" />
          <circle cx="12" cy="6" r="1.5" />
          <circle cx="18" cy="6" r="1.5" />
          <circle cx="6" cy="12" r="1.5" />
          <circle cx="12" cy="12" r="1.5" />
          <circle cx="18" cy="12" r="1.5" />
          <circle cx="6" cy="18" r="1.5" />
          <circle cx="12" cy="18" r="1.5" />
          <circle cx="18" cy="18" r="1.5" />
        </svg>
      </div>

      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm font-semibold opacity-75 uppercase tracking-wide">
            {title}
          </p>
          <div className="p-2 bg-white/40 dark:bg-white/20 rounded-xl backdrop-blur">
            {icon || <Wallet className="w-5 h-5" />}
          </div>
        </div>
        <p className="text-4xl font-bold">
          {currency}
          {amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
        </p>
        <div className="mt-3 flex items-center gap-2 text-xs opacity-70">
          <TrendingUp className="w-4 h-4" />
          <span>Current period</span>
        </div>
      </div>
    </div>
  )
}
