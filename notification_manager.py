from twilio.rest import Client
import smtplib
import requests
import os

TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_KEY = os.environ.get("TWILIO_KEY")

to_number = os.environ.get("TO_NUMBER")
from_number = os.environ.get("FROM_NUMBER")

suzy_email = os.environ.get("SEND_EMAIL")
suzy_password = os.environ.get("SEND_PASSWORD")
josh_email = os.environ.get("RECIEVE_EMAIL")

SHEETY_USERS_ENDPOINT = "https://api.sheety.co/f152023cd2003d67eac458538ae45d0b/flightFinder/users"

class NotificationManager:

    def __init__(self):
        self.twi_auth = TWILIO_SID
        self.twi_key = TWILIO_KEY
        self.to_num = to_number
        self.from_num = from_number

    def send_message(self, message):
        client = Client(self.twi_auth, self.twi_key)
        message = client.messages \
            .create(
            body=message,
            from_=self.from_num,
            to=to_number,
        )
        # print(message.status)

    def send_emails(self, message):
        email_list = []
        response = requests.get(SHEETY_USERS_ENDPOINT)
        response_json = response.json()
        response_list_of_dict = response_json["users"]
        for x in response_list_of_dict:
            email_list.append(x["email"])

        for email in email_list:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=suzy_email, password=suzy_password)
                connection.sendmail(from_addr=suzy_email, to_addrs=email,
                                    msg=message)
