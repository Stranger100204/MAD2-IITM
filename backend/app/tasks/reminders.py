from app.extensions import celery


@celery.task(name="daily_reminder")
def daily_reminder():

    print("Running Daily Reminder")

    return "Done"