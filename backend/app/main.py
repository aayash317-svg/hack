from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.core.config import settings
from backend.app.db.base import Base
from backend.app.db.session import engine, SessionLocal
from backend.app.models import user, complaint, identity, suspect, evidence, case_link, case_group, escalation, status_history, notification, audit_log
from backend.app.core.security import get_password_hash
from backend.app.models.user import User

# Import routers
from backend.app.api.auth import router as auth_router
from backend.app.api.complaints import router as complaints_router
from backend.app.api.tracking import router as tracking_router
from backend.app.api.cases import router as cases_router
from backend.app.api.evidence import router as evidence_router
from backend.app.api.match_reviews import router as match_reviews_router
from backend.app.api.escalations import router as escalations_router
from backend.app.api.admin import router as admin_router


def seed_demo_accounts():
    """Initializes synthetic demo authority accounts if empty."""
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            demo_users = [
                User(
                    name="System Administrator",
                    email="admin@campus.edu",
                    password_hash=get_password_hash("AdminPass2026!"),
                    role="administrator",
                    department="Campus Administration"
                ),
                User(
                    name="Dr. S. Sharma (HOD)",
                    email="hod.cse@campus.edu",
                    password_hash=get_password_hash("HodPass2026!"),
                    role="hod",
                    department="Computer Science & Engineering"
                ),
                User(
                    name="Prof. M. Verma (Dean)",
                    email="dean.studentaffairs@campus.edu",
                    password_hash=get_password_hash("DeanPass2026!"),
                    role="dean",
                    department="Student Affairs & Welfare"
                ),
                User(
                    name="Dr. R. Kapoor (Higher Authority)",
                    email="director.office@campus.edu",
                    password_hash=get_password_hash("DirectorPass2026!"),
                    role="higher_authority",
                    department="Office of the Director / Ombudsman"
                ),
                User(
                    name="Aarav Patel (Student)",
                    email="student.demo@campus.edu",
                    password_hash=get_password_hash("StudentPass2026!"),
                    role="student",
                    department="Computer Science & Engineering"
                ),
            ]
            db.add_all(demo_users)
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create DB tables
    Base.metadata.create_all(bind=engine)
    # Ensure evidence storage dir
    storage_dir = Path(settings.EVIDENCE_STORAGE_DIR)
    storage_dir.mkdir(parents=True, exist_ok=True)
    # Seed default accounts
    seed_demo_accounts()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(complaints_router, prefix=settings.API_V1_STR)
app.include_router(tracking_router, prefix=settings.API_V1_STR)
app.include_router(cases_router, prefix=settings.API_V1_STR)
app.include_router(evidence_router, prefix=settings.API_V1_STR)
app.include_router(match_reviews_router, prefix=settings.API_V1_STR)
app.include_router(escalations_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)


@app.get("/api/health", tags=["Health"])
def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "institution": settings.INSTITUTION_NAME
    }


# Mount Frontend static files
frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(frontend_dir / "index.html")

    @app.get("/{page}.html")
    def serve_html_page(page: str):
        page_path = frontend_dir / f"{page}.html"
        if page_path.exists():
            return FileResponse(page_path)
        return FileResponse(frontend_dir / "index.html")
