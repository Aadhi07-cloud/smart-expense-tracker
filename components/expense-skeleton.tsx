'use client'

export function ExpenseSkeleton() {
  return (
    <div className="glass p-4 rounded-2xl">
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="h-5 bg-muted rounded-lg w-24 mb-2 animate-pulse" />
            <div className="h-4 bg-muted rounded-lg w-32 animate-pulse" />
          </div>
          <div className="h-8 bg-muted rounded-lg w-24 animate-pulse" />
        </div>
      </div>
    </div>
  )
}

export function ExpenseListSkeleton() {
  return (
    <div className="space-y-3">
      {Array.from({ length: 5 }).map((_, i) => (
        <ExpenseSkeleton key={i} />
      ))}
    </div>
  )
}
