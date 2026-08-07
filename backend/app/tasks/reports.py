from app.extensions import celery


@celery.task(name="monthly_report")
def monthly_report():

    print("Generating Monthly Report")

    return "Done"