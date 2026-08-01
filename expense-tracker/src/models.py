"""
Data models for the Expense Tracker application.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Expense:
    """
    Represents an expense entry.
    
    Attributes:
        id: Unique identifier for the expense
        title: Name/description of the expense
        amount: Cost amount (must be positive)
        category: Category classification
        date: Date in YYYY-MM-DD format
    """
    id: int
    title: str
    amount: float
    category: str
    date: str

    def to_dict(self) -> dict:
        """Convert expense to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """Create expense from dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            amount=data["amount"],
            category=data["category"],
            date=data["date"]
        )
