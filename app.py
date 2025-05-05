# app.py

import os
from flask import Flask, request, Response
from dotenv import load_dotenv

from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from bot import EchoBot

@app.route("/api/test", methods=["GET"])
def test():
    return "Hello, this is a test endpoint!"

# Load environment variables
load_dotenv()

# App credentials from .env
APP_ID = os.getenv("MicrosoftAppId", "")
APP_PASSWORD = os.getenv("MicrosoftAppPassword", "")

print(f"App ID: {APP_ID}")
print(f"App Password: {APP_PASSWORD}")
# Create bot adapter and bot instance
adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)
bot = EchoBot()

# Create Flask app
app = Flask(__name__)

@app.route("/api/messages", methods=["POST"])
async def messages():
    # print("Request headers: ", request.headers)
    # print("Request body: ", request.json)
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

    async def aux(turn_context: TurnContext):
        await bot.on_turn(turn_context)

    task = await adapter.process_activity(activity, auth_header, aux)
    print("--------- TASK ------", task)
    return Response(status=202)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
    
