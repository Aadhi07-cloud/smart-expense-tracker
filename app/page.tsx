'use client'

import { useState, useEffect } from 'react'
import { SummaryCard } from '@/components/summary-card'
import { ExpenseCard } from '@/components/expense-card'
import { AddExpenseForm } from '@/components/add-expense-form'
import { CategoryFilter } from '@/components/category-filter'
import { ExpenseListSkeleton } from '@/components/expense-skeleton'
import { Wallet, TrendingDown, Calendar } from 'lucide-react'

interface Expense {
  id: string
  title: string
  amount: number
  category: string
  date: string
}

interface Summary {
  total_expenses: number
  total_amount: number
  by_category: Record<string, number>
}

function normalizeSummary(data: Partial<Summary> & Record<string, unknown> | null | undefined): Summary {
  if (!data || typeof data !== 'object') {
    return {
      total_expenses: 0,
      total_amount: 0,
      by_category: {},
    }
  }

  const byCategory =
    data.by_category && typeof data.by_category === 'object' && !Array.isArray(data.by_category)
      ? (data.by_category as Record<string, number>)
      : {}

  return {
    total_expenses:
      typeof data.total_expenses === 'number'
        ? data.total_expenses
        : typeof data.count === 'number'
          ? data.count
          : 0,
    total_amount:
      typeof data.total_amount === 'number'
        ? data.total_amount
        : typeof data.total === 'number'
          ? data.total
          : 0,
    by_category: byCategory,
  }
}

export default function Home() {
  const [expenses, setExpenses] = useState<Expense[]>([])
  const [summary, setSummary] = useState<Summary>({
    total_expenses: 0,
    total_amount: 0,
    by_category: {},
  })
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)
  const [deleting, setDeleting] = useState<string | null>(null)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || ''

  // Fetch expenses
  const fetchExpenses = async () => {
    try {
      const params = new URLSearchParams()
      if (selectedCategory) {
        params.append('category', selectedCategory)
      }
      const response = await fetch(`${API_URL}/api/expenses?${params}`)
      if (response.ok) {
        const data = await response.json()
        setExpenses(data)
      }
    } catch (error) {
      console.error('Failed to fetch expenses:', error)
    } finally {
      setLoading(false)
    }
  }

  // Fetch summary
  const fetchSummary = async () => {
    try {
      const response = await fetch(`${API_URL}/api/summary`)
      if (response.ok) {
        const data = await response.json()
        setSummary(normalizeSummary(data))
      }
    } catch (error) {
      console.error('Failed to fetch summary:', error)
    }
  }

  useEffect(() => {
    setLoading(true)
    fetchExpenses()
    fetchSummary()
  }, [selectedCategory])

  const handleAddExpense = async (expense: {
    title: string
    amount: number
    category: string
    date: string
  }) => {
    setAdding(true)
    try {
      const response = await fetch(`${API_URL}/api/expenses`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(expense),
      })
      if (response.ok) {
        fetchExpenses()
        fetchSummary()
      }
    } catch (error) {
      console.error('Failed to add expense:', error)
    } finally {
      setAdding(false)
    }
  }

  const handleDeleteExpense = async (id: string) => {
    setDeleting(id)
    try {
      const response = await fetch(`${API_URL}/api/expenses/${id}`, {
        method: 'DELETE',
      })
      if (response.ok) {
        fetchExpenses()
        fetchSummary()
      }
    } catch (error) {
      console.error('Failed to delete expense:', error)
    } finally {
      setDeleting(null)
    }
  }

  const categories = Object.keys(summary.by_category)

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950 overflow-hidden">
      {/* Decorative blobs */}
      <div className="fixed top-0 left-0 w-96 h-96 bg-primary/10 dark:bg-primary/5 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2 pointer-events-none" />
      <div className="fixed bottom-0 right-0 w-96 h-96 bg-accent/10 dark:bg-accent/5 rounded-full blur-3xl translate-x-1/2 translate-y-1/2 pointer-events-none" />

      <div className="relative z-10 max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8 animate-slide-down">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-3 bg-gradient-to-br from-lime-300 to-lime-400 dark:from-lime-500 dark:to-lime-600 rounded-xl">
              <Wallet className="w-6 h-6 text-slate-900 dark:text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 dark:from-white dark:to-slate-300 bg-clip-text text-transparent">
              Expense Tracker
            </h1>
          </div>
          <p className="text-muted-foreground mt-2">Track and manage your spending effortlessly</p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <SummaryCard
            title="Total Spending"
            amount={summary.total_amount}
            gradient="lime"
            icon={<TrendingDown className="w-5 h-5" />}
          />
          <SummaryCard
            title="This Month"
            amount={summary.total_amount}
            gradient="orange"
            icon={<Calendar className="w-5 h-5" />}
          />
          <SummaryCard
            title="Transactions"
            amount={summary.total_expenses}
            currency=""
            gradient="blue"
            icon={<Wallet className="w-5 h-5" />}
          />
        </div>

        {/* Filter Section */}
        {categories.length > 0 && (
          <div className="mb-6">
            <CategoryFilter
              categories={categories}
              selectedCategory={selectedCategory}
              onCategoryChange={setSelectedCategory}
            />
          </div>
        )}

        {/* Expenses List */}
        <div className="glass rounded-3xl p-6">
          <h2 className="text-2xl font-bold mb-4">Recent Expenses</h2>

          {loading ? (
            <ExpenseListSkeleton />
          ) : expenses.length === 0 ? (
            <div className="text-center py-12">
              <TrendingDown className="w-12 h-12 text-muted-foreground mx-auto mb-4 opacity-50" />
              <p className="text-muted-foreground mb-2">No expenses yet</p>
              <p className="text-sm text-muted-foreground">
                {selectedCategory
                  ? `Add your first ${selectedCategory.toLowerCase()} expense`
                  : 'Add your first expense to get started'}
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {expenses.map((expense) => (
                <ExpenseCard
                  key={expense.id}
                  {...expense}
                  onDelete={handleDeleteExpense}
                  isDeleting={deleting === expense.id}
                />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Add Expense Button */}
      <AddExpenseForm onSubmit={handleAddExpense} isLoading={adding} />
    </main>
  )
}
