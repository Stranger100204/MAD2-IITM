from app.models import User, Trek, Booking

from app.extensions import db

from app.models import (
    User,
    Staff,
    Trek,
    Booking
)

from app.constants.roles import UserRole
from app.constants.status import TrekStatus, UserStatus

from app.utils.security import hash_password
from app.extensions import cache
from datetime import datetime

class AdminService:
    
    @staticmethod
    def get_dashboard_statistics():

        return {
            "statistics": {
                "total_users": User.query.filter_by(role="TREKKER").count(),
                "total_staff": User.query.filter_by(role="STAFF").count(),
                "total_treks": Trek.query.count(),
                "total_bookings": Booking.query.count()
            }
        }

    @staticmethod
    def create_trek(data):

        required_fields = [
            "name",
            "location",
            "difficulty",
            "duration_days",
            "total_slots",
            "start_date",
            "end_date"
        ]

        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field} is required.")

        total_slots = int(data.get("total_slots"))

        trek = Trek(
            name=data.get("name"),
            description=data.get("description"),
            location=data.get("location"),
            difficulty=data.get("difficulty"),
            duration_days=int(data.get("duration_days")),
            total_slots=total_slots,
            available_slots=total_slots,
            assigned_staff_id=data.get("assigned_staff_id"),
            status=data.get("status", TrekStatus.PENDING.value),
            start_date=datetime.strptime(
                data.get("start_date"),
                "%Y-%m-%d"
            ).date(),
            end_date=datetime.strptime(
                data.get("end_date"),
                "%Y-%m-%d"
            ).date()
        )

        db.session.add(trek)
        db.session.commit()
        cache.clear()

        return trek

    @staticmethod
    def get_all_treks():
        return Trek.query.order_by(Trek.created_at.desc()).all()

    @staticmethod
    def get_trek(trek_id):
        trek = Trek.query.get(trek_id)

        if not trek:
            raise ValueError("Trek not found.")

        return trek

    @staticmethod
    def update_trek(trek_id, data):

        trek = Trek.query.get(trek_id)

        if not trek:
            raise ValueError("Trek not found.")

        if "name" in data:
            trek.name = data["name"]

        if "description" in data:
            trek.description = data["description"]

        if "location" in data:
            trek.location = data["location"]

        if "difficulty" in data:
            trek.difficulty = data["difficulty"]

        if "duration_days" in data:
            trek.duration_days = int(data["duration_days"])

        if "status" in data:
            trek.status = data["status"]

        if "assigned_staff_id" in data:
            trek.assigned_staff_id = data["assigned_staff_id"]

        if "start_date" in data:
            trek.start_date = datetime.strptime(
                data["start_date"],
                "%Y-%m-%d"
            ).date()

        if "end_date" in data:
            trek.end_date = datetime.strptime(
                data["end_date"],
                "%Y-%m-%d"
            ).date()

        if "total_slots" in data:

            total_slots = int(data["total_slots"])

            booked_slots = trek.total_slots - trek.available_slots

            if total_slots < booked_slots:
                raise ValueError(
                    "Total slots cannot be less than booked slots."
                )

            trek.available_slots = total_slots - booked_slots
            trek.total_slots = total_slots

        db.session.commit()
        cache.clear()

        return trek

    @staticmethod
    def delete_trek(trek_id):

        trek = Trek.query.get(trek_id)

        if not trek:
            raise ValueError("Trek not found.")

        if trek.bookings:
            raise ValueError(
                "Cannot delete a trek with existing bookings."
            )

        db.session.delete(trek)

        db.session.commit()
        cache.clear()

    @staticmethod
    def create_staff(data):

        required_fields = [
            "name",
            "email",
            "password",
            "phone",
            "specialization",
            "experience_years",
            "emergency_contact"
        ]

        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field} is required.")

        existing_user = User.query.filter_by(
            email=data["email"]
        ).first()

        if existing_user:
            raise ValueError(
                "Email already registered."
            )

        user = User(
            name=data["name"],
            email=data["email"],
            password_hash=hash_password(
                data["password"]
            ),
            phone=data["phone"],
            role=UserRole.STAFF.value
        )

        db.session.add(user)
        db.session.flush()

        staff = Staff(
            user_id=user.id,
            specialization=data["specialization"],
            experience_years=int(
                data["experience_years"]
            ),
            emergency_contact=data["emergency_contact"]
        )

        db.session.add(staff)

        db.session.commit()

        return user

    @staticmethod
    def get_all_staff():

        return Staff.query.order_by(
            Staff.created_at.desc()
        ).all()

    @staticmethod
    def get_staff(staff_id):

        staff = Staff.query.get(staff_id)

        if not staff:
            raise ValueError("Staff not found.")

        return staff

    @staticmethod
    def update_staff(staff_id, data):

        staff = Staff.query.get(staff_id)

        if not staff:
            raise ValueError("Staff not found.")

        user = staff.user

        if "name" in data:
            user.name = data["name"]

        if "phone" in data:
            user.phone = data["phone"]

        if "status" in data:
            user.status = data["status"]

        if "specialization" in data:
            staff.specialization = data["specialization"]

        if "experience_years" in data:
            staff.experience_years = int(
                data["experience_years"]
            )

        if "emergency_contact" in data:
            staff.emergency_contact = data["emergency_contact"]

        db.session.commit()

        return staff

    @staticmethod
    def delete_staff(staff_id):

        staff = Staff.query.get(staff_id)

        if not staff:
            raise ValueError("Staff not found.")

        if staff.user.assigned_treks:
            raise ValueError(
                "Staff is assigned to one or more treks."
            )

        db.session.delete(staff.user)

        db.session.commit()

    @staticmethod
    def assign_staff(trek_id, staff_id):

        trek = Trek.query.get(trek_id)

        if not trek:
            raise ValueError("Trek not found.")

        staff = Staff.query.get(staff_id)

        if not staff:
            raise ValueError("Staff not found.")

        if staff.user.role != UserRole.STAFF.value:
            raise ValueError("Selected user is not a staff member.")

        if staff.user.status != UserStatus.ACTIVE.value:
            raise ValueError("Staff member is inactive.")

        trek.assigned_staff_id = staff.user_id

        db.session.commit()

        return trek

    @staticmethod
    def get_all_users():

        return User.query.order_by(
            User.created_at.desc()
        ).all()

    @staticmethod
    def get_user(user_id):

        user = User.query.get(user_id)

        if not user:
            raise ValueError("User not found.")

        return user

    @staticmethod
    def update_user_status(user_id, status, current_admin_id):

        user = User.query.get(user_id)

        if not user:
            raise ValueError("User not found.")

        if user.id == current_admin_id:
            raise ValueError("Admin cannot change their own status.")

        allowed_statuses = [
            UserStatus.ACTIVE.value,
            UserStatus.BLACKLISTED.value
        ]

        if status not in allowed_statuses:
            raise ValueError("Invalid status.")

        user.status = status

        db.session.commit()

        return user

    @staticmethod
    def search(query):

        users = User.query.filter(
            User.name.ilike(f"%{query}%")
        ).all()

        staff = Staff.query.join(User).filter(
            User.name.ilike(f"%{query}%")
        ).all()

        treks = Trek.query.filter(
            Trek.name.ilike(f"%{query}%")
        ).all()

        return {
            "users": [
                user.to_dict()
                for user in users
            ],
            "staff": [
                member.to_dict()
                for member in staff
            ],
            "treks": [
                trek.to_dict()
                for trek in treks
            ]
        }

    @staticmethod
    def get_all_bookings():

        bookings = Booking.query.order_by(
            Booking.booking_date.desc()
        ).all()

        return bookings

    @staticmethod
    def get_trek_history():

        treks = Trek.query.filter_by(
            status=TrekStatus.COMPLETED.value
        ).order_by(
            Trek.end_date.desc()
        ).all()

        return treks