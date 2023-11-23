#store converstion of one intent in the s3 bucket
import boto3
import json
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import PartialCredentialsError
from botocore.exceptions import BotoCoreError

# Initialize the Lex runtime client
lex_runtime = boto3.client('lexv2-runtime', region_name='us-east-1') 

bot_id = 'HDSQ7W9OQ5'
bot_alias_id = 'TSTALIASID'

# Initialize S3 client
s3 = boto3.client('s3') 
bucket_name = 'practices-0'

# Define the conversation history list
conversation_history = []

# Interaction loop
while True:
    # Get user input 
    user_input = input("User: ")
    
    # Send user input to the bot
    response = lex_runtime.recognize_text(
        botId=bot_id,
        botAliasId=bot_alias_id,
        localeId="en_US",
        sessionId='sessionId',
        text=user_input
    )
    
    # Get the bot's response
    bot_response = response['messages'][0]['content']
    print("Bot:", bot_response)
    
    # Add user input and bot response to conversation history
    conversation_history.append({"user": user_input, "bot": bot_response})
    
    # Break the loop if the bot indicates the conversation is complete
    if response['sessionState']['dialogAction']['type'] =="ElicitIntent":
        break

# Store the conversation history in S3
try:
    s3.put_object(
        Bucket=bucket_name,
        Key='conversation.json',
        Body=json.dumps(conversation_history)
    )
    print("Conversation stored in S3 successfully.")

    # Generate a pre-signed URL for the stored conversation
    presigned_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': 'conversation.json'})
    print("Presigned URL to access the conversation:", presigned_url)

except (NoCredentialsError, PartialCredentialsError, BotoCoreError) as e:
    print("Error:", e)
