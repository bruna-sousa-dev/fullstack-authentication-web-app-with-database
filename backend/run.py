from app import create_app
from app.services.auth_service import create_default_user_service

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        from app.models.db_user_model import User
        from app import db
        create_default_user_service(User, db)
    app.run()
