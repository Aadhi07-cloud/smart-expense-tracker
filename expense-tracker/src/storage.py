"""
JSON file storage operations for expenses.
"""

import json
import os
from typing import List
from pathlib import Path
from src.models import Expense


# Determine the data file path
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "expenses.json"


def load_expenses() -> List[Expense]:
    """
    Load all expenses from the JSON file.
    
    Returns:
        List of Expense objects
        
    Raises:
        ValueError: If JSON file is corrupted
    """
    if not DATA_FILE.exists():
        return []
    
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return [Expense.from_dict(item) for item in data]
    except json.JSONDecodeError as e:
        raise ValueError(f"Corrupted JSON file: {e}")
    except Exception as e:
        raise ValueError(f"Error reading expenses file: {e}")


def save_expenses(expenses: List[Expense]) -> None:
    """
    Save expenses to the JSON file.
    
    Args:
        expenses: List of Expense objects to save
        
    Raises:
        ValueError: If unable to write to file
    """
    try:
        with open(DATA_FILE, "w") as f:
            data = [expense.to_dict() for expense in expenses]
            json.dump(data, f, indent=2)
    except Exception as e:
        raise ValueError(f"Error saving expenses: {e}")


def generate_next_id(expenses: List[Expense]) -> int:
    """
    Generate the next available ID for a new expense.
    
    Args:
        expenses: List of existing expenses
        
    Returns:
        Next available ID (one higher than the max ID, or 1 if list is empty)
    """
    if not expenses:
        return 1
    return max(expense.id for expense in expenses) + 1


def find_expense_by_id(expenses: List[Expense], expense_id: int) -> Expense | None:
    """
    Find an expense by its ID.
    
    Args:
        expenses: List of expenses to search
        expense_id: ID to search for
        
    Returns:
        Expense object if found, None otherwise
    """
    return next((expense for expense in expenses if expense.id == expense_id), None)


def filter_by_category(expenses: List[Expense], category: str) -> List[Expense]:
    """
    Filter expenses by category.
    
    Args:
        expenses: List of expenses to filter
        category: Category to filter by
        
    Returns:
        List of expenses matching the category
    """
    return [expense for expense in expenses if expense.category.lower() == category.lower()]
