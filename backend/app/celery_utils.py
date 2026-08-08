from app.extensions import celery

from celery.schedules import crontab


def init_celery(app):

    celery.conf.broker_url = "redis://localhost:6379/0"
    celery.conf.result_backend = "redis://localhost:6379/0"
    celery.conf.beat_schedule = {

        "daily-reminder": {

            "task": "daily_reminder",

            "schedule": crontab(hour=8, minute=0)

        },

        "monthly-report": {

            "task": "monthly_report",

            "schedule": crontab(
                day_of_month=1,
                hour=8,
                minute=0
            )

        }

    }

    class ContextTask(celery.Task):

        def __call__(self, *args, **kwargs):

            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery