import json
import os

class ConfigLoader:
    def __init__(self, settings_path, email_path, schedule_path):
        self.settings_path = settings_path
        self.email_path = email_path
        self.schedule_path = schedule_path

    def get_settings(self):
        return self._load_json(self.settings_path)

    def get_email_settings(self):
        return self._load_json(self.email_path)

    def get_schedule(self):
        return self._load_json(self.schedule_path)

    def _load_json(self, path):
        try:
            abs_path = os.path.abspath(path)
            with open(abs_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File not found at {path}")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {path}")
        except Exception as e:
            print(f"Error loading configuration from {path}: {e}")
        return None

