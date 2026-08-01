from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.routes import router, api_router

# Create FastAPI application
app = FastAPI(
    title="Smart Expense Tracker",
    description="A REST API for tracking and managing expenses",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# -------------------------------
# CORS Configuration
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000",
        "http://192.168.1.248:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)
app.include_router(api_router)


# -------------------------------
# Exception Handler
# -------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    errors = []

    for error in exc.errors():
        errors.append(
            {
                "field": ".".join(str(x) for x in error["loc"][1:]),
                "message": error["msg"],
            }
        )

    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": errors,
        },
    )


# -------------------------------
# Health Check
# -------------------------------
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


# -------------------------------
# Root Endpoint
# -------------------------------
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Smart Expense Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


# -------------------------------
# Run Application
# -------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )