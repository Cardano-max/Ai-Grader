import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


sg = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
FROM_EMAIL = "contact@teachermate.ai"

def send_email(to, subject, body):
    """
    Send 
    """
    try:
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=to,
            subject=subject,
            html_content=body)

        response = sg.send(message)
        print(response)
        return True
    except Exception as ex:
        print(ex)
        return False