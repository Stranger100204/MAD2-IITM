from app.constants.roles import UserRole
from app.constants.status import UserStatus
from datetime import datetime
from app.extensions import db


class User(db.Model):
    """
    Represents all authenticated users in the Trekking Management Application.

    Roles:
    - ADMIN
    - STAFF
    - TREKKER

    Stores authentication credentials and common profile information.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    phone = db.Column(db.String(15))

    role = db.Column(
        db.String(20),
        nullable=False,
        default=UserRole.TREKKER.value
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default=UserStatus.ACTIVE.value
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    staff = db.relationship(
        "Staff",
        back_populates="user",
        uselist=False,
        cascade='all, delete-orphan'
    )
    
    assigned_treks = db.relationship(
        "Trek",
        back_populates="assigned_staff",
        lazy=True
    )

    bookings = db.relationship(
        "Booking",
        back_populates="user",
        cascade='all, delete-orphan',
        lazy=True
    )

    def __repr__(self):
        return f"<User {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }