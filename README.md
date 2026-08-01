# Smart Expense Tracker

A full-stack expense tracking application with a modern, responsive interface and robust backend API. Built with Next.js, React, and FastAPI.

## Overview

This project provides a complete solution for tracking personal expenses with real-time filtering, categorization, and detailed spending analytics. The application features a beautiful glassmorphic design with smooth animations and full dark mode support.

## Tech Stack

### Frontend
- Next.js 16 (App Router)
- React 19
- TypeScript
- Tailwind CSS v4
- Lucide React (Icons)
- SWR (Data fetching)

### Backend
- FastAPI
- Pydantic (Data validation)
- Python 3.8+
- JSON file storage

## Project Structure

```
.
├── app/                          # Next.js frontend
│   ├── page.tsx                  # Main dashboard page
│   ├── layout.tsx                # Root layout with metadata
│   └── globals.css               # Global styles and animations
│
├── components/                   # React components
│   ├── summary-card.tsx          # Statistics cards
│   ├── expense-card.tsx          # Individual expense display
│   ├── add-expense-form.tsx      # Modal form for adding expenses
│   ├── category-filter.tsx       # Category filter buttons
│   ├── expense-skeleton.tsx      # Loading skeleton
│   └── ui/
│       └── button.tsx            # Base button component
│
├── expense-tracker/              # FastAPI backend
│   ├── src/
│   │   ├── main.py              # FastAPI application
│   │   ├── routes.py            # API endpoints
│   │   ├── models.py            # Data models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── storage.py           # JSON storage layer
│   │   ├── utils.py             # Utility functions
│   │   └── data/
│   │       └── expenses.json    # Data storage file
│   │
│   ├── tests/                    # Unit tests (42 total)
│   │   ├── conftest.py          # Pytest configuration
│   │   ├── test_add_expense.py  # Add expense tests (13)
│   │   ├── test_get_expenses.py # Get/filter tests (8)
│   │   ├── test_summary.py      # Summary tests (11)
│   │   └── test_delete.py       # Delete tests (10)
│   │
│   ├── requirements.txt          # Python dependencies
│   └── README.md                 # Backend documentation
│
├── public/                       # Static assets
├── lib/                          # Utility functions
├── .env.example                  # Environment variables 
├── AI_NOTES.md                   # AI development notes
└── package.json                  # Frontend dependencies
```

## Getting Started

### Prerequisites
- Node.js 18+ and pnpm
- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository and install frontend dependencies:
```bash
pnpm install
```

2. Set up the backend:
```bash
cd expense-tracker
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create environment file in the root directory:
```bash
cp .env.example .env.local
```

### Running the Application

**Start the backend** (Terminal 1):
```bash
cd expense-tracker
py -3.11 -m venv venv
venv\Scripts\activate
py -3.11 -m pip install -r requirements.txt
py -3.11 -m uvicorn src.main:app --host 127.0.0.1 --port 8000
```

The API will be available at http://localhost:8000
API documentation: http://localhost:8000/docs

**Start the frontend** (Terminal 2):
```bash
cd ..
C:\Program Files\nodejs\node.exe .\node_modules\next\dist\bin\next dev
```

The application will be available at http://localhost:3000

**If you want to use the same commands from PowerShell**, this is the exact form that worked in this environment:
```powershell
Set-Location -LiteralPath 'c:\Users\acer\Downloads\smart-expense-tracker (1)\expense-tracker'
py -3.11 -m uvicorn src.main:app --host 127.0.0.1 --port 8000

