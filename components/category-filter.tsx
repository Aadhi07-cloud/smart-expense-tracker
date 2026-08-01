'use client'

import { Button } from '@/components/ui/button'

interface CategoryFilterProps {
  categories: string[]
  selectedCategory: string | null
  onCategoryChange: (category: string | null) => void
}

export function CategoryFilter({
  categories,
  selectedCategory,
  onCategoryChange,
}: CategoryFilterProps) {
  return (
    <div className="flex gap-2 pb-4 overflow-x-auto scrollbar-hide">
      <Button
        variant={selectedCategory === null ? 'default' : 'outline'}
        size="sm"
        onClick={() => onCategoryChange(null)}
        className="whitespace-nowrap rounded-full"
      >
        All
      </Button>
      {categories.map((category) => (
        <Button
          key={category}
          variant={selectedCategory === category ? 'default' : 'outline'}
          size="sm"
          onClick={() => onCategoryChange(category === selectedCategory ? null : category)}
          className="whitespace-nowrap rounded-full"
        >
          {category}
        </Button>
      ))}
    </div>
  )
}
