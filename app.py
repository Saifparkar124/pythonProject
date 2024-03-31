from flask import Flask, jsonify, request
import razorpay
import time
# from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

razorpay_client = razorpay.Client(auth=("rzp_test_jj2yCck3bTssnU", "qoR7BWWy5Z7EaDUzFgI5zWpf"))

# TELEGRAM_BOT_TOKEN = "7080909704:AAEjDep69_6PG69gRz3_xGsIHWZhTtIm6jA"
# TELEGRAM_CHAT_ID = " 5467600867"

# def send_telegram_message(message,payment_link_id=None):
#     url = f"https://api.telegram.org/7080909704:AAEjDep69_6PG69gRz3_xGsIHWZhTtIm6jA/sendMessage"
#     text = message
#     if payment_link_id:
#         text += f"\nPayment Link ID: {payment_link_id}"
#     payload = {
#         "chat_id": TELEGRAM_CHAT_ID,
#         "text": text
#     }
#     response = requests.post(url, json=payload)
#     return response.json()

@app.route('/', methods=['GET'])
def home():
    return 'Hello World!'

@app.route('/create_payment_link', methods=['POST'])
def create_payment_link():
    try:
        data = request.get_json()
        amount = data.get('amount')
        if amount is None:
            return jsonify({'error': 'Amount is required.'}), 400

        # Set expiration time to 5 minutes from now
        expire_by = int(time.time()) + 17 * 60  # 5 minutes in seconds

        payment_link = razorpay_client.payment_link.create({
            "amount": amount,
            "currency": "INR",
            "expire_by": expire_by,
            "notify": {
                "email": True,
                "sms": True
            },
            "notes": {
                "policy_name": "Ticketing System"
            },
            "description": "For XYZ purpose",
            # Add other configurations as needed
        })
        return jsonify(payment_link)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/payment_status', methods=['POST'])
def payment_status():
    try:
        data = request.get_json()
        payment_link_id = data.get('payment_link_id')
        if payment_link_id is None:
            return jsonify({'error': 'Payment link ID is required.'}), 400

        payment_link = razorpay_client.payment_link.fetch(payment_link_id)
        # if payment_link.get('status') == 'paid':
        #     send_telegram_message("Payment Successful!")
        return jsonify(payment_link)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
