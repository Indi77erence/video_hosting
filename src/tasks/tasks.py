import smtplib
from email.message import EmailMessage
from celery import Celery


from src.config import SMTP_USER, SMTP_PASSWORD


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')


def get_email_report_video(user_email: str):
	email = EmailMessage()
	email['Subject'] = 'Названия последних 5 загруженных видеозаписей'
	email['From'] = SMTP_USER
	email['To'] = user_email
	email.set_content(
		'<div>'
		f'<h1 style="color: red;">Здравствуйте, {user_email}, вот последние загруженные видеозаписи. Зацените 😊</h1>'
		# f'<h2 style="color: red;">Вот они: {last_video}</h2>'
		'</div>',
		subtype='html'
	)
	return email


@celery.task
def send_email_report_last_video(user_email: str):
	email = get_email_report_video(user_email)
	with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
		server.login(SMTP_USER, SMTP_PASSWORD)
		server.send_message(email)
