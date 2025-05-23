from models import db, user_datastore
from app import create_app

app, _ = create_app()

with app.app_context():
    db.create_all()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='User')
    db.session.flush()
    if not user_datastore.find_user(email="admin@abc.com"):
        print("Creating admin user")
        user_datastore.create_user(email="admin@abc.com", username="admin", password="admin", roles=['admin'])
    db.session.commit()