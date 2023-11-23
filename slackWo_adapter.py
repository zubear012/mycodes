# make .env file with slack token
import slack
import os
from pathlib import Path
from dotenv import *
from flask import Flask, request, jsonify
import boto3

client_lex = boto3.client("lexv2-runtime")

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

slack_token = os.getenv("slack_token")
print('slack_token-----',slack_token)

app = Flask(__name__)
# client = slack.WebClient(token=slack_token)
# bot_id = client.api_call("auth.test")['user_id']

def lex(sessionId, text):
    response = client_lex.recognize_text(
        botId='SZENO5SJPC',
        botAliasId='TSTALIASID',
        localeId="en_US",
        sessionId=sessionId,
        text=text
    )
    content_response = response['messages'][0]['content']
    print("prompt from lex------>", content_response)
    return content_response

@app.route('/slack/events', methods=['POST'])
def slack_events():
    client = slack.WebClient(token=slack_token)
    bot_id = client.api_call("auth.test")['user_id']
    data = request.get_json()
    print("<<<<<<<data>>>>>>>", data)
    if data['type'] == 'url_verification':
        return jsonify({'challenge': data['challenge']})
    
    event = data.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    session_id = 'test'
    print('the message from slack------>', text)
    message = lex(session_id, text)

    if bot_id != user_id:
        client.chat_postMessage(channel='#bottest', text=message)
    
    return jsonify({'message': 'Message sent successfully!'})

if __name__ == "__main__":
    app.run(debug=True)
    
    
