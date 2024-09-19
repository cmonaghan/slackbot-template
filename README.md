# slackbot-template

Starter kit for building any kind of ChatGPT-backed slackbot, deployed on AWS Lambda.


## Setup steps

### 1. Set Up Slack API and Bot

* Create a Slack App: Go to the [Slack API website](https://api.slack.com/apps/) and create a new app.
Enable Permissions:
  * Enable the following permissions so the bot can post messages and read channels:
    * `chat:write`
    * `chat:write.public`
    * `channels:history`
    * `channels:join`
    * `app_mentions:read`
  * Enable any additional permissions based on where and how you want the bot to function (e.g., in DMs, private channels).
* Install App to Workspace: Once the app is created and permissions are set, install it in your Slack workspace to get a bot token.

### 2. Run the slackbot server locally

Install packages:

    pip install slack_sdk flask openai

Export access keys

    export SLACK_BOT_TOKEN='your-slack-bot-token'
    export OPENAI_API_KEY='your-openai-api-key'

Run the server

    python main.py

By default, Flask will run on http://localhost:3000.

Make a request

    curl --header "Content-Type: application/json" \
      --request POST \
      --data '{"event":{"text":"what is the meaning of life?","channel":"sandbox-for-testing","user":"christian"}}' \
      http://localhost:3000/slack/events

### 3. Customize slackbot

Customize the default ChatGPT prompt, completion settings, temperature, max tokens, etc.


## Expose Your Application to the Internet
You need to expose your local Flask app to the internet so that Slack can communicate with it. You can use ngrok for this:

Install ngrok:

    # https://ngrok.com/docs/getting-started/
    brew install ngrok/ngrok/ngrok
    # sign up for an ngrok account at https://dashboard.ngrok.com/
    ngrok config add-authtoken <TOKEN>

Put your app online:

    ngrok http 3000

Once ngrok is running, you’ll get a public URL (e.g., https://your-ngrok-url.ngrok.io) which you can use as the Request URL in your Slack app's Event Subscriptions settings.

### Configure Slack
Go to your Slack App dashboard and navigate to Event Subscriptions.
Enable Event Subscriptions and enter your ngrok URL as the Request URL (e.g., https://your-ngrok-url.ngrok.io/slack/events).
Subscribe to the event types you want (like message.channels or message.im).

### Test Your Bot
Go to a Slack channel or direct message the bot.
Type in a message, and the bot should respond with an answer from ChatGPT.
