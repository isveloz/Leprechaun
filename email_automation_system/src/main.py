from config_loader import ConfigLoader
from file_monitor import FileMonitor
from email_sender import EmailSender
from gui_interface import GUIInterface
from scheduler import Scheduler
import time
import os
import sys
import threading

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils.logger import setup_logger

def main():
    # Configuración de logs
    setup_logger()

    # Configuraciones predeterminadas (sin JSON)
    schedule = {
        "schedule": [
            {
                "name": "Envio Diario",
                "enabled": True,
                "time": "08:00",
                "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "description": "Envía correos cada día hábil a las 08:00 AM."
            }
        ]
    }

    folder_path = "default_folder"

    # Inicializar componentes
    scheduler = Scheduler(schedule)
    file_monitor = FileMonitor(folder_path)
    email_sender = EmailSender()  # Sin argumentos
    gui = GUIInterface()

    # Simulación de integración con GUI
    def simulate():
        time.sleep(1)
        gui.notify(
            ok=True,
            archivo="archivo_prueba.txt",
            destinatarios=["destino1@ejemplo.com", "destino2@ejemplo.com"],
            duration_s=2.5,
            log="Envío exitoso"
        )

    # Ejecutar GUI
    threading.Thread(target=simulate, daemon=True).start()
    gui.mainloop()

if __name__ == "__main__":
    main()