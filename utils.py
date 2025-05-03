import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega o .env aqui também

def enviar_email_confirmacao(email_destino, token):
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    link = f"http://localhost:5000/confirmar_email/{token}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Confirmação de Email - Sist.Login"
    msg["From"] = EMAIL_SENDER
    msg["To"] = email_destino

    corpo = f"""
    <html>
    <body>
        <p>Olá!<br>
        Clique no link abaixo para confirmar seu email:<br>
        <a href="{link}">Confirmar Email</a>
        </p>
    </body>
    </html>
    """
    msg.attach(MIMEText(corpo, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, email_destino, msg.as_string())
        return True
    except Exception as e:
        print("❌ Erro ao enviar email:", e)
        return False
