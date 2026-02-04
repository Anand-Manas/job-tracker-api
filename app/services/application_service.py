from app.models.db_models import Application


applications = []
app_id = 1

# def create_application(data):
#     global app_id
#     record = {
#         "id": app_id,
#         "company": data.company,
#         "position": data.position,
#         "status": data.status
#     }
#     applications.append(record)
#     app_id += 1
#     return record

# def get_all_applications():
#     return applications


def create_application(db, data):
    record = Application(
        company=data.company,
        position=data.position,
        status=data.status
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_applications(db):
    return db.query(Application).all()

