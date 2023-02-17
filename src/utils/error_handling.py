from .slack_notification import send_slack_message
import os

class ErrorHandling:
    def __init__(self, type, category):
        self.type = type
        self.category = category
        
    def print_error(self,error):
        # print in terminal
        print(f'{self.type} - {error}')
        return f'{self.type} - {error}'
        
    def send_slack_notification(self, payload):
        # send slack notification
        if os.environ.get("SLACK_WEBHOOK") == '' or os.environ.get("SLACK_WEBHOOK") == None:
            self.print_error('ERROR: SLACK_WEBHOOK variable not found')
            return
        webhook = os.environ.get("SLACK_WEBHOOK")

        send_slack_message(payload, webhook)