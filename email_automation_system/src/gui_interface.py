
import customtkinter as ctk
import threading
import time
import os

# Colores corporativos Falabella
FALABELLA_GREEN = "#78be20"
FALABELLA_YELLOW = "#ffcc00"
FALABELLA_WHITE = "#ffffff"
FALABELLA_DARK = "#222222"


class EmailAutomationGUI:
	def __init__(self, root):
		self.root = root
		self.root.title(" Sistema automatico de Correos - Marketing Digital")
		self.root.geometry("540x600")
		ctk.set_appearance_mode("dark")
		self.root.configure(fg_color=FALABELLA_DARK)

		# Variables de control
		self.files_list = []
		self.countdown_active = False
		self.folder_path = r"C:\Users\idveloz\Desktop\carpeta base"

		# Crear widgets
		self.create_widgets()
		self.scan_files()

	def create_widgets(self):
		# Header con logo y título
		self.header_frame = ctk.CTkFrame(self.root, fg_color=FALABELLA_GREEN, corner_radius=16, height=70)
		self.header_frame.pack(fill="x", padx=18, pady=(18, 10))
		self.header_frame.pack_propagate(False)

		self.title_label = ctk.CTkLabel(self.header_frame, text="Automatización de Envío de Correos", text_color=FALABELLA_DARK, font=("Segoe UI", 22, "bold"), fg_color="transparent")
		self.title_label.pack(side="left", padx=(18, 0), pady=10)

		# Frame para la hora programada
		self.time_frame = ctk.CTkFrame(self.root, fg_color=FALABELLA_WHITE, corner_radius=14)
		self.time_frame.pack(fill="x", padx=18, pady=(0, 10))

		self.time_label = ctk.CTkLabel(self.time_frame, text="Hora actual: --:--", text_color=FALABELLA_DARK, font=("Segoe UI", 14, "bold"), fg_color="transparent")
		self.time_label.pack(pady=(10, 0))

		self.confirm_button = ctk.CTkButton(self.time_frame, text="Confirmar Hora", fg_color=FALABELLA_YELLOW, hover_color="#ffe066", text_color=FALABELLA_DARK, corner_radius=10, font=("Segoe UI", 13, "bold"), command=self.confirm_time)
		self.confirm_button.pack(pady=10)

		# Frame para la lista de archivos
		self.files_frame = ctk.CTkFrame(self.root, fg_color=FALABELLA_DARK, corner_radius=14, border_color=FALABELLA_GREEN, border_width=2)
		self.files_frame.pack(fill="both", padx=18, pady=10, expand=True)

		self.files_label = ctk.CTkLabel(self.files_frame, text="Archivos Encontrados", text_color=FALABELLA_GREEN, font=("Segoe UI", 15, "bold"), fg_color="transparent")
		self.files_label.pack(pady=(10, 0))

		self.files_text = ctk.CTkTextbox(self.files_frame, height=140, fg_color=FALABELLA_WHITE, text_color=FALABELLA_DARK, font=("Consolas", 12), corner_radius=8, border_color=FALABELLA_YELLOW, border_width=1)
		self.files_text.pack(fill="both", expand=True, padx=10, pady=10)
		self.files_text.configure(state="disabled")

		# Frame para el countdown
		self.countdown_frame = ctk.CTkFrame(self.root, fg_color=FALABELLA_GREEN, corner_radius=14)
		self.countdown_frame.pack(fill="x", padx=18, pady=10)

		self.countdown_label = ctk.CTkLabel(self.countdown_frame, text="Listo para enviar...", text_color=FALABELLA_DARK, font=("Segoe UI", 14, "bold"), fg_color="transparent")
		self.countdown_label.pack(pady=10)

		# Frame para los botones de acción
		self.action_frame = ctk.CTkFrame(self.root, fg_color="transparent")
		self.action_frame.pack(fill="x", padx=18, pady=(10, 18))

		self.send_button = ctk.CTkButton(self.action_frame, text="Enviar Correos", fg_color=FALABELLA_GREEN, hover_color=FALABELLA_YELLOW, text_color=FALABELLA_DARK, border_color=FALABELLA_YELLOW, border_width=2, corner_radius=18, font=("Segoe UI", 15, "bold"), height=38, command=self.start_countdown)
		self.send_button.pack(side="left", padx=7, pady=10, ipadx=8)

		self.cancel_button = ctk.CTkButton(self.action_frame, text="Cancelar", fg_color=FALABELLA_DARK, hover_color="#444444", text_color=FALABELLA_WHITE, border_color=FALABELLA_GREEN, border_width=2, corner_radius=18, font=("Segoe UI", 15), height=38, command=self.cancel_process)
		self.cancel_button.pack(side="left", padx=7, pady=10, ipadx=8)

		self.close_button = ctk.CTkButton(self.action_frame, text="Cerrar", fg_color=FALABELLA_YELLOW, hover_color="#ffe066", text_color=FALABELLA_DARK, border_color=FALABELLA_GREEN, border_width=2, corner_radius=18, font=("Segoe UI", 15), height=38, command=self.root.quit)
		self.close_button.pack(side="right", padx=7, pady=10, ipadx=8)

	def confirm_time(self):
		self.scan_files()
		self.show_popup("Hora confirmada. Archivos encontrados.")

	def scan_files(self):
		"""Escanea la carpeta base y actualiza la lista de archivos."""
		if os.path.exists(self.folder_path) and os.path.isdir(self.folder_path):
			self.files_list = [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]
		else:
			self.files_list = []
		self.update_files_list()

	def update_files_list(self):
		self.files_text.configure(state="normal")
		self.files_text.delete("1.0", "end")
		for file in self.files_list:
			self.files_text.insert("end", f"- {file}\n")
		self.files_text.configure(state="disabled")

	def start_countdown(self):
		if not self.files_list:
			self.show_popup("No hay archivos para enviar.", error=True)
			return
		self.countdown_active = True
		self.countdown_label.configure(text="Enviando en 10 segundos...")
		threading.Thread(target=self.run_countdown, daemon=True).start()

	def run_countdown(self):
		for i in range(10, 0, -1):
			if not self.countdown_active:
				return
			self.countdown_label.configure(text=f"Enviando en {i} segundos...")
			time.sleep(1)
		self.send_emails()

	def send_emails(self):
		self.countdown_label.configure(text="Enviando correos...")
		self.show_popup("Correos enviados correctamente.", success=True)

	def cancel_process(self):
		self.countdown_active = False
		self.countdown_label.configure(text="Proceso cancelado.")

	def show_popup(self, message, success=False, error=False):
		popup = ctk.CTkToplevel(self.root)
		popup.geometry("360x150")
		popup.title("Mensaje")
		color = FALABELLA_GREEN if success else (FALABELLA_YELLOW if error else FALABELLA_DARK)
		popup.configure(fg_color=color)
		label = ctk.CTkLabel(popup, text=message, text_color=FALABELLA_DARK if color != FALABELLA_DARK else FALABELLA_WHITE, font=("Segoe UI", 16, "bold"), fg_color="transparent")
		label.pack(pady=(32, 12), padx=24, fill="x")
		btn_ok = ctk.CTkButton(popup, text="Aceptar", fg_color=FALABELLA_WHITE, hover_color=FALABELLA_GREEN, text_color=FALABELLA_DARK, corner_radius=14, font=("Segoe UI", 13, "bold"), command=popup.destroy)
		btn_ok.pack(pady=10)
		popup.transient(self.root)
		popup.grab_set()
		self.root.wait_window(popup)

# Ejecutar la interfaz
if __name__ == "__main__":
	root = ctk.CTk()
	app = EmailAutomationGUI(root)
	root.mainloop()