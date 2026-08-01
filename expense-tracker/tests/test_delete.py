"""
Tests for deleting expenses.
"""

import pytest
from fastapi.testclient import TestClient


def test_delete_expense_success(client: TestClient, sample_expense: dict):
    """Test successfully deleting an expense."""
    # Add expense
    add_response = client.post("/expenses", json=sample_expense)
    expense_id = add_response.json()["id"]
    
    # Delete expense
    delete_response = client.delete(f"/expenses/{expense_id}")
    
    assert delete_response.status_code == 204


def test_delete_removes_expense(client: TestClient, sample_expense: dict):
    """Test that deleted expense is no longer retrievable."""
    # Add expense
    add_response = client.post("/expenses", json=sample_expense)
    expense_id = add_response.json()["id"]
    
    # Verify it exists
    get_response = client.get("/expenses")
    assert len(get_response.json()) == 1
    
    # Delete expense
    client.delete(f"/expenses/{expense_id}")
    
    # Verify it's gone
    get_response = client.get("/expenses")
    assert len(get_response.json()) == 0


def test_delete_nonexistent_expense(client: TestClient):
    """Test deleting an expense that doesn't exist."""
    response = client.delete("/expenses/999")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_specific_expense_from_multiple(client: TestClient, sample_expenses: list):
    """Test deleting a specific expense when multiple exist."""
    # Add expenses
    ids = []
    for expense in sample_expenses:
        response = client.post("/expenses", json=expense)
        ids.append(response.json()["id"])
    
    # Delete the second expense
    delete_response = client.delete(f"/expenses/{ids[1]}")
    assert delete_response.status_code == 204
    
    # Verify correct one was deleted
    get_response = client.get("/expenses")
    remaining = get_response.json()
    assert len(remaining) == 3
    
    # Verify deleted expense is gone and others remain
    remaining_ids = [e["id"] for e in remaining]
    assert ids[1] not in remaining_ids
    assert ids[0] in remaining_ids
    assert ids[2] in remaining_ids
    assert ids[3] in remaining_ids


def test_delete_updates_summary(client: TestClient, sample_expenses: list):
    """Test that deleting an expense updates the summary."""
    # Add expenses
    for expense in sample_expenses:
        client.post("/expenses", json=expense)
    
    # Get initial summary
    summary_before = client.get("/expenses/summary").json()
    initial_total = summary_before["total"]
    initial_count = summary_before["count"]
    
    # Get first expense and delete it
    expenses = client.get("/expenses").json()
    first_id = expenses[0]["id"]
    first_amount = expenses[0]["amount"]
    
    client.delete(f"/expenses/{first_id}")
    
    # Get updated summary
    summary_after = client.get("/expenses/summary").json()
    
    assert summary_after["count"] == initial_count - 1
    assert summary_after["total"] == initial_total - first_amount


def test_delete_updates_category_summary(client: TestClient, sample_expenses: list):
    """Test that deleting an expense updates category summary."""
    # Add expenses
    for expense in sample_expenses:
        client.post("/expenses", json=expense)
    
    # Get initial Food summary
    food_summary_before = client.get("/expenses/summary?category=Food").json()
    
    # Find and delete a Food expense
    expenses = client.get("/expenses?category=Food").json()
    to_delete = expenses[0]
    
    client.delete(f"/expenses/{to_delete['id']}")
    
    # Get updated Food summary
    food_summary_after = client.get("/expenses/summary?category=Food").json()
    
    assert food_summary_after["count"] == food_summary_before["count"] - 1
    assert food_summary_after["total"] == food_summary_before["total"] - to_delete["amount"]


def test_delete_first_id_preservation(client: TestClient):
    """Test that IDs are not reused after deletion."""
    # Add three expenses
    expense = {"title": "Test", "amount": 100, "category": "Test", "date": "2026-08-01"}
    
    id1 = client.post("/expenses", json=expense).json()["id"]
    id2 = client.post("/expenses", json=expense).json()["id"]
    id3 = client.post("/expenses", json=expense).json()["id"]
    
    # Delete first one
    client.delete(f"/expenses/{id1}")
    
    # Add new expense - should get id4, not id1
    id4 = client.post("/expenses", json=expense).json()["id"]
    
    assert id4 == 4
    assert id4 != id1


def test_delete_already_deleted_expense(client: TestClient, sample_expense: dict):
    """Test deleting an expense that was already deleted."""
    # Add and delete an expense
    response = client.post("/expenses", json=sample_expense)
    expense_id = response.json()["id"]
    
    client.delete(f"/expenses/{expense_id}")
    
    # Try to delete again
    response = client.delete(f"/expenses/{expense_id}")
    
    assert response.status_code == 404


def test_delete_with_negative_id(client: TestClient):
    """Test deleting with negative ID."""
    response = client.delete("/expenses/-1")
    
    assert response.status_code == 404


def test_delete_with_zero_id(client: TestClient):
    """Test deleting with zero ID."""
    response = client.delete("/expenses/0")
    
    assert response.status_code == 404


def test_delete_returns_no_content(client: TestClient, sample_expense: dict):
    """Test that delete returns 204 with no content."""
    # Add expense
    response = client.post("/expenses", json=sample_expense)
    expense_id = response.json()["id"]
    
    # Delete expense
    delete_response = client.delete(f"/expenses/{expense_id}")
    
    assert delete_response.status_code == 204
    # Response should be empty for 204
    assert delete_response.text == ""


def test_delete_all_expenses_sequentially(client: TestClient, sample_expenses: list):
    """Test deleting all expenses one by one."""
    # Add all expenses
    ids = []
    for expense in sample_expenses:
        response = client.post("/expenses", json=expense)
        ids.append(response.json()["id"])
    
    # Delete each one
    for expense_id in ids:
        response = client.delete(f"/expenses/{expense_id}")
        assert response.status_code == 204
    
    # Verify all are gone
    response = client.get("/expenses")
    assert len(response.json()) == 0
