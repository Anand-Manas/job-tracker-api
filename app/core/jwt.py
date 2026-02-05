from jose import jwt
from datetime import datetime, timedelta
from datetime import timezone
from app.core.config import SECRET_KEY, ALGORITHM


SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_minutes=15):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
