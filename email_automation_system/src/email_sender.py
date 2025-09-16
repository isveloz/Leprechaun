import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from pathlib import Path
from dotenv import load_dotenv
import os
from email.utils import encode_rfc2231
import pytz
from datetime import datetime
from email.header import Header

# Load environment variables
load_dotenv()

class EmailSender:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.username = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL")
        self.timezone = pytz.timezone("America/Santiago")

    def send_email_with_attachment(self, to_emails, subject, body, attachments=None, images=None):
        try:
            print(f"Servidor SMTP: {self.smtp_server}")
            print(f"Puerto: {self.smtp_port}")
            print(f"Usuario: {self.username}")

            # Crear el mensaje
            msg = MIMEMultipart()
            msg['From'] = str(Header(self.from_email, 'utf-8'))
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = str(Header(subject, 'utf-8'))

            # Agregar cuerpo del mensaje con codificacion UTF-8
            msg.attach(MIMEText(body, 'html', 'utf-8'))

            # Agregar archivos adjuntos
            if attachments:
                for file_path in attachments:
                    sanitized_name = Path(file_path).name  # Mantener el nombre original con UTF-8
                    with open(file_path, 'rb') as f:
                        part = MIMEApplication(f.read(), Name=sanitized_name)
                        part.add_header('Content-Disposition', 'attachment', filename=sanitized_name)
                        msg.attach(part)

            # Agregar imagenes embebidas
            if images:
                for image_path in images:
                    try:
                        sanitized_name = Path(image_path).name  # Mantener el nombre original con UTF-8
                        with open(image_path, 'rb') as f:
                            img = MIMEImage(f.read())
                            img.add_header('Content-ID', f'<{sanitized_name}>')
                            msg.attach(img)
                        print(f"Imagen adjuntada correctamente: {sanitized_name}")
                    except Exception as img_error:
                        print(f"Error al adjuntar la imagen {image_path}: {img_error}")

            # Enviar el correo
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                to_emails.extend(['automatizacionesmarketing.f@gmail.com', 'isaiasveloz41@gmail.com', 'mateofn.20@gmail.com'])
                server.sendmail(self.from_email, to_emails, msg.as_string())

            # Registrar el envio con la zona horaria de Santiago, CL
            current_time = datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S")
            print(f"Correo enviado exitosamente a las {current_time} hora local de Santiago, CL")
            return True
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
            return False