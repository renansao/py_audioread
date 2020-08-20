import email, smtplib, ssl
import os

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email():
    sender_email = os.environ.get("EMAIL_APNEA_SLEEP")
    email_password = os.environ.get("PASSWORD_EMAIL_APNEA_SLEEP")
    receiver_email = "gabrielbnetto@gmail.com"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Bcc"] = receiver_email
    message["Subject"] = "ApneaSleep Relatório"

    filename = "ApneaSleep - Relatorio.pdf" 
    body = "Olá. \n \n Aqui está o relatório que você solicitou! \n Qualquer dúvida ou problema, entre em contato! \n \n Ass: Equipe ApneaSleep"

    message.attach(MIMEText(body, "plain"))

    with open(filename, "rb") as attachment:
        pdfData = attachment.read()
    
    part = MIMEApplication(pdfData, _subtype="pdf", _encoder=encoders.encode_base64)
    part.add_header('content-disposition', 'attachment',  filename= filename)
    message.attach(part)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

