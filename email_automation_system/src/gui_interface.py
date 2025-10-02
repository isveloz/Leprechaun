import customtkinter as ctk
import time
import threading
from typing import Optional
from email_sender import EmailSender

# Paleta gris simplificada con mejoras
GRAY = {
    "bg":        "#0F0F10",
    "panel":     "#16181C",
    "card":      "#1F2328",
    "border":    "#2A2F36",
    "muted":     "#9BA3AF",
    "text":      "#D0D4DB",
    "text_hi":   "#F2F4F8",
    "btn":       "#2B3138",
    "btn_hover": "#343A43",
    "entry":     "#1B1F24",
    "success":   "#2ECC71",
    "error":     "#E74C3C",
    "warning":   "#F39C12",
}

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_FONT = ("Segoe UI Variable", 12)
TITLE_FONT = ("Segoe UI Variable", 16, "bold")
LABEL_FONT = ("Segoe UI Variable", 12)
BUTTON_FONT = ("Segoe UI Variable", 13, "bold")
SP = 8

def center(win, w=480, h=320):
    """Centra la ventana en la pantalla"""
    win.update_idletasks()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x, y = int((sw - w)/2), int((sh - h)/2.5)
    win.geometry(f"{w}x{h}+{x}+{y}")

class GUIInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Interfaz de Envío de Correos")
        self.configure(fg_color=GRAY["bg"])
        center(self, 480, 320)
        
        # Estado
        self.sending = False
        self.log_completo = ""
        
        # Construir UI
        self._build_header()
        self._build_card()
        self._build_buttons()
        
        # Inicializar estado
        self._update_status("Esperando...", "neutral")

    def _build_header(self):
        """Construye el encabezado con título e indicador de estado"""
        header = ctk.CTkFrame(self, fg_color=GRAY["panel"], corner_radius=10)
        header.pack(fill="x", padx=SP*2, pady=(SP*2, SP))
        
        ctk.CTkLabel(
            header, 
            text="Confirmación de Envío", 
            font=TITLE_FONT, 
            text_color=GRAY["text_hi"]
        ).pack(side="left", padx=(SP*2, 0), pady=SP*1.5)
        
        # Indicador de estado visual
        self.status_indicator = ctk.CTkLabel(
            header,
            text="●",
            font=("Segoe UI Variable", 20),
            text_color=GRAY["muted"]
        )
        self.status_indicator.pack(side="right", padx=(0, SP*2), pady=SP*1.5)

    def _build_card(self):
        """Construye la tarjeta con información del envío"""
        card = ctk.CTkFrame(
            self, 
            fg_color=GRAY["card"], 
            corner_radius=12, 
            border_color=GRAY["border"], 
            border_width=1
        )
        card.pack(fill="x", padx=SP*2, pady=SP)
        
        # Crear filas de información
        self.val_estado = self._create_info_row(card, "Estado:")
        self.val_archivo = self._create_info_row(card, "Archivo:")
        self.val_destinat = self._create_info_row(card, "Destinatarios:")
        self.val_duracion = self._create_info_row(card, "Duración:")
        
        # Barra de progreso (inicialmente oculta)
        self.progress_bar = ctk.CTkProgressBar(
            card,
            fg_color=GRAY["entry"],
            progress_color=GRAY["success"]
        )
        self.progress_bar.pack(fill="x", padx=SP*2, pady=(SP, SP*2))
        self.progress_bar.set(0)
        self.progress_bar.pack_forget()

    def _create_info_row(self, parent, label_text: str) -> ctk.CTkLabel:
        """Crea una fila de información con etiqueta y valor"""
        row = ctk.CTkFrame(parent, fg_color=GRAY["card"])
        row.pack(fill="x", padx=SP*2, pady=(SP, 0))
        
        ctk.CTkLabel(
            row, 
            text=label_text, 
            font=LABEL_FONT, 
            text_color=GRAY["muted"]
        ).pack(side="left")
        
        value_label = ctk.CTkLabel(
            row, 
            text="—", 
            font=LABEL_FONT, 
            text_color=GRAY["text_hi"]
        )
        value_label.pack(side="right")
        
        return value_label

    def _build_details(self):
        """Construye el área de detalles expandible"""
        self.detalle_frame = ctk.CTkFrame(
            self, 
            fg_color=GRAY["card"], 
            corner_radius=10,
            border_color=GRAY["border"],
            border_width=1
        )
        
        # Encabezado de detalles
        detail_header = ctk.CTkFrame(self.detalle_frame, fg_color=GRAY["card"])
        detail_header.pack(fill="x", padx=SP, pady=(SP, 0))
        
        ctk.CTkLabel(
            detail_header,
            text="Información Detallada",
            font=("Segoe UI Variable", 11, "bold"),
            text_color=GRAY["text"]
        ).pack(side="left", padx=SP)
        
        # Área de texto
        self.detalle_text = ctk.CTkTextbox(
            self.detalle_frame, 
            fg_color=GRAY["entry"], 
            text_color=GRAY["text_hi"],
            font=("Consolas", 10),
            height=120
        )
        self.detalle_text.pack(fill="both", expand=True, padx=SP, pady=SP)
        self.detalle_text.configure(state="disabled")

    def _build_buttons(self):
        """Construye los botones de acción"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=SP*2)
        
        ctk.CTkButton(
            button_frame,
            text="📋 Ver Detalles",
            command=self.abrir_ventana_detalles,
            fg_color=GRAY["btn"],
            hover_color=GRAY["btn_hover"],
            text_color=GRAY["text"],
            corner_radius=10,
            height=36,
            width=140
        ).pack(side="left", padx=(0, SP))
        
        ctk.CTkButton(
            button_frame,
            text="Cerrar",
            command=self.destroy,
            fg_color=GRAY["btn"],
            hover_color=GRAY["btn_hover"],
            text_color=GRAY["text"],
            corner_radius=10,
            height=36,
            width=100
        ).pack(side="left")

    def toggle_detalle(self):
        """Alterna la visibilidad del panel de detalles"""
        if self.detalle_visible:
            self.detalle_frame.pack_forget()
            self.btn_detalles.configure(text="▼ Ver Detalles")
            center(self, 480, 420)
        else:
            self.detalle_frame.pack(fill="both", expand=True, padx=SP*2, pady=(0, SP))
            self.btn_detalles.configure(text="▲ Ocultar Detalles")
            center(self, 480, 600)
            self._update_details()
        
        self.detalle_visible = not self.detalle_visible

    def _update_details(self):
        """Actualiza el contenido del área de detalles"""
        info = (
            f"Estado: {self.val_estado.cget('text')}\n"
            f"Archivo: {self.val_archivo.cget('text')}\n"
            f"Destinatarios: {self.val_destinat.cget('text')}\n"
            f"Duración: {self.val_duracion.cget('text')}\n"
            f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        
        self.detalle_text.configure(state="normal")
        self.detalle_text.delete("1.0", "end")
        self.detalle_text.insert("1.0", info)
        self.detalle_text.configure(state="disabled")

    def _update_status(self, status: str, status_type: str = "neutral"):
        """Actualiza el indicador de estado visual"""
        colors = {
            "success": GRAY["success"],
            "error": GRAY["error"],
            "warning": GRAY["warning"],
            "neutral": GRAY["muted"],
            "sending": GRAY["warning"]
        }
        self.status_indicator.configure(text_color=colors.get(status_type, GRAY["muted"]))

    def send_email(self, destinatarios: list[str], archivo: str, archivo_path: str):
        """Envía el correo electrónico con animación de progreso"""
        if self.sending:
            return
        
        self.sending = True
        self.progress_bar.pack(fill="x", padx=SP*2, pady=(SP, SP*2))
        self._update_status("Enviando...", "sending")
        self.val_estado.configure(text="Enviando...")
        
        def send_thread():
            sender = EmailSender()
            try:
                start_time = time.time()
                
                # Simular progreso
                for i in range(5):
                    self.progress_bar.set((i + 1) / 5)
                    time.sleep(0.2)
                
                sender.send_email_with_attachment(
                    destinatarios,
                    'Prueba desde GUI',
                    'Correo enviado desde la interfaz gráfica.',
                    attachments=None,
                    images=[archivo_path]
                )
                
                duration = time.time() - start_time
                self.after(0, lambda: self.notify(True, archivo, destinatarios, duration, 'Correo enviado exitosamente.'))
                
            except Exception as e:
                self.after(0, lambda: self.notify(False, archivo, destinatarios, 0, f"Error: {str(e)}"))
            
            finally:
                self.sending = False
                self.after(100, lambda: self.progress_bar.pack_forget())
        
        threading.Thread(target=send_thread, daemon=True).start()

    def notify(self, ok: bool, archivo: str, destinatarios: list[str], duration_s: float, log: str):
        """Notifica el resultado del envío"""
        estado_txt = "✓ Éxito" if ok else "✗ Error"
        status_type = "success" if ok else "error"
        
        self._update_status(estado_txt, status_type)
        self.val_estado.configure(
            text=estado_txt,
            text_color=GRAY["success"] if ok else GRAY["error"]
        )
        self.val_archivo.configure(text=archivo or "—")
        self.val_destinat.configure(text=f"{len(destinatarios)} destinatario(s)")
        self.val_duracion.configure(text=f"{duration_s:.2f}s" if duration_s > 0 else "—")
        
        # Guardar información completa para la ventana de detalles
        self.log_completo = (
            f"{'='*50}\n"
            f"REPORTE DE ENVÍO\n"
            f"{'='*50}\n\n"
            f"Estado: {estado_txt}\n"
            f"Archivo: {archivo or 'N/A'}\n"
            f"Destinatarios ({len(destinatarios)}):\n"
        )
        for i, dest in enumerate(destinatarios, 1):
            self.log_completo += f"  {i}. {dest}\n"
        
        self.log_completo += (
            f"\nDuración: {duration_s:.2f}s\n"
            f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"{'='*50}\n"
            f"LOG DETALLADO\n"
            f"{'='*50}\n"
            f"{log}\n"
        )

    def abrir_ventana_detalles(self):
        """Abre una ventana separada con información detallada"""
        # Crear ventana independiente
        ventana_detalles = ctk.CTkToplevel(self)
        ventana_detalles.title("Detalles del Envío")
        ventana_detalles.configure(fg_color=GRAY["bg"])
        center(ventana_detalles, 600, 500)
        ventana_detalles.resizable(True, True)
        
        # Header
        header = ctk.CTkFrame(ventana_detalles, fg_color=GRAY["panel"], corner_radius=10)
        header.pack(fill="x", padx=SP*2, pady=(SP*2, SP))
        
        ctk.CTkLabel(
            header,
            text="📋 Detalles Completos del Envío",
            font=TITLE_FONT,
            text_color=GRAY["text_hi"]
        ).pack(side="left", padx=SP*2, pady=SP*1.5)
        
        # Frame principal con scroll
        main_frame = ctk.CTkFrame(
            ventana_detalles,
            fg_color=GRAY["card"],
            corner_radius=12,
            border_color=GRAY["border"],
            border_width=1
        )
        main_frame.pack(fill="both", expand=True, padx=SP*2, pady=SP)
        
        # Resumen rápido
        resumen_frame = ctk.CTkFrame(main_frame, fg_color=GRAY["panel"], corner_radius=8)
        resumen_frame.pack(fill="x", padx=SP*2, pady=SP*2)
        
        ctk.CTkLabel(
            resumen_frame,
            text="Resumen Rápido",
            font=("Segoe UI Variable", 12, "bold"),
            text_color=GRAY["text_hi"]
        ).pack(anchor="w", padx=SP*2, pady=(SP, 4))
        
        # Info en grid
        info_grid = ctk.CTkFrame(resumen_frame, fg_color=GRAY["panel"])
        info_grid.pack(fill="x", padx=SP*2, pady=(0, SP))
        
        self._crear_fila_info(info_grid, "Estado:", self.val_estado.cget('text'), 0)
        self._crear_fila_info(info_grid, "Archivo:", self.val_archivo.cget('text'), 1)
        self._crear_fila_info(info_grid, "Destinatarios:", self.val_destinat.cget('text'), 2)
        self._crear_fila_info(info_grid, "Duración:", self.val_duracion.cget('text'), 3)
        
        # Separador
        ctk.CTkFrame(main_frame, fg_color=GRAY["border"], height=1).pack(fill="x", padx=SP*2, pady=SP)
        
        # Log completo
        ctk.CTkLabel(
            main_frame,
            text="Log Completo",
            font=("Segoe UI Variable", 12, "bold"),
            text_color=GRAY["text_hi"]
        ).pack(anchor="w", padx=SP*2, pady=(SP, 4))
        
        # Área de texto con scroll
        text_frame = ctk.CTkFrame(main_frame, fg_color=GRAY["entry"], corner_radius=8)
        text_frame.pack(fill="both", expand=True, padx=SP*2, pady=(0, SP*2))
        
        texto_log = ctk.CTkTextbox(
            text_frame,
            fg_color=GRAY["entry"],
            text_color=GRAY["text_hi"],
            font=("Consolas", 10),
            wrap="word"
        )
        texto_log.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Insertar log completo
        texto_log.insert("1.0", self.log_completo if self.log_completo else "No hay información disponible aún.")
        texto_log.configure(state="disabled")
        
        # Botones
        btn_frame = ctk.CTkFrame(ventana_detalles, fg_color="transparent")
        btn_frame.pack(pady=SP*2)
        
        ctk.CTkButton(
            btn_frame,
            text="Copiar Log",
            command=lambda: self._copiar_al_portapapeles(ventana_detalles),
            fg_color=GRAY["btn"],
            hover_color=GRAY["btn_hover"],
            text_color=GRAY["text"],
            corner_radius=10,
            height=36,
            width=120
        ).pack(side="left", padx=(0, SP))
        
        ctk.CTkButton(
            btn_frame,
            text="Cerrar",
            command=ventana_detalles.destroy,
            fg_color=GRAY["btn"],
            hover_color=GRAY["btn_hover"],
            text_color=GRAY["text"],
            corner_radius=10,
            height=36,
            width=100
        ).pack(side="left")
    
    def _crear_fila_info(self, parent, label: str, valor: str, row: int):
        """Crea una fila de información en grid"""
        ctk.CTkLabel(
            parent,
            text=label,
            font=LABEL_FONT,
            text_color=GRAY["muted"]
        ).grid(row=row, column=0, sticky="w", padx=(SP, SP*2), pady=4)
        
        ctk.CTkLabel(
            parent,
            text=valor,
            font=LABEL_FONT,
            text_color=GRAY["text_hi"]
        ).grid(row=row, column=1, sticky="w", pady=4)
    
    def _copiar_al_portapapeles(self, ventana):
        """Copia el log completo al portapapeles"""
        try:
            ventana.clipboard_clear()
            ventana.clipboard_append(self.log_completo)
            
            # Mostrar notificación temporal
            notif = ctk.CTkLabel(
                ventana,
                text="✓ Log copiado al portapapeles",
                font=LABEL_FONT,
                text_color=GRAY["success"],
                fg_color=GRAY["panel"],
                corner_radius=6
            )
            notif.place(relx=0.5, rely=0.95, anchor="center")
            
            # Ocultar después de 2 segundos
            ventana.after(2000, notif.destroy)
        except:
            pass

if __name__ == "__main__":
    app = GUIInterface()
    
    # Simulación de envío para pruebas
    def simular_envio():
        time.sleep(1)
        destinatarios = ['automatizacionesmarketing.f@gmail.com', 'isaiasveloz41@gmail.com']
        archivo = 'media.jpg'
        archivo_path = f'C:/Users/idveloz/Desktop/carpeta base/{archivo}'
        app.send_email(destinatarios, archivo, archivo_path)
    
    threading.Thread(target=simular_envio, daemon=True).start()
    app.mainloop()