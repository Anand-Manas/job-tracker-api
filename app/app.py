from fastapi import FastAPI
from app.api.routes import applications, auth
from fastapi.middleware.cors import CORSMiddleware
import time
from fastapi import Request
from fastapi import FastAPI
from app.core.database import init_db
from app.core.database import engine
from app.models.db_models import Base


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

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


app.include_router(applications.router)
app.include_router(auth.router)