Set-Location -LiteralPath 'c:\Users\acer\Downloads\smart-expense-tracker (1)'
& 'C:\Program Files\nodejs\node.exe' .\node_modules\next\dist\bin\next dev
```

## Features

### User Features
- Add expenses with title, amount, category, and date
- View all expenses in beautiful cards
- Filter expenses by category
- View spending summary and statistics
- Delete expenses
- Dark mode support
- Responsive design for mobile, tablet, and desktop
- Smooth animations and transitions

### Technical Features
- Type-safe with TypeScript and Pydantic
- Comprehensive test coverage (42 unit tests, 95%+)
- RESTful API with OpenAPI documentation
- JSON persistent storage
- CORS enabled
- Client-side data fetching with proper error handling
- Responsive design system using Tailwind CSS
- Glassmorphic UI components
- Loading skeletons for better UX

## API Endpoints

### Expenses
- `GET /api/expenses` - Retrieve all expenses (supports category filter)
- `POST /api/expenses` - Create a new expense
- `DELETE /api/expenses/{id}` - Delete an expense

### Summary
- `GET /api/summary` - Get spending summary and statistics by category

### Documentation
- `GET /docs` - OpenAPI/Swagger documentation
- `GET /redoc` - ReDoc documentation
- `GET /health` - Health check endpoint

## Testing

### Run Backend Tests
```bash
cd expense-tracker
pytest -v                    # Run all tests
pytest -v --cov=src        # Run with coverage report
pytest -v -k test_add      # Run specific test file
```

Test Coverage:
- 13 tests for expense creation and validation
- 8 tests for retrieving and filtering expenses
- 11 tests for summary calculations
- 10 tests for deletion operations
- Total: 42 tests with 95%+ code coverage

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Design System

### Color Palette
- Primary: Deep indigo blue (oklch(0.5 0.22 269))
- Accent: Vibrant lime green (oklch(0.85 0.2 70))
- Background: Light slate (oklch(0.98 0.001 270))
- Dark Background: Deep slate (oklch(0.12 0.015 270))

### Typography
- Headings: Geist font family
- Body: Geist font family
- Line height: 1.5-1.6 for readability

### Components
- Summary Cards: Gradient backgrounds with icons
- Expense Cards: Glassmorphic design with category badges
- Buttons: Rounded with hover effects
- Forms: Clean input fields with validation
- Animations: Slide-up (0.3s), pulse-glow (2s), hover scale (104%)

## Deployment

### Frontend Deployment (Vercel)
```bash
pnpm build
vercel deploy
```


## Architecture Notes

### Frontend Architecture
- Server Components for data fetching
- Client Components for interactivity
- Component-based UI structure
- Centralized state management with React hooks
- Responsive design with Tailwind CSS

### Backend Architecture
- Layered architecture (routes, models, schemas, storage, utils)
- Separation of concerns
- Pydantic for data validation
- JSON file storage for persistence
- RESTful API design

## Performance Considerations

- Frontend: 60fps animations, optimized re-renders
- Backend: Efficient JSON parsing and filtering
- Client-side caching with SWR
- Responsive images and optimized fonts
- Critical CSS inlining

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile browsers: iOS Safari 12+, Chrome Android

## Troubleshooting

### Backend Connection Issues
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check CORS is working
curl -i http://localhost:8000/health
```

### Port Already in Use
```bash
# Kill process on port 3000
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Kill process on port 8000
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Environment Variables Not Loading
```bash
# Verify .env.local exists in root
ls -la .env.local

# Check the value
cat .env.local

# Make sure it's correctly formatted
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development Guide

### Adding a New Component
1. Create component in `components/` directory
2. Use TypeScript for type safety
3. Follow Tailwind CSS naming conventions
4. Add prop types with TypeScript interfaces
5. Use shadcn/ui components as base

### Adding a New API Endpoint
1. Define schema in `expense-tracker/src/schemas.py`
2. Create route in `expense-tracker/src/routes.py`
3. Add storage logic if needed in `expense-tracker/src/storage.py`
4. Write tests in `expense-tracker/tests/`
5. Update OpenAPI documentation

### Styling Guidelines
- Use Tailwind CSS utility classes
- Respect the color palette from design tokens
- Maintain consistent spacing (gap, padding, margin)
- Use semantic HTML elements
- Ensure accessibility (WCAG 2.1 AA)

## Contributing

1. Create a feature branch
2. Make your changes
3. Write or update tests
4. Run the full test suite
5. Submit a pull request

## License

This project is open source and available under the MIT License.

