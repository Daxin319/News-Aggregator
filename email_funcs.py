import smtplib
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# function to generate the basic email body
def generate_email_body(news_stories):
    if not news_stories:
        return "No results found."

    body = "Here are today's top news stories:\n\n"
    for story in news_stories:
        body += f"- {story['title']} ({story['source']})\n  {story['url']}\n\n"
    return body

# function to send the email
def send_email(from_email, to_email, subject, body, smtp_server, smtp_port, email_password):
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, email_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Email sent successfully! {now}")
    except Exception as e:
        print(f"Failed to send email: {e}")

#function to check if email address is in proper format (xxxxxxxxx@yyyyy.zzz would pass this check right now, but I don't really care about validating that the email is real, only that it is the proper format for an email to be sent)
def validate_email(string):
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", string):
        print("<------------------------------Invalid email address, please try again------------------------------>")
        return False
    return True