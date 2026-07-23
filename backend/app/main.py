from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.core.config import settings
from app.core.exceptions import AuditOSError

app = FastAPI(
    title=settings.APP_NAME,
    description="Autonomous Enterprise Audit & Compliance Intelligence Platform",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AuditOSError)
def handle_domain_error(request: Request, exc: AuditOSError):
    """
    Every domain-level error raised by a service maps to a clean JSON
    response here, so routers never need repetitive try/except blocks.
    """
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/api/health", tags=["System"])
def health_check():
    return {"status": "ok", "service": settings.APP_NAME, "environment": settings.APP_ENV}


app.include_router(api_router, prefix=settings.API_V1_PREFIX)
