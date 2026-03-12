from flask import Flask, request

# Load the standard json library to handle returned data format
import json

# Load LINE Message API related libraries
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from chatbot import chatbot

from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage

import os
from dotenv import load_dotenv

load_dotenv()

access_token = os.environ['ACCESS_TOKEN']
secret = os.environ['SECRET_KEY']


app = Flask(__name__)
@app.route("/", methods=['POST'])


def linebot():
    body = request.get_data(as_text=True)                    # Get the received message content
    
    try:
        json_data = json.loads(body)                         # Convert message content to JSON format
        line_bot_api = LineBotApi(access_token)              # Verify whether the token is correct
        handler = WebhookHandler(secret)                     # Verify whether the secret key is correct
        signature = request.headers['X-Line-Signature']      # Get the signature from headers
        handler.handle(body, signature)                      # Bind the message handling information
        tk = json_data['events'][0]['replyToken']            # Get the reply token
        
        type = json_data['events'][0]['message']['type']     # Get the message type received by LINE
        
        if type=='text':
            msg = json_data['events'][0]['message']['text']  # Get the text message received from LINE
            print(msg)                                       # Print the received message
            
            response = chatbot(str(msg))
            #print('frombot:\n\n\n',response)
            reply = response
        else:
            reply = 'The message you sent is not text.'
        print(reply)
        
        line_bot_api.reply_message(tk,TextSendMessage(reply))# Send reply message
        
    except:
        print(body)                                          # If an error occurs, print the received content
    return 'OK'                                              # Required for webhook verification

if __name__ == "__main__":
    app.run()