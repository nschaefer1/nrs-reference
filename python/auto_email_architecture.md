
# Automatic Emailing Architecture

The `password` element in this code is an **App Password**. It's recommended to use a provider like google. This App Password should be stored in an environment variable and *not* in your core code.

**Recommended Domain**: *Google*.  
This can be done by going to Google > User Settings > App Passwords.  
It's *critical* to have Two-Factor authentication enabled.

```python
import smtplib
import os

from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

sender = "sender@domain.com"                            # ← change who is sending the email
password = os.getenv("APP_PASS")
receiver = "receiver@domain.com"                        # ← change who is receiving the email

msg = MIMEText("Test Email Body")
msg["Subject"] = "Test Email"
msg["From"] = sender
msg["To"] = receiver

with smtplib.SMTP("smtp.gmail.com", 587) as server:     # ← may need to change your domain
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender, password)
    server.send_message(msg)

print("Email sent")
```