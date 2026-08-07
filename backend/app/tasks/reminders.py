from app.extensions import celery
from app.services.reminder_service import ReminderService


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

        print(
            f"Reminder -> {reminder['user']} | "
            f"{reminder['trek']} | "
            f"{reminder['start_date']}"
        )

    return f"{len(reminders)} reminders processed"