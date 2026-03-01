from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from bot import ITDeptBot

app = Flask(__name__)
# Make sure your CSV file name exactly matches this string
my_bot = ITDeptBot('Time_Table -sem-2.xlsx - TE_A.csv')

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    # 1. Get the message the user sent on WhatsApp
    incoming_msg = request.values.get('Body', '').strip()
    
    # 2. Pass it to your OOP bot logic
    response_text = my_bot.process_query(incoming_msg)
    
    # 3. Format the response for Twilio to send back to WhatsApp
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(response_text)
    
    return str(resp)

# Gunicorn will look for this app object
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)