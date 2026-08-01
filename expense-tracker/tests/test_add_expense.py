"""
Tests for creating expenses.
"""

import pytest
from fastapi.testclient import TestClient


def test_add_expense_success(client: TestClient, sample_expense: dict):
    """Test successfully adding an expense."""
    response = client.post("/expenses", json=sample_expense)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_expense["title"]
    assert data["amount"] == sample_expense["amount"]
    assert data["category"] == sample_expense["category"]
    assert data["date"] == sample_expense["date"]
    assert "id" in data
    assert data["id"] == 1


def test_add_multiple_expenses(client: TestClient, sample_expenses: list):
    """Test adding multiple expenses and verifying IDs increment."""
    ids = []
    
    for expense in sample_expenses:
        response = client.post("/expenses", json=expense)
        assert response.status_code == 201
        data = response.json()
        ids.append(data["id"])
    
    # Verify IDs are sequential
    assert ids == [1, 2, 3, 4]


def test_add_expense_missing_title(client: TestClient):
    """Test validation fails when title is missing."""
    data = {
        "amount": 100,
        "category": "Food",
        "date": "2026-08-01"
    }
    response = client.post("/expenses", json=data)
    
    assert response.status_code == 422


def test_add_expense_empty_title(client: TestClient):
    """Test validation fails when title is empty."""
    data = {
        "title": "",
        "amount": 100,
        "category": "Food",
        "date": "2026-08-01"
    }
    response = client.post("/expenses", json=data)
    
    assert response.status_code == 422


def test_add_expense_whitespace_only_title(client: TestClient):
    """Test validation fails when title is whitespace only."""
    data = {
        "title": "   ",
        "amount": 100,
        "category": "Food",
        "date": "2026-08-01"
    }
    response = client.post("/expenses", json=data)
    
    assert response.status_code == 422


def test_add_expense_missing_amount(client: TestClient):
    """Test validation fails when amount is missing."""
    data = {
        "title": "Coffee",
        "category": "Food",
        "date": "2026-08-01"
    }
    response = client.post("/expenses", json=data)
    
    assert response.status_code == 422


def test_add_expense_negative_amount(client: TestClient):
    """Test validation fails when amount is negative."""
    data = {
        "title": "Coffee",
        "amount": -50,
        "category": "Food",
        "date": "2026-08-01"
    }
    response = client.post("/expenses", json=data)
    
    assert response.status_code == 422


def test_add_expense_zero_amount(client: TestClient):
    """Test validation fails when amount is zero."""
    data = {
        "title": "Coffee",
        "amount": 0,
        "category": "Food",
        "date": "2026-08-01"
    }
    response = client.post("/expenses", json=data)
    
    assert response.status_code == 422


def test_add_expense_missing_category(client: TestClient):
    """Test validation fails when category is missing."""
    data = {
        "title": "Coffee",
        "amount": 100,
        "date": "2026-08-01"
    }
    response = client.post("/expenses", json=data)
    
    assert response.status_code == 422


def test_add_expense_empty_category(client: TestClient):
    """Test validation fails when category is empty."""
    data = {
        "title": "Coffee",
        "amount": 100,
        "category": "",
        "date": "2026-08-01"
    }
    response = client.post("/expenses", json=data)
    
    assert response.status_code == 422


def test_add_expense_missing_date(client: TestClient):
    """Test validation fails when date is missing."""
    data = {
        "title": "Coffee",
        "amount": 100,
        "category": "Food"
    }
    response = client.post("/expenses", json=data)
    
    assert response.status_code == 422


def test_add_expense_invalid_date_format(client: TestClient):
    """Test validation fails with invalid date format."""
    invalid_dates = [
        "01-08-2026",
        "2026/08/01",
        "08-01-2026",
        "2026-8-1",
        "invalid"
    ]
    
    for invalid_date in invalid_dates:
        data = {
            "title": "Coffee",
            "amount": 100,
            "category": "Food",
            "date": invalid_date
        }
        response = client.post("/expenses", json=data)
        assert response.status_code == 422, f"Expected validation error for date: {invalid_date}"


def test_add_expense_response_structure(client: TestClient, sample_expense: dict):
    """Test response has correct structure."""
    response = client.post("/expenses", json=sample_expense)
    
    assert response.status_code == 201
    data = response.json()
    
    required_fields = {"id", "title", "amount", "category", "date"}
    assert set(data.keys()) == required_fields


def test_add_expense_title_trimmed(client: TestClient):
    """Test that whitespace is trimmed from title."""
    data = {
        "title": "  Coffee  ",
        "amount": 100,
        "category": "Food",
        "date": "2026-08-01"
    }
    response = client.post("/expenses", json=data)
    
    assert response.status_code == 201
    assert response.json()["title"] == "Coffee"
