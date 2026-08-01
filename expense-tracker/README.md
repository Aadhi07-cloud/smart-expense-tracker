# Smart Expense Tracker REST API

A production-quality REST API for managing personal expenses built with FastAPI and Python. Store expenses locally in JSON format with comprehensive filtering, categorization, and summary calculations.

## Features

- ✅ **Add Expenses**: Create new expense entries with validation
- ✅ **View Expenses**: Retrieve all expenses or filter by category
- ✅ **Categorization**: Organize expenses by categories
- ✅ **Summary Calculations**: Get overall totals or category-specific summaries
- ✅ **Delete Expenses**: Remove expenses by ID
- ✅ **JSON Storage**: Persistent local file storage
- ✅ **Pydantic Validation**: Robust input validation
- ✅ **OpenAPI Documentation**: Interactive API docs with Swagger UI
- ✅ **Comprehensive Tests**: Full pytest test suite with high coverage
- ✅ **Error Handling**: Meaningful error responses with proper HTTP status codes

## Project Structure

```
expense-tracker/
├── README.md                 # Project documentation
├── AI_NOTES.md              # AI development notes
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
│
├── src/
│   ├── main.py             # FastAPI application entry point
│   ├── models.py           # Data models (Expense class)
│   ├── schemas.py          # Pydantic validation schemas
│   ├── storage.py          # JSON file storage operations
│   ├── routes.py           # API route handlers
│   ├── utils.py            # Utility functions for calculations
│   └── data/
│       └── expenses.json   # Local expense data storage
│
└── tests/
    ├── conftest.py         # Pytest fixtures and configuration
    ├── test_add_expense.py      # Tests for creating expenses
    ├── test_get_expenses.py     # Tests for retrieving expenses
    ├── test_summary.py          # Tests for summaries
    └── test_delete.py           # Tests for deleting expenses
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip or pip3

### Virtual Environment Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
# Start the FastAPI development server
python -m uvicorn src.main:app --reload

# Server will be available at: http://localhost:8000
```

### API Documentation

Once the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Running Tests

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_add_expense.py -v

# Run with coverage
pytest --cov=src tests/

