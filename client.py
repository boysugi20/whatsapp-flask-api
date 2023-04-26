import os
import requests
import json
from datetime import datetime

class WhatsAppWrapper:

    API_URL = "https://graph.facebook.com/v16.0/"
    API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
    NUMBER_ID = os.environ.get("WHATSAPP_NUMBER_ID")

    print(NUMBER_ID, API_TOKEN)

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.API_URL + self.NUMBER_ID
    
    def send_message(self, message_body, phone_number):

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "text": {
                "body" : message_body
            }
        })

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        assert response.status_code == 200, "Error sending message"

        return response.status_code

    def send_template_message(self, template_name, language_code, phone_number):

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        })

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        assert response.status_code == 200, "Error sending message"

        return response.status_code
    
    def process_webhook_notification(self, data):

        response = []

        for entry in data["entry"]:

            for change in entry["changes"]:

                value = change["value"]

                # Message received
                if 'contacts' in value:

                    from_name = value['contacts'][0]['profile']['name']
                    from_number = value['contacts'][0]['wa_id']
                    timestamp = datetime.utcfromtimestamp(int(value['messages'][0]['timestamp'])).strftime('%Y%m%d%H%M%S')
                    msg_id = value['messages'][0]['id']
                    msg = value['messages'][0]['text']['body']
                    recipient = value["metadata"]["display_phone_number"]
                    
                    response.append(
                        {
                            "type": change["field"],
                            "msg_type": 'received',
                            "to": recipient,
                            "from_name": from_name,
                            "from_number": from_number,
                            "timestamp": timestamp,
                            "msg_id": msg_id,
                            "msg": msg,
                        }
                    )
                # Message sent
                else:

                    status = value['statuses'][0]['status']
                    timestamp = datetime.utcfromtimestamp(int(value['statuses'][0]['timestamp'])).strftime('%Y%m%d%H%M%S')
                    from_id = value["metadata"]['phone_number_id']
                    from_number = value["metadata"]['display_phone_number']

                    response.append(
                        {
                            "type": change["field"],
                            "msg_type": 'sent',
                            "status": status,
                            "timestamp": timestamp,
                            "from_id": from_id,
                            "from_number": from_number,
                        }
                    )
        return response