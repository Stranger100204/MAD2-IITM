from datetime import datetime

from app.extensions import db
from app.constants.status import BookingStatus


class Booking(db.Model):
    """
    Represents a user's booking for a trek.

    Acts as the junction table between User and Trek while storing
    booking-specific information.
    """
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id"),
        nullable=False
    )

    booking_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default=BookingStatus.BOOKED.value
    )

    payment_status = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        back_populates="bookings"
    )

    trek = db.relationship(
        "Trek",
        back_populates="bookings"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "trek_id",
            name="unique_user_trek_booking"
        ),
    )

    def __repr__(self):
        return f"<Booking User={self.user_id} Trek={self.trek_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "trek_id": self.trek_id,
            "booking_date": self.booking_date.isoformat() if self.booking_date else None,
            "status": self.status,
            "payment_status": self.payment_status,
        }