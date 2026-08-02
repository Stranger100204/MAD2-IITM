from datetime import datetime

from app.extensions import db
from app.constants.difficulty import Difficulty
from app.constants.status import TrekStatus


class Trek(db.Model):
    """
    Represents a trekking event created and managed by the administrator.

    Each trek is assigned to one staff member and can have multiple bookings.
    """
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)

    description = db.Column(db.Text)

    location = db.Column(db.String(120), nullable=False)

    difficulty = db.Column(
        db.String(20),
        nullable=False,
        default=Difficulty.EASY.value
    )

    duration_days = db.Column(
        db.Integer,
        nullable=False
    )

    total_slots = db.Column(
        db.Integer,
        nullable=False
    )

    available_slots = db.Column(
        db.Integer,
        nullable=False
    )

    assigned_staff_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default=TrekStatus.PENDING.value
    )

    start_date = db.Column(
        db.Date,
        nullable=False
    )

    end_date = db.Column(
        db.Date,
        nullable=False
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

    assigned_staff = db.relationship(
        "User",
        back_populates="assigned_treks"
    )

    bookings = db.relationship(
        "Booking",
        back_populates="trek",
        cascade='all, delete-orphan',
        lazy=True
    )

    def __repr__(self):
        return f"<Trek {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "difficulty": self.difficulty,
            "duration_days": self.duration_days,
            "total_slots": self.total_slots,
            "available_slots": self.available_slots,
            "assigned_staff_id": self.assigned_staff_id,
            "status": self.status,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
        }