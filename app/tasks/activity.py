from datetime import datetime

def log_activity(company: str, position: str):
    print("BACKGROUND TASK RUNNING")
    with open("activity.log", "a", encoding="utf-8") as f:
        f.write(
            f"[{datetime.utcnow()}] Applied to {company} for {position}\n"
        )
