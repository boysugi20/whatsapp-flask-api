
# Flask API Wrapper for WhatsApp

This is a simple Flask API Wrapper for sending messages and templates to WhatsApp, which requires the following environment variables to be set in a `.env` file:

-   `WHATSAPP_API_TOKEN`: WhatsApp API token obtained from [https://developers.facebook.com/](https://developers.facebook.com/)
-   `WHATSAPP_NUMBER_ID`: Your WhatsApp number ID obtained from [https://developers.facebook.com/](https://developers.facebook.com/)
-   `WHATSAPP_HOOK_TOKEN`: Webhook token obtained from [https://developers.facebook.com/](https://developers.facebook.com/)

## Endpoints

-   `localhost/send_message/`: Send a message to a phone number.
    -   Request body should include `message_body` and `phone_number`.
-   `localhost/send_template_message/`: Send a template message to a phone number.
    -   Request body should include `template_name`, `language_code`, and `phone_number`.
-   `localhost/webhook/`: Endpoint for webhook to detect user sent messages.

## Setup

1.  Clone the repository:<br />
	`https://github.com/boysugi20/whatsapp-flask-api.git` 

2.  Install the required dependencies:<br />
	`pipenv shell` <br />
	`pipenv install` 

3.  Create a `.env` file in the root directory and set the following environment variables:<br />
	`WHATSAPP_API_TOKEN=<your_api_token>` <br />
	`WHATSAPP_NUMBER_ID=<your_number_id>` <br />
	`WHATSAPP_HOOK_TOKEN=<your_hook_token>`

4.  Run the application:<br />
	`flask run` 

## Usage

After running the application, you can use the above endpoints to send messages and templates to WhatsApp. You can use `curl` or any other HTTP client to make requests to the endpoints.

Example:
```go
curl -X POST \
  http://localhost:5000/send_message/ \
  -H 'Content-Type: application/json' \
  -d '{
        "message_body": "Hello, world!",
        "phone_number": "1234567890"
      }
```


This will send the message "Hello, world!" to the phone number "1234567890".
