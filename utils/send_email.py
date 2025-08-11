import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

def send_status_email(applicant_email: str, applicant_name: str, status_data: dict, job_title: str) -> bool:
    subject = f"Application Status for {job_title}"
    content = f"""
    Hi {applicant_name},

    Your application for "{job_title}" has been processed.

    Match Score: {status_data.get('match_score')}
    Status: {status_data.get('status')}
    Feedback: {status_data.get('feedback')}

    Thank you for applying!
    """

    message = Mail(
        from_email='zelalem.t8@gmail.com',
        to_emails=applicant_email,
        subject=subject,
        plain_text_content=content
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        print(f"SendGrid error: {e}")
        return False