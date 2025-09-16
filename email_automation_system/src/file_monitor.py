import os
from pathlib import Path

class FileMonitor:
    def __init__(self, folder_path):
        self.folder_path = Path(folder_path)

    def get_files(self):
        try:
            if not self.folder_path.exists():
                print(f"La carpeta {self.folder_path} no existe.")
                return []

            return [str(file) for file in self.folder_path.iterdir() if file.is_file()]
        except Exception as e:
            print(f"Error al obtener archivos de {self.folder_path}: {e}")
            return []

    def move_to_sent(self, file_path):
        self._move_file(file_path, "sent/archive")

    def move_to_failed(self, file_path):
        self._move_file(file_path, "failed/retry")

    def _move_file(self, file_path, target_subfolder):
        try:
            target_folder = self.folder_path / target_subfolder
            target_folder.mkdir(parents=True, exist_ok=True)
            target_path = target_folder / Path(file_path).name
            Path(file_path).rename(target_path)
            print(f"Archivo movido a {target_path}")
        except Exception as e:
            print(f"Error al mover el archivo {file_path} a {target_subfolder}: {e}")

