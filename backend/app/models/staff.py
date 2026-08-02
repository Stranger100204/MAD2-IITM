from datetime import datetime

from app.extensions import db


class Staff(db.Model):
    """
    Stores additional information specific to staff members.

    Each Staff record belongs to exactly one User with the STAFF role.
    Contains trekking experience and specialization details.
    """
    __tablename__ = "staff"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    experience_years = db.Column(
        db.Integer,
        default=0
    )

    specialization = db.Column(
        db.String(100)
    )

    emergency_contact = db.Column(
        db.String(15)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        back_populates="staff"
    )

    def __repr__(self):
        return f"<Staff User={self.user_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "experience_years": self.experience_years,
            "specialization": self.specialization,
            "emergency_contact": self.emergency_contact,
        }