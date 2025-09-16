import requests

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def send_slack_message(text):
    payload = {"text": text}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload)
    except Exception as e:
        print("Slack send error:", e)


