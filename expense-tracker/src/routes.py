

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from src.models import Expense
from src.schemas import ExpenseCreate, ExpenseResponse, SummaryResponse
from src.storage import (
    load_expenses,
    save_expenses,
    generate_next_id,
    find_expense_by_id,
    filter_by_category,
)
from src.utils import (
    calculate_total,
    calculate_count,
    calculate_category_total,
    calculate_category_count,
)

router = APIRouter(prefix="/expenses", tags=["expenses"])
api_router = APIRouter(prefix="/api", tags=["expenses"])


def _create_expense(expense_data: ExpenseCreate) -> ExpenseResponse:
    try:
        expenses = load_expenses()
        next_id = generate_next_id(expenses)

        new_expense = Expense(
            id=next_id,
            title=expense_data.title,
            amount=expense_data.amount,
            category=expense_data.category,
            date=expense_data.date,
        )

        expenses.append(new_expense)
        save_expenses(expenses)

        return ExpenseResponse(**new_expense.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


def _get_expenses(category: Optional[str] = None) -> List[ExpenseResponse]:
    try:
        expenses = load_expenses()

        if category:
            expenses = filter_by_category(expenses, category)

        return [ExpenseResponse(**expense.to_dict()) for expense in expenses]
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


def _get_summary(category: Optional[str] = None) -> SummaryResponse:
    try:
        expenses = load_expenses()

        if category:
            total = calculate_category_total(expenses, category)
            count = calculate_category_count(expenses, category)
            return SummaryResponse(total=total, count=count, category=category)

        total = calculate_total(expenses)
        count = calculate_count(expenses)
        return SummaryResponse(total=total, count=count)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


def _delete_expense(expense_id: int) -> None:
    try:
        expenses = load_expenses()
        expense = find_expense_by_id(expenses, expense_id)

        if not expense:
            raise HTTPException(
                status_code=404,
                detail=f"Expense with ID {expense_id} not found",
            )

        expenses = [e for e in expenses if e.id != expense_id]
        save_expenses(expenses)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", status_code=201, response_model=ExpenseResponse)
@api_router.post("/expenses", status_code=201, response_model=ExpenseResponse)
def create_expense(expense_data: ExpenseCreate) -> ExpenseResponse:
    """Create a new expense."""
    return _create_expense(expense_data)


@router.get("", response_model=List[ExpenseResponse])
@api_router.get("/expenses", response_model=List[ExpenseResponse])
def get_expenses(category: Optional[str] = Query(None)) -> List[ExpenseResponse]:
    """Get all expenses or filter by category."""
    return _get_expenses(category)


@router.get("/summary", response_model=SummaryResponse)
@api_router.get("/summary", response_model=SummaryResponse)
def get_summary(category: Optional[str] = Query(None)) -> SummaryResponse:
    """Get summary of expenses."""
    return _get_summary(category)


@router.delete("/{expense_id}", status_code=204)
@api_router.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int) -> None:
    """Delete an expense by ID."""
    _delete_expense(expense_id)
