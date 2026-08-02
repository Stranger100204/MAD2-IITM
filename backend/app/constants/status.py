from enum import Enum


class UserStatus(Enum):
    ACTIVE = "ACTIVE"
    BLACKLISTED = "BLACKLISTED"
    INACTIVE = "INACTIVE"


class TrekStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    COMPLETED = "COMPLETED"


class BookingStatus(Enum):
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"