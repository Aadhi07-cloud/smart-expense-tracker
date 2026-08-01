'use client'

import { useState } from 'react'
import { Plus } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface AddExpenseFormProps {
  onSubmit: (expense: { title: string; amount: number; category: string; date: string }) => void
  isLoading?: boolean
}

const categories = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other']

export function AddExpenseForm({ onSubmit, isLoading = false }: AddExpenseFormProps) {
  const [title, setTitle] = useState('')
  const [amount, setAmount] = useState('')
  const [category, setCategory] = useState('Food')
  const [date, setDate] = useState(new Date().toISOString().split('T')[0])
  const [isOpen, setIsOpen] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (title.trim() && amount && parseFloat(amount) > 0) {
      onSubmit({
        title: title.trim(),
        amount: parseFloat(amount),
        category,
        date,
      })
      setTitle('')
      setAmount('')
      setCategory('Food')
      setDate(new Date().toISOString().split('T')[0])
      setIsOpen(false)
    }
  }

  return (
    <div className="relative">
      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-8 right-8 z-40 w-16 h-16 bg-gradient-to-br from-lime-300 to-lime-400 dark:from-lime-500 dark:to-lime-600 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-110 active:scale-95 flex items-center justify-center animate-pulse-glow"
      >
        <Plus className="w-6 h-6 text-slate-900 dark:text-white" />
      </button>

      {/* Modal Background */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/40 dark:bg-black/60 backdrop-blur-sm z-40 transition-opacity"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Form Modal */}
      {isOpen && (
        <div className="fixed bottom-0 left-0 right-0 z-50 sm:bottom-auto sm:left-1/2 sm:top-1/2 sm:transform sm:-translate-x-1/2 sm:-translate-y-1/2 sm:w-full sm:max-w-md animate-slide-up">
          <div className="glass m-4 rounded-3xl p-6 max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-6">Add New Expense</h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Title Input */}
              <div>
                <label className="block text-sm font-semibold mb-2">What did you spend on?</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g., Lunch at café"
                  className="w-full px-4 py-3 rounded-2xl border border-border bg-background text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-all"
                  disabled={isLoading}
                />
              </div>

              {/* Amount Input */}
              <div>
                <label className="block text-sm font-semibold mb-2">Amount ($)</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  placeholder="0.00"
                  className="w-full px-4 py-3 rounded-2xl border border-border bg-background text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-all"
                  disabled={isLoading}
                />
              </div>

              {/* Category Select */}
              <div>
                <label className="block text-sm font-semibold mb-2">Category</label>
                <div className="grid grid-cols-2 gap-2">
                  {categories.map((cat) => (
                    <button
                      key={cat}
                      type="button"
                      onClick={() => setCategory(cat)}
                      className={`px-4 py-2 rounded-xl font-medium transition-all ${
                        category === cat
                          ? 'bg-primary text-primary-foreground shadow-md'
                          : 'bg-secondary text-secondary-foreground border border-border hover:bg-muted'
                      }`}
                      disabled={isLoading}
                    >
                      {cat}
                    </button>
                  ))}
                </div>
              </div>

              {/* Date Input */}
              <div>
                <label className="block text-sm font-semibold mb-2">Date</label>
                <input
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className="w-full px-4 py-3 rounded-2xl border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-all"
                  disabled={isLoading}
                />
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3 pt-4">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsOpen(false)}
                  className="flex-1"
                  disabled={isLoading}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  className="flex-1 bg-gradient-to-r from-lime-300 to-lime-400 dark:from-lime-500 dark:to-lime-600 text-slate-900 dark:text-white hover:shadow-lg"
                  disabled={isLoading}
                >
                  {isLoading ? 'Adding...' : 'Add Expense'}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
