import os
def get_settings():
    return {"app_name": "Job Tracker API"}

import os

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
ALGORITHM = "HS256"

