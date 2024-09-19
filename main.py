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
            response = handle_message(event_data)
    return "OK", 200

def handle_message(event_data):
    user_id = event_data.get("user")
    text = event_data.get("text")
    channel_id = event_data.get("channel")

    # Skip if the bot sent the message
    if user_id == "slackbot-template":  # Update this to your slackbot username
        return

    # Get a response from ChatGPT
    answer = get_chatgpt_response(text)

    # Post the answer back to Slack
    try:
        client.chat_postMessage(
            channel=channel_id,
            text=f"<@{user_id}> {answer}"
        )
    except SlackApiError as e:
        print(f"Error posting message: {e.response['error']}")

def get_chatgpt_response(user_input):
    response = openai.chat.completions.create(
        messages=[{
            "role": "user",
            "content": user_input,
        }],
        model="gpt-4",
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    app.run(port=3000)
