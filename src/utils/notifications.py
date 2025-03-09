import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage


load_dotenv()


class Notificator:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.port = int(os.getenv("SMTP_SERVER_PORT"))
        self.service_email = os.getenv("SERVICE_EMAIL")
        self.service_email_password = os.getenv("SERVICE_EMAIL_PASSWORD")
        self.email_recipient = os.getenv("EMAIL_RECIPIENT")

    def _get_smpt_server_connection(self):
        server = smtplib.SMTP(self.smtp_server, self.port)
        server.starttls()
        server.login(self.service_email, self.service_email_password)
        return server

    def _send_email(
        self,
        subject: str | bytes,
        message: str | bytes,
    ):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.service_email
        msg['To'] = self.email_recipient
        msg.set_content(message)


        server = self._get_smpt_server_connection()
        server.send_message(msg)
        # server.sendmail(
        #     from_addr=self.service_email,
        #     to_addrs=self.email_recipient,
        #     # msg=f"Subject: {subject}\n\n{message}".encode("UTF-8")
        # )
        server.quit()

    def send_notification_about_balance(self, current_balance):
        subject = f"Низкий баланс на OpenRouter: пополните счёт для продолжения работы"
        message = f"Уважаемый пользователь!\n"\
                  f"На вашем аккаунте OpenRouter осталось {current_balance} кредитов.\n"\
                  f"Чтобы избежать прерывания запросов к API, рекомендуем пополнить баланс в ближайшее время.\n\n"\
                  f"Что нужно сделать:\n"\
                  f"- Перейдите в раздел Пополнение счёта - https://openrouter.ai/credits .\n"\
                  f"- Выберите удобный способ оплаты.\n"\
                  f"- Укажите сумму пополнения.\n\n\n"\
                  f"Нужна помощь?\n"\
                  f"- Напишите в поддержку: support@openrouter.ai \n\n"\
                  f"С уважением,\n"\
                  f"Шилов Илья"
        self._send_email(subject, message)
