"""
Tests for retrieving expenses.
"""

import pytest
from fastapi.testclient import TestClient


def test_get_all_expenses_empty(client: TestClient):
    """Test getting expenses when none exist."""
    response = client.get("/expenses")
    
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_expenses(client: TestClient, sample_expenses: list):
    """Test retrieving all expenses."""
    # Add expenses
    for expense in sample_expenses:
        client.post("/expenses", json=expense)
    
    # Retrieve all
    response = client.get("/expenses")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
    
    # Verify data integrity
    for i, expense in enumerate(data):
        assert expense["title"] == sample_expenses[i]["title"]
        assert expense["amount"] == sample_expenses[i]["amount"]


def test_get_expenses_with_invalid_category_filter(client: TestClient, sample_expenses: list):
    """Test getting expenses with category that doesn't exist."""
    # Add expenses
    for expense in sample_expenses:
        client.post("/expenses", json=expense)
    
    # Query non-existent category
    response = client.get("/expenses?category=Electronics")
    
    assert response.status_code == 200
    assert response.json() == []


def test_filter_expenses_by_category_food(client: TestClient, sample_expenses: list):
    """Test filtering expenses by Food category."""
    # Add expenses
    for expense in sample_expenses:
        client.post("/expenses", json=expense)
    
    # Filter by Food category
    response = client.get("/expenses?category=Food")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Verify all are Food category
    for expense in data:
        assert expense["category"] == "Food"
        assert expense["title"] in ["Coffee", "Lunch"]


def test_filter_expenses_by_category_transportation(client: TestClient, sample_expenses: list):
    """Test filtering expenses by Transportation category."""
    # Add expenses
    for expense in sample_expenses:
        client.post("/expenses", json=expense)
    
    # Filter by Transportation category
    response = client.get("/expenses?category=Transportation")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Verify all are Transportation category
    for expense in data:
        assert expense["category"] == "Transportation"


def test_filter_case_insensitive(client: TestClient, sample_expenses: list):
    """Test that category filter is case-insensitive."""
    # Add expenses
    for expense in sample_expenses:
        client.post("/expenses", json=expense)
    
    # Test different cases
    test_cases = ["food", "FOOD", "Food", "FoOd"]
    
    for category in test_cases:
        response = client.get(f"/expenses?category={category}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2, f"Failed for category: {category}"


def test_get_expenses_response_structure(client: TestClient, sample_expense: dict):
    """Test response structure for get expenses."""
    # Add an expense
    client.post("/expenses", json=sample_expense)
    
    # Get expenses
    response = client.get("/expenses")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    
    expense = data[0]
    required_fields = {"id", "title", "amount", "category", "date"}
    assert set(expense.keys()) == required_fields


def test_get_expenses_preserves_order(client: TestClient):
    """Test that expenses are returned in the order they were added."""
    expenses = [
        {"title": "First", "amount": 100, "category": "A", "date": "2026-08-01"},
        {"title": "Second", "amount": 200, "category": "B", "date": "2026-08-02"},
        {"title": "Third", "amount": 300, "category": "C", "date": "2026-08-03"},
    ]
    
    # Add expenses
    for expense in expenses:
        client.post("/expenses", json=expense)
    
    # Get and verify order
    response = client.get("/expenses")
    data = response.json()
    
    for i, expense in enumerate(data):
        assert expense["title"] == expenses[i]["title"]


def test_filter_with_multiple_same_category(client: TestClient):
    """Test filtering when multiple expenses have same category."""
    expenses = [
        {"title": "Item1", "amount": 100, "category": "TestCat", "date": "2026-08-01"},
        {"title": "Item2", "amount": 200, "category": "TestCat", "date": "2026-08-02"},
        {"title": "Item3", "amount": 300, "category": "TestCat", "date": "2026-08-03"},
        {"title": "Other", "amount": 50, "category": "Different", "date": "2026-08-04"},
    ]
    
    # Add all expenses
    for expense in expenses:
        client.post("/expenses", json=expense)
    
    # Filter by TestCat
    response = client.get("/expenses?category=TestCat")
    data = response.json()
    
    assert len(data) == 3
    assert all(e["category"] == "TestCat" for e in data)


def test_api_prefix_routes_are_available(client: TestClient, sample_expense: dict):
    """Test that the frontend-friendly /api routes return the same data as /expenses."""
    client.post("/expenses", json=sample_expense)

    expenses_response = client.get("/api/expenses")
    summary_response = client.get("/api/summary")

    assert expenses_response.status_code == 200
    assert summary_response.status_code == 200
    assert expenses_response.json()[0]["title"] == sample_expense["title"]
    assert summary_response.json()["count"] == 1
