import requests
import os

from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
CHANNEL_ID = os.environ.get('SLACK_BOT_CHANNEL')


def slack_post_message(message: str):
    """
    Send a message to a configured Slack channel.
    
    :param message: The text message to send to Slack
    :return: True if message was sent successfully
    :raises ValueError: If SLACK_BOT_TOKEN or CHANNEL_ID environment variables are missing
    :raises requests.exceptions.HTTPError: If Slack API request fails with HTTP error
    :raises RuntimeError: If Slack API returns an error response
    """
    if not SLACK_BOT_TOKEN or not CHANNEL_ID:
        raise ValueError("Missing Slack configuration: SLACK_BOT_TOKEN or CHANNEL_ID")

    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }

    resp = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers=headers,
        json={"channel": CHANNEL_ID, "text": message}
    )

    if resp.ok is False:
        raise requests.exceptions.HTTPError(
            f"Slack API request failed with status {resp.status_code}: {resp.text}"
        )

    json = resp.json()
    if json.get('ok') is False:
        raise RuntimeError(f"Slack API error: {json}")

    return True
