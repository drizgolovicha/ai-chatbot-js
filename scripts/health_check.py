import requests
import argparse
from dotenv import load_dotenv
from datetime import datetime

from utils.slack_notificator import slack_post_message

load_dotenv()  # noqa: E402

print(f"{str(datetime.today())}")
parser = argparse.ArgumentParser(description="Healthcheck script for verifying that the AI Agent operates with the correct context.")
parser.add_argument("--host",
                    required=True,
                    default="http://127.0.0.1:8000", type=str,
                    help="Base URL where the AI Agent API is hosted")
args = parser.parse_args()


def healthCheck():
    """
    Perform a health check on the AI Agent API to verify correct context operation.
    
    Sends a test question to the health-check endpoint and validates the response
    to ensure the AI agent is operating with proper context and not returning
    generic "I am not sure" responses.
    
    :raises AssertionError: If the response contains unexpected content indicating
                           incorrect context
    :raises requests.exceptions.RequestException: If the HTTP request fails
    """
    payload = {
        "question": "Is company you represent a software development company?"
    }

    try:
        response = requests.post(f"{args.host}/chat/health-check", json=payload)

        # Check the response status code
        if response.status_code == 200:
            json = response.json()
            content = json.get("response", "").lower()

            assert "hmm, i am not sure" not in content, f"❌ Healthcheck failed: unexpected answer -> {content}"

            message = f"✅ Healthcheck for '{args.host}' passed: context is correct"
            print(message)

            try:
                slack_post_message(message)
            except Exception as ex:
                print(str(ex))
        else:
            print(f"POST request failed with status code: {response.status_code}")
            print("Response content:", response.text)
    except requests.exceptions.RequestException as e:
        message = f"❌ Healthcheck failed: An error occurred during the request: {e}"
        print(message)
        slack_post_message(message)
    except AssertionError as e:
        message = str(e)
        print(message)
        slack_post_message(message)


if __name__ == "__main__":
    healthCheck()
    print('\r\n\r\n')
