from celery import shared_task


# celery -A main.celery_app worker --loglevel=info
# celery -A main.celery_app flower --port=5555
# Then enter python console
# >>> from main import app
# >>> from tasks.sample_tasks import divide
# >>> task = divide.delay(10,2)

@shared_task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y

@shared_task
def add(x, y):
    import time
    time.sleep(5)
    return x + y
