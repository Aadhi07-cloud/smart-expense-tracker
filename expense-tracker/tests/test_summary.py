"""
Tests for summary and calculation endpoints.
"""

import pytest
from fastapi.testclient import TestClient


def test_get_summary_empty(client: TestClient):
    """Test summary when no expenses exist."""
    response = client.get("/expenses/summary")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["count"] == 0
    assert data["category"] is None


def test_get_summary_overall(client: TestClient, sample_expenses: list):
    """Test overall summary calculation."""
    # Add expenses
    for expense in sample_expenses:
        client.post("/expenses", json=expense)
    
    # Get summary
    response = client.get("/expenses/summary")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify totals
    expected_total = 180 + 250 + 450 + 500  # 1380
    assert data["total"] == expected_total
    assert data["count"] == 4
    assert data["category"] is None


def test_get_summary_by_category_food(client: TestClient, sample_expenses: list):
    """Test summary for Food category."""
    # Add expenses
    for expense in sample_expenses:
        client.post("/expenses", json=expense)
    
    # Get Food category summary
    response = client.get("/expenses/summary?category=Food")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify Food totals (Coffee: 180, Lunch: 450 = 630)
    assert data["total"] == 630
    assert data["count"] == 2
    assert data["category"] == "Food"


def test_get_summary_by_category_transportation(client: TestClient, sample_expenses: list):
    """Test summary for Transportation category."""
    # Add expenses
    for expense in sample_expenses:
        client.post("/expenses", json=expense)
    
    # Get Transportation category summary
    response = client.get("/expenses/summary?category=Transportation")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify Transportation totals (Uber: 250, Gas: 500 = 750)
    assert data["total"] == 750
    assert data["count"] == 2
    assert data["category"] == "Transportation"


def test_get_summary_nonexistent_category(client: TestClient, sample_expenses: list):
    """Test summary for non-existent category."""
    # Add expenses
    for expense in sample_expenses:
        client.post("/expenses", json=expense)
    
    # Get summary for non-existent category
    response = client.get("/expenses/summary?category=Electronics")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should return 0 for non-existent category
    assert data["total"] == 0
    assert data["count"] == 0
    assert data["category"] == "Electronics"


def test_summary_case_insensitive_category(client: TestClient, sample_expenses: list):
    """Test that category filter in summary is case-insensitive."""
    # Add expenses
    for expense in sample_expenses:
        client.post("/expenses", json=expense)
    
    # Test different cases for Food
    test_cases = ["food", "FOOD", "Food", "FoOd"]
    
    for category in test_cases:
        response = client.get(f"/expenses/summary?category={category}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 630, f"Failed for category: {category}"
        assert data["count"] == 2


def test_summary_response_structure(client: TestClient, sample_expense: dict):
    """Test response structure for summary."""
    # Add an expense
    client.post("/expenses", json=sample_expense)
    
    # Get summary
    response = client.get("/expenses/summary")
    
    assert response.status_code == 200
    data = response.json()
    
    required_fields = {"total", "count", "category"}
    assert set(data.keys()) == required_fields


def test_summary_single_expense(client: TestClient):
    """Test summary with single expense."""
    expense = {
        "title": "Single",
        "amount": 999.99,
        "category": "Test",
        "date": "2026-08-01"
    }
    
    # Add expense
    client.post("/expenses", json=expense)
    
    # Get summary
    response = client.get("/expenses/summary")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 999.99
    assert data["count"] == 1


def test_summary_precision(client: TestClient):
    """Test that summary calculations maintain decimal precision."""
    expenses = [
        {"title": "A", "amount": 10.50, "category": "Cat", "date": "2026-08-01"},
        {"title": "B", "amount": 20.30, "category": "Cat", "date": "2026-08-01"},
        {"title": "C", "amount": 15.20, "category": "Cat", "date": "2026-08-01"},
    ]
    
    # Add expenses
    for expense in expenses:
        client.post("/expenses", json=expense)
    
    # Get summary
    response = client.get("/expenses/summary")
    
    assert response.status_code == 200
    data = response.json()
    # 10.50 + 20.30 + 15.20 = 46.0
    assert data["total"] == 46.0


def test_summary_large_numbers(client: TestClient):
    """Test summary with large expense amounts."""
    expenses = [
        {"title": "A", "amount": 100000.00, "category": "Big", "date": "2026-08-01"},
        {"title": "B", "amount": 250000.00, "category": "Big", "date": "2026-08-01"},
    ]
    
    # Add expenses
    for expense in expenses:
        client.post("/expenses", json=expense)
    
    # Get summary
    response = client.get("/expenses/summary")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 350000.00
    assert data["count"] == 2


def test_summary_after_adding_same_category(client: TestClient):
    """Test that summary updates correctly when adding more expenses."""
    # Add first batch
    response1 = client.get("/expenses/summary")
    assert response1.json()["count"] == 0
    
    # Add expenses
    expense = {"title": "Test", "amount": 100, "category": "X", "date": "2026-08-01"}
    client.post("/expenses", json=expense)
    
    response2 = client.get("/expenses/summary")
    assert response2.json()["count"] == 1
    
    # Add more
    client.post("/expenses", json=expense)
    
    response3 = client.get("/expenses/summary")
    assert response3.json()["count"] == 2
    assert response3.json()["total"] == 200
