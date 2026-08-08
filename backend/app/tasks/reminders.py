from app.extensions import celery
from app.services.reminder_service import ReminderService
from app.utils.email import send_email

@celery.task(name="daily_reminder")
def daily_reminder():

    reminders = ReminderService.get_upcoming_users()

    print("=" * 50)
    print("Daily Reminder Job")
    print("=" * 50)

    if not reminders:
        print("No reminders today.")
        return "No reminders"

    for reminder in reminders:

        send_email(
    reminder["user"],
    "Upcoming Trek Reminder",
    f"""
Hello,

Your trek "{reminder['trek']}"
starts on {reminder['start_date']}.

Please report on time.

Happy Trekking!
"""
)

    return f"{len(reminders)} reminders processed"