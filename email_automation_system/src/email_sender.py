import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class EmailSender:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL")

    def send_email_with_attachment(self, to_emails, subject, body, attachments=None, images=None):
        try:
            # Crear el mensaje
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = subject

            # Agregar cuerpo del mensaje
            msg.attach(MIMEText(body, 'html'))

            # Agregar archivos adjuntos
            if attachments:
                for file_path in attachments:
                    with open(file_path, 'rb') as f:
                        part = MIMEApplication(f.read(), Name=Path(file_path).name)
                        part['Content-Disposition'] = f'attachment; filename="{Path(file_path).name}"'
                        msg.attach(part)

            # Agregar imágenes embebidas
            if images:
                for image_path in images:
                    with open(image_path, 'rb') as f:
                        img = MIMEImage(f.read())
                        img.add_header('Content-ID', f'<{Path(image_path).name}>')
                        msg.attach(img)

            # Enviar el correo
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.from_email, to_emails, msg.as_string())

            return True
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
            return False