import os
import zmq
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def main():
    load_dotenv()
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5567")
    email_username = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")

    try:
        while True:
            if socket.poll(1000):
                obj = socket.recv_json()
                email, name, url = obj["email"], obj["name"], obj["url"]

                subject = "Price Alert"
                body = (
                    f"Hello,\n\n"
                    f"Your Amazon item '{name}' has reached your desired price!"
                    f"Click the link below to be redirected to the item's page:\n\n"
                    f"{url}\n\n"
                    f"Thanks!"
                )

                msg = MIMEMultipart()
                msg['From'] = email_username
                msg['To'] = email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtpserver:
                    smtpserver.ehlo()

                    smtpserver.login(email_username,
                                     email_password)
                    smtpserver.sendmail(email_username, email, msg.as_string())

                msg = f'Alert has been sent to {email}'
                socket.send(msg.encode('utf-8'))
    except KeyboardInterrupt:
        print("Email sender is shutting down")
    finally:
        socket.close()
        print("Socket Closed")


if __name__ == "__main__":
    main()
