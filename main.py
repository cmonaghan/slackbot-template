import os
from flask import Flask, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import openai

app = Flask(__name__)

# Slack and OpenAI tokens
slack_token = os.environ["SLACK_BOT_TOKEN"]
openai_api_key = os.environ["OPENAI_API_KEY"]

client = WebClient(token=slack_token)
openai.api_key = openai_api_key

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    # Check if event is a message
    if "event" in data:
        event_data = data["event"]
        if "text" in event_data:
            # Handle the message event
            handle_message(event_data)
    return "OK", 200

def handle_message(event_data):
    user_id = event_data.get("user")
    text = event_data.get("text")
    channel_id = event_data.get("channel")

    # Skip if the bot sent the message
    if user_id == None or user_id == "<BOT_USER_ID>":
        return

    # Get a response from ChatGPT
    response = get_chatgpt_response(text)

    # Post the response back to Slack
    try:
        client.chat_postMessage(
            channel=channel_id,
            text=f"<@{user_id}> {response}"
        )
    except SlackApiError as e:
        print(f"Error posting message: {e.response['error']}")

def get_chatgpt_response(user_input):
    response = openai.Completion.create(
        engine="gpt-4",  # Or "gpt-3.5-turbo"
        prompt=user_input,
        max_tokens=150
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    app.run(port=3000)
