"""
Utility functions for calculations and common operations.
"""

from typing import List
from src.models import Expense


def calculate_total(expenses: List[Expense]) -> float:
    """
    Calculate the total of all expenses.
    
    Args:
        expenses: List of expenses
        
    Returns:
        Sum of all expense amounts
    """
    return sum(expense.amount for expense in expenses)


def calculate_count(expenses: List[Expense]) -> int:
    """
    Count the number of expenses.
    
    Args:
        expenses: List of expenses
        
    Returns:
        Number of expenses
    """
    return len(expenses)


def calculate_category_total(expenses: List[Expense], category: str) -> float:
    """
    Calculate total for a specific category.
    
    Args:
        expenses: List of expenses
        category: Category to calculate for
        
    Returns:
        Sum of expense amounts in the category
    """
    category_expenses = [
        expense for expense in expenses
        if expense.category.lower() == category.lower()
    ]
    return calculate_total(category_expenses)


def calculate_category_count(expenses: List[Expense], category: str) -> int:
    """
    Count expenses in a specific category.
    
    Args:
        expenses: List of expenses
        category: Category to count
        
    Returns:
        Number of expenses in the category
    """
    category_expenses = [
        expense for expense in expenses
        if expense.category.lower() == category.lower()
    ]
    return calculate_count(category_expenses)
