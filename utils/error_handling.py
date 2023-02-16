class ErrorHandling:
    def __init__(self, type, category):
        self.type = type
        self.category = category
        
    def print_error(self,error):
        # print in terminal
        print(f'{self.type} - {error}')
        return f'{self.type} - {error}'
        
    def send_slack_notification(self):
        # send slack notification
        print('to be done')