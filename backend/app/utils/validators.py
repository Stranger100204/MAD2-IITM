import re
from datetime import datetime

def validate_registration_data(data):

    required_fields = [
        "name",
        "email",
        "password"
    ]

    for field in required_fields:

        if not data.get(field):
            return f"{field} is required."

    email = data.get("email")

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(email_pattern, email):
        return "Invalid email address."

    if len(data.get("password")) < 6:
        return "Password must be at least 6 characters long."

    return None

def validate_trek_data(data):

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

        if data.get(field) in [None, ""]:
            return f"{field} is required."

    if data["duration_days"] <= 0:
        return "Duration must be greater than zero."

    if data["total_slots"] <= 0:
        return "Total slots must be greater than zero."

    try:

        start_date = datetime.strptime(
            data["start_date"],
            "%Y-%m-%d"
        )

        end_date = datetime.strptime(
            data["end_date"],
            "%Y-%m-%d"
        )

    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."

    if end_date < start_date:
        return "End date cannot be before start date."

    return None

def validate_staff_data(data):

    required_fields = [
        "name",
        "email",
        "password",
        "specialization",
        "experience_years"
    ]

    for field in required_fields:

        if data.get(field) in [None, ""]:
            return f"{field} is required."

    if data["experience_years"] < 0:
        return "Experience cannot be negative."

    phone = data.get("phone")

    if phone and len(phone) != 10:
        return "Phone number must contain 10 digits."

    emergency = data.get("emergency_contact")

    if emergency and len(emergency) != 10:
        return "Emergency contact must contain 10 digits."

    return None