from config.celery import app
from account.services import send


@app.task
def send_welcome_email(user_email):
    send(user_email)
