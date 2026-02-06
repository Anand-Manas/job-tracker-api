from fastapi import APIRouter
from app.models.schemas import ApplicationCreate
from app.services.application_service import create_application, get_all_applications
from fastapi import Depends
#from app.core.config import get_settings
from app.core.database import get_db
from app.models.schemas import ApplicationResponse
from fastapi import Header
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import SECRET_KEY, ALGORITHM
import json
from app.core.cache import redis_client
from fastapi import BackgroundTasks
from app.tasks.activity import log_activity

router = APIRouter(prefix="/applications", tags=["Applications"])
security = HTTPBearer()

@router.get("/")
def list_apps(db=Depends(get_db)):
    if redis_client:
        try:
            cached = redis_client.get("applications")
            if cached:
                return json.loads(cached)
        except Exception:
            pass 

    apps = get_all_applications(db)

    if redis_client:
        try:
            redis_client.setex(
                "applications",
                60,
                json.dumps([
                    {
                        "id": a.id,
                        "company": a.company,
                        "position": a.position,
                        "status": a.status
                    } for a in apps
                ])
            )
        except Exception:
            pass

    return apps


@router.post("/", response_model=ApplicationResponse, status_code=201)
def create_app(
    data: ApplicationCreate,
    background_tasks: BackgroundTasks,
    db=Depends(get_db)
):
    app = create_application(db, data)

    background_tasks.add_task(
        log_activity,
        data.company,
        data.position
    )

    if redis_client:
        try:
            redis_client.delete("applications")
        except Exception:
            pass

    return app

@router.get("/secure")
def secure_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    print("RAW TOKEN RECEIVED:", token)
    print("SECRET USED:", SECRET_KEY)
    print("ALGO USED:", ALGORITHM)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("DECODED PAYLOAD:", payload)
    except JWTError as e:
        print("JWT ERROR:", str(e))
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {
        "user": payload.get("sub"),
        "message": "Access granted"
    }

