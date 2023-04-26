import os
from flask import Flask, jsonify, request
from client import WhatsAppWrapper

from dotenv import load_dotenv

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get('WHATSAPP_HOOK_TOKEN')

load_dotenv()

@app.route("/send_message/", methods=["POST"])
def send_message():

    if "phone_number" not in request.json:
        return jsonify({"error": "Missing phone_number"}), 400

    if "message_body" not in request.json:
        return jsonify({"error": "Missing message_body"}), 400

    response = WhatsAppWrapper().send_message(
        message_body=request.json["message_body"],
        phone_number=request.json["phone_number"],
    )

    return jsonify(
        {
            "data": response,
            "status": "success",
        },
    ), 200

@app.route("/send_template_message/", methods=["POST"])
def send_template_message():

    if "language_code" not in request.json:
        return jsonify({"error": "Missing language_code"}), 400

    if "phone_number" not in request.json:
        return jsonify({"error": "Missing phone_number"}), 400

    if "template_name" not in request.json:
        return jsonify({"error": "Missing template_name"}), 400

    response = WhatsAppWrapper().send_template_message(
        template_name=request.json["template_name"],
        language_code=request.json["language_code"],
        phone_number=request.json["phone_number"],
    )

    return jsonify(
        {
            "data": response,
            "status": "success",
        },
    ), 200

@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    
    if request.method == "GET":
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Authentication failed. Invalid Token."

    response = WhatsAppWrapper().process_webhook_notification(request.get_json())

    return jsonify({"status": "success"}, 200)