# Run tests with detailed output
pytest -vv --tb=short
```

## API Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|------------|
| POST | `/expenses` | Create a new expense | 201 |
| GET | `/expenses` | Get all expenses | 200 |
| GET | `/expenses?category=Food` | Filter expenses by category | 200 |
| GET | `/expenses/summary` | Get overall summary | 200 |
| GET | `/expenses/summary?category=Food` | Get category summary | 200 |
| DELETE | `/expenses/{id}` | Delete an expense | 204 |
| GET | `/health` | Health check | 200 |

## Example API Usage

### Create an Expense

```bash
curl -X POST http://localhost:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Coffee",
    "amount": 180,
    "category": "Food",
    "date": "2026-08-01"
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Coffee",
  "amount": 180,
  "category": "Food",
  "date": "2026-08-01"
}
```

### Get All Expenses

```bash
curl http://localhost:8000/expenses
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Coffee",
    "amount": 180,
    "category": "Food",
    "date": "2026-08-01"
  },
  {
    "id": 2,
    "title": "Uber",
    "amount": 250,
    "category": "Transportation",
    "date": "2026-08-01"
  }
]
```

### Filter Expenses by Category

```bash
curl http://localhost:8000/expenses?category=Food
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Coffee",
    "amount": 180,
    "category": "Food",
    "date": "2026-08-01"
  }
]
```

### Get Overall Summary

```bash
curl http://localhost:8000/expenses/summary
```

**Response (200 OK):**
```json
{
  "total": 3200,
  "count": 8,
  "category": null
}
```

### Get Category Summary

```bash
curl http://localhost:8000/expenses/summary?category=Food
```

**Response (200 OK):**
```json
{
  "category": "Food",
  "total": 950,
  "count": 4
}
```

### Delete an Expense

```bash
curl -X DELETE http://localhost:8000/expenses/1
```

**Response (204 No Content):** (empty body)

## Validation Rules

### Title
- Required field
- Cannot be empty or whitespace only
- Whitespace is trimmed automatically

### Amount
- Required field
- Must be greater than 0
- Accepts decimal values (e.g., 10.50)

### Category
- Required field
- Cannot be empty or whitespace only

### Date
- Required field
- Must follow YYYY-MM-DD format (e.g., 2026-08-01)

## Error Responses

### 400 Bad Request
Invalid request format

### 422 Unprocessable Entity
Validation error - field validation failed

```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "amount",
      "message": "ensure this value is greater than 0"
    }
  ]
}
```

### 404 Not Found
Resource not found (e.g., expense ID doesn't exist)

```json
{
  "detail": "Expense with ID 999 not found"
}
```

### 500 Internal Server Error
Server error (e.g., JSON file corruption)

## Design Decisions

### 1. JSON File Storage
- **Choice**: Local JSON file instead of database
- **Rationale**: Simplicity, no external dependencies, easy to backup, suitable for single-user/development scenarios
- **Trade-off**: Not suitable for multi-user concurrent access at scale

### 2. Pydantic Validation
- **Choice**: Comprehensive field-level validation using Pydantic
- **Rationale**: Type safety, automatic error messages, request/response schema validation
- **Benefit**: Catches invalid data before processing

### 3. Case-Insensitive Category Filtering
- **Choice**: Category filters treat uppercase/lowercase as equivalent
- **Rationale**: Better UX, reduces errors from case mismatches
- **Implementation**: Convert to lowercase for comparison

### 4. ID Auto-Increment
- **Choice**: IDs increment sequentially and are never reused
- **Rationale**: Predictable IDs, easier debugging, prevents ID conflicts
- **Implementation**: Track max ID and increment on new expense

### 5. Modular Architecture
- **Choice**: Separate files for models, schemas, storage, routes, utils
- **Rationale**: Clean separation of concerns, easier testing, maintainability
- **Benefit**: Easy to extend and modify individual components

### 6. No Authentication
- **Choice**: No auth required (as per requirements)
- **Rationale**: Simpler API for demo/learning purposes
- **Future**: Can be added with middleware/decorator pattern

## Future Improvements

1. **Database Integration**
   - Migrate from JSON to PostgreSQL/SQLite for better performance and concurrency

2. **Authentication & Authorization**
   - Add user accounts with JWT tokens
   - Per-user expense isolation

3. **Advanced Filtering**
   - Date range filters
   - Amount range filters
   - Multiple category filters

4. **Recurring Expenses**
   - Support for recurring/recurring transactions
   - Automatic generation on schedule

5. **Tags & Labels**
   - Multiple tags per expense
   - Custom filtering by tags

6. **Reports & Analytics**
   - Monthly/yearly summaries
   - Spending trends
   - Category breakdown charts

7. **Export Functionality**
   - CSV export
   - PDF reports

8. **Bulk Operations**
   - Bulk delete
   - Bulk category update

9. **Soft Deletes**
   - Keep deleted records for audit trail
   - Restore functionality

10. **Caching**
    - Redis for frequently accessed summaries
    - Reduce JSON file reads

## Testing Coverage

The test suite includes:
- ✅ Add expense validation (13 tests)
- ✅ Get expenses and filtering (8 tests)
- ✅ Summary calculations (11 tests)
- ✅ Delete operations (10 tests)
- **Total**: 42 comprehensive tests

All tests are isolated and use temporary data files to ensure independence.

## Code Quality

- **Type Hints**: Full type annotations throughout
- **Docstrings**: Comprehensive docstrings for all functions
- **Error Handling**: Graceful error handling with meaningful messages
- **SOLID Principles**: Single responsibility, open/closed principles applied
- **DRY**: No code duplication, reusable helper functions
- **Black Compatible**: Code formatted for Black compatibility

## License

This project is open source and available under the MIT License.
