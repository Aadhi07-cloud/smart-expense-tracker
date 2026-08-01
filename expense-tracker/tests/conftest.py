"""
Test configuration and fixtures.
"""

import pytest
import json
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
from src.main import app
from src import storage


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def temp_data_file():
    """
    Create a temporary data file for testing.
    Automatically used for all tests to ensure isolation.
    """
    # Create a temporary directory and file
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "expenses.json"
        temp_file.write_text("[]")
        
        # Replace the storage module's DATA_FILE temporarily
        original_data_file = storage.DATA_FILE
        storage.DATA_FILE = temp_file
        
        yield temp_file
        
        # Restore original
        storage.DATA_FILE = original_data_file


@pytest.fixture
def sample_expense():
    """Provide sample expense data."""
    return {
        "title": "Coffee",
        "amount": 180,
        "category": "Food",
        "date": "2026-08-01"
    }


@pytest.fixture
def sample_expenses():
    """Provide multiple sample expenses."""
    return [
        {
            "title": "Coffee",
            "amount": 180,
            "category": "Food",
            "date": "2026-08-01"
        },
        {
            "title": "Uber",
            "amount": 250,
            "category": "Transportation",
            "date": "2026-08-01"
        },
        {
            "title": "Lunch",
            "amount": 450,
            "category": "Food",
            "date": "2026-08-02"
        },
        {
            "title": "Gas",
            "amount": 500,
            "category": "Transportation",
            "date": "2026-08-02"
        }
    ]
