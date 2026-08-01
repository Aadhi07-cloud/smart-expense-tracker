"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class ExpenseCreate(BaseModel):
    """Schema for creating a new expense."""
    
    title: str = Field(..., min_length=1, description="Expense title")
    amount: float = Field(..., gt=0, description="Expense amount (must be positive)")
    category: str = Field(..., min_length=1, description="Expense category")
    date: str = Field(..., description="Expense date in YYYY-MM-DD format")

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Ensure title is not empty or whitespace only."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("category")
    @classmethod
    def category_not_empty(cls, v: str) -> str:
        """Ensure category is not empty or whitespace only."""
        if not v or not v.strip():
            raise ValueError("Category cannot be empty")
        return v.strip()

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Validate date follows YYYY-MM-DD format."""
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            raise ValueError("Date must be in YYYY-MM-DD format")
        return v


class ExpenseResponse(BaseModel):
    """Schema for expense response."""
    
    id: int
    title: str
    amount: float
    category: str
    date: str

    class Config:
        """Pydantic config."""
        from_attributes = True


class SummaryResponse(BaseModel):
    """Schema for summary response (overall or by category)."""
    
    total: float
    count: int
    category: Optional[str] = None


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    
    detail: str
    status_code: int
