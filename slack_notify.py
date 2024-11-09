# Send Slack Notification
    email = demisto.args().get('email')
    if email:
        send_slack_notification = demisto.executeCommand("send-notification", {"message":readable_output,"to":email})
