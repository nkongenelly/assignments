import requests
import json

def send_slack_message(payload, webhook):
    try:
        res = requests.post(webhook, json.dumps(payload))
        print("Slack message sent")
        return res
    except requests.exceptions as e:
        # imported error handling here to avoid circular import
        from .error_handling import ErrorHandling 
        error_obj = ErrorHandling('PAYLOAD_CONFIG', 'NOTICE')
        error_obj.print_error(e)


