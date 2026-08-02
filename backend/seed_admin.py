from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import User
from app.constants.roles import UserRole

app = create_app()

with app.app_context():

    admin = User.query.filter_by(
        role=UserRole.ADMIN.value
    ).first()

    if admin:
        print("✅ Admin already exists.")

    else:
        admin = User(
            name="Administrator",
            email="admin@tma.com",
            password_hash=generate_password_hash("admin123"),
            role=UserRole.ADMIN.value
        )

        db.session.add(admin)
        db.session.commit()

        print("✅ Default admin created successfully.")