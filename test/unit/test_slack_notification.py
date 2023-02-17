from mock import patch 
from utils.slack_notification import send_slack_message

@patch('utils.slack_notification.send_slack_message', return_value=200)
def test_slack_notification(mock_send_to_slack):
    res = mock_send_to_slack()
    
    assert mock_send_to_slack.call_count == 1
    assert res == 200
