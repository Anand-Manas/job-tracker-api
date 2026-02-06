from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

from app.api.routes import applications, auth
from app.core.database import engine, Base
from app.models import db_models  

app = FastAPI()

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in real prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ STARTUP ------------------
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

# ------------------ LOGGING MIDDLEWARE ------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(
        f"{request.method} {request.url.path} "
        f"→ {response.status_code} "
        f"[{process_time:.3f}s]"
    )
    return response

# ------------------ ROUTES ------------------
app.include_router(applications.router)
app.include_router(auth.router)
