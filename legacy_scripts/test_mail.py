import smtplib
from email.message import EmailMessage

try:
    msg = EmailMessage()
    msg.set_content("This is an automated local environment test from the Clinical Food AI platform. If you are receiving this, your secure loopback postfix configuration is verified and functioning flawlessly over Port 25!")
    msg['Subject'] = "Local Food AI: Internal Subnet Verification"
    msg['From'] = "system@localfoodaimaster.com"
    msg['To'] = '"Mr Lange François" <flange@pt.lu>'

    # Strict loopback port explicitly targeting postfix configurations to bypass 0.0.0.0 leaks
    s = smtplib.SMTP('localhost', 25)
    s.send_message(msg)
    s.quit()
    print("✅ Email dispatched perfectly via local postfix socket!")
except Exception as e:
    print(f"❌ Failed to reach or broadcast via local SMTP Postfix. Error: {e}")
