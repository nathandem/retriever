import os
from mailjet_rest import Client


API_KEY = os.environ['RETRIEVER_MJ_API_KEY']
API_SECRET = os.environ['RETRIEVER_MJ_API_SECRET']
mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')

def send_paper(name: str, ref: str, url: str):
    receiver_email = os.environ['RETRIEVER_RECEIVER_EMAIL']
    data = {
        'Messages': [
            {
                "From": {
                    "Email": os.environ['RETRIEVER_SENDER_EMAIL'],
                    "Name": "Retriever"
                },
                "To": [
                    {
                        "Email": receiver_email,
                        "Name": os.environ['RETRIEVER_RECEIVER_NAME']
                    }
                ],
                "Subject": f"New issue of {ref} available!",
                "TextPart": f"New issue of {name} available at {url}",
                "HTMLPart": f"New issue of {name} available at {url}",
            }
        ]
    }

    result = mailjet.send.create(data=data)

    if result.status_code != 200:
        print("An error occurred while sending the email!")
        # note: no exception raised to avoid making `retriever` flow harder to read with too many try/except blocks

    print(f"Email for {ref} sent to {receiver_email}")
