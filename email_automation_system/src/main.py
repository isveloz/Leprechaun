from src.config_loader import ConfigLoader
from src.file_monitor import FileMonitor
from src.email_sender import EmailSender
from src.gui_interface import GUIInterface
from src.scheduler import Scheduler
from utils.logger import setup_logger
import time
import os

def main():
    # Configuración de logs
    setup_logger()

    # Cargar configuraciones
    config = ConfigLoader(
        settings_path="config/settings.json",
        email_path="config/email_config.json",
        schedule_path="config/schedule_config.json"
    )
    email_settings = config.get_email_settings()
    schedule = config.get_schedule()
    folder_path = config.get_folder_path()

    # Inicializar componentes
    scheduler = Scheduler(schedule)
    file_monitor = FileMonitor(folder_path)
    email_sender = EmailSender(email_settings)
    gui = GUIInterface()

    while True:
        # Verificar si es la hora programada
        if not scheduler.is_scheduled_time():
            time.sleep(60)
            continue

        # Mostrar GUI de confirmación
        if not gui.show_confirmation():
            continue

        # Buscar archivos en carpeta de entrada
        files = file_monitor.get_files()
        if not files:
            gui.show_no_files()
            continue

        # Mostrar lista de archivos y countdown
        gui.show_files(files)
        if gui.countdown_cancel(10):
            gui.cancel_process()
            continue

        # Intentar enviar archivos
        for file in files:
            try:
                result = email_sender.send_email_with_attachment(file)
                if result:
                    gui.show_success()
                    gui.auto_close(3)
                    # Mover archivo a carpeta sent/archive
                    file_monitor.move_to_sent(file)
                else:
                    gui.show_error()
                    gui.wait_for_close()
                    # Mover archivo a carpeta failed/retry
                    file_monitor.move_to_failed(file)
            except Exception as e:
                gui.show_error()
                gui.wait_for_close()
                file_monitor.move_to_failed(file)

        # Decidir si salir o volver a monitoreo
        if gui.should_exit():
            break

if __name__ == "__main__":
    main()