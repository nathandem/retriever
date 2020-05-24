import logging
import os
from mailjet_rest import Client


API_KEY = os.environ['RETRIEVER_MJ_API_KEY']
API_SECRET = os.environ['RETRIEVER_MJ_API_SECRET']
RECEIVER_EMAIL = os.environ['RETRIEVER_RECEIVER_EMAIL']
mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')


def send_email(subject: str, message: str):
    data = {
        'Messages': [
            {
                "From": {
                    "Email": os.environ['RETRIEVER_SENDER_EMAIL'],
                    "Name": "Retriever"
                },
                "To": [
                    {
                        "Email": RECEIVER_EMAIL,
                        "Name": os.environ['RETRIEVER_RECEIVER_NAME']
                    }
                ],
                "Subject": subject,
                "TextPart": message,
                "HTMLPart": message,
            }
        ]
    }

    result = mailjet.send.create(data=data)

    if result.status_code != 200:
        logging.error(f"An error occurred while sending the email! - status: {result.status_code}. Full res: {result}")
        raise Exception  # let the script crash


def email_alert(ref: str, name: str, url: str):
    subject = f"New issue of {name} available!"
    message = f"New issue of {name} available!\nLink: {url}"
    send_email(subject, message)
    logging.info(f"Email for new issue of {ref} sent to {RECEIVER_EMAIL}")


def email_error(ref: str, url: str):
    subject = f"Issue to {ref} failed!"
    message = f"Request to {ref} failed.\nFailing url: {url}"
    send_email(subject, message)
    logging.info(f"Email for request failure sent to {RECEIVER_EMAIL}")
