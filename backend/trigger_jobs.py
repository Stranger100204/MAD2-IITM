from app import create_app
from app.tasks.reminders import daily_reminder
from app.tasks.reports import monthly_report

app = create_app()

def run():
    with app.app_context():
        print("Trigerring Daily Reminder Task (Celery)...")
        # Run it synchronously for the sake of the demo so they don't even need the celery worker running!
        # Wait, if we use .delay() they MUST have the celery worker running. 
        # For the demo, let's just trigger the actual functions so it works even if celery worker isn't active.
        daily_reminder()
        
        print("Trigerring Monthly Report Task (Celery)...")
        monthly_report()
        
        print("\nTasks have been executed!")
        print("Check 'mock_emails.log' in the backend folder to see the generated emails.")

if __name__ == "__main__":
    run()
