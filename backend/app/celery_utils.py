from app.extensions import celery


def init_celery(app):

    celery.conf.broker_url = "redis://localhost:6379/0"
    celery.conf.result_backend = "redis://localhost:6379/0"

    class ContextTask(celery.Task):

        def __call__(self, *args, **kwargs):

            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery