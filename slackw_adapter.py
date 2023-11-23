# Make .env file with signing secret , slack token
import slack
import os
from pathlib import Path
from dotenv import *
from flask import Flask
from slackeventsapi import SlackEventAdapter
import boto3
client_lex = boto3.client("lexv2-runtime")

env_path= Path('.')/ '.env'
load_dotenv(dotenv_path=env_path)
signing_secret = os.getenv("signing_secret")
slack_token = os.getenv("slack_token")
app=Flask(__name__)
slack_event_adapter=SlackEventAdapter(signing_secret,'/slack/events',app)
client=slack.WebClient(token=slack_token)
print("client", client)
bot_id=client.api_call("auth.test")['user_id']
print("bot_id", bot_id)

@slack_event_adapter.on('message')
def message(payload):
    print("PAYLOAD", payload)
    event=payload.get('event',{})
    print("EVENT")
    channel_id=event.get('channel')
    user_id=event.get('user')
    text=event.get('text')
    sessionId='test'
    print('the message from slack------>',text)
    message=lex(sessionId,text)

    if bot_id!=user_id:
        client.chat_postMessage(channel='#bottest',text=message)


def lex(sessionId , text):
    response = client_lex.recognize_text(
        botId='SZENO5SJPC',
        botAliasId='TSTALIASID',
        localeId="en_US",
        sessionId=sessionId,
        text=text
    )
    content_response = response['messages'][0]['content']
    print("prompt------>", content_response)
    return content_response



if __name__=="__main__":
    app.run(debug=True)
