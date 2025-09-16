import customtkinter as ctk
import time
import threading

# Paleta gris simplificada           
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
    "success":   "#1E2A1E",
    "error":     "#2A1E1E",
}

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_FONT = ("Segoe UI Variable", 12)
TITLE_FONT = ("Segoe UI Variable", 16, "bold")
LABEL_FONT = ("Segoe UI Variable", 12)
BUTTON_FONT = ("Segoe UI Variable", 13, "bold")
SP = 8

def center(win, w=480, h=320):
    win.update_idletasks()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x, y = int((sw - w)/2), int((sh - h)/2.5)
    win.geometry(f"{w}x{h}+{x}+{y}")

class ModalSimple(ctk.CTkToplevel):
    """Modal sencillo con OK y Ver más, tamaño compacto."""
    def __init__(self, master, resumen, detalle):
        super().__init__(master)
        self.title("Resultado del envío")
        self.configure(fg_color=GRAY["card"])
        center(self, 440, 220)
        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text="Resultado", font=TITLE_FONT, text_color=GRAY["text_hi"])\
            .grid(row=0, column=0, sticky="w", padx=SP*2, pady=(SP*2, SP))

        ctk.CTkLabel(self, text=resumen, font=BASE_FONT, text_color=GRAY["text"])\
            .grid(row=1, column=0, sticky="we", padx=SP*2, pady=(0, SP*2))

        btns = ctk.CTkFrame(self, fg_color=GRAY["card"])
        btns.grid(row=2, column=0, sticky="e", padx=SP*2, pady=(0, SP*2))

        style = dict(font=BUTTON_FONT, fg_color=GRAY["btn"], hover_color=GRAY["btn_hover"],
                     text_color=GRAY["text"], corner_radius=10, height=SP*4)
        ctk.CTkButton(btns, text="Ver más acerca del envío", command=self.ver_mas(detalle), **style)\
            .pack(side="left", padx=(0, SP))
        ctk.CTkButton(btns, text="OK", command=self.destroy, **style)\
            .pack(side="left", padx=(SP, 0))

    def ver_mas(self, detalle):
        def inner():
            d = ctk.CTkToplevel(self)
            d.title("Detalle de envío")
            d.configure(fg_color=GRAY["card"])
            center(d, 500, 300)
            d.transient(self)
            d.grab_set()
            d.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(d, text="Detalle", font=TITLE_FONT, text_color=GRAY["text_hi"])\
                .grid(row=0, column=0, sticky="w", padx=SP*2, pady=(SP*2, SP))
            tb = ctk.CTkTextbox(d, fg_color=GRAY["entry"], text_color=GRAY["text_hi"],
                                font=("Consolas", 11), height=8)
            tb.grid(row=1, column=0, sticky="nsew", padx=SP*2, pady=(0, SP*2))
            tb.insert("1.0", detalle)
            tb.configure(state="disabled")
            btn_style = dict(font=BUTTON_FONT, fg_color=GRAY["btn"], hover_color=GRAY["btn_hover"],
                             text_color=GRAY["text"], corner_radius=10, height=SP*4)
            ctk.CTkButton(d, text="Cerrar", command=d.destroy, **btn_style)\
                .grid(row=2, column=0, sticky="e", padx=SP*2, pady=(0, SP*2))
        return inner


class ConfirmacionVisual(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("")
        self.configure(fg_color=GRAY["bg"])
        center(self, 480, 320)

        # Valores de estado
        self.val_estado = None
        self.val_archivo = None
        self.val_destinat = None
        self.val_duracion = None

        # UI simple
        header = ctk.CTkFrame(self, fg_color=GRAY["panel"], corner_radius=10)
        header.pack(fill="x", padx=SP*2, pady=(SP*2, SP))
        ctk.CTkLabel(header, text="Confirmación de envio", font=TITLE_FONT, text_color=GRAY["text_hi"])\
            .pack(side="left", padx=(SP*2, 0), pady=SP*1.5)

        card = ctk.CTkFrame(self, fg_color=GRAY["card"], corner_radius=12, border_color=GRAY["border"], border_width=1)
        card.pack(fill="both", expand=True, padx=SP*2, pady=SP)

        # Etiquetas/read-only
        def make_row(parent, text_label):
            row = ctk.CTkFrame(parent, fg_color=GRAY["card"])
            row.pack(fill="x", padx=SP*2, pady=(0, SP))
            lbl = ctk.CTkLabel(row, text=text_label, font=LABEL_FONT, text_color=GRAY["muted"])
            val = ctk.CTkLabel(row, text="—", font=LABEL_FONT, text_color=GRAY["text_hi"])
            lbl.pack(side="left")
            val.pack(side="right")
            return val

        self.val_estado   = make_row(card, "Estado:")
        self.val_archivo  = make_row(card, "Archivo:")
        self.val_destinat = make_row(card, "Destinatarios:")
        self.val_duracion = make_row(card, "Duración:")

    def notify(self, ok: bool, archivo: str, destinatarios: list[str], duration_s: float, log: str):
        estado_txt = "Éxito" if ok else "Error"
        self.val_estado.configure(text=estado_txt, text_color=GRAY["text_hi"])
        self.val_archivo.configure(text=archivo or "—")
        self.val_destinat.configure(text=", ".join(destinatarios))
        self.val_duracion.configure(text=f"{duration_s:.2f}s")

        resumen = "Envío completado." if ok else "Se produjo un error."
        detalle = f"Archivo: {archivo}\nDestinatarios: {', '.join(destinatarios)}\nDuración: {duration_s:.2f}s\n\nLog:\n{log}"
        ModalSimple(self, resumen, detalle)

if __name__ == "__main__":
    app = ConfirmacionVisual()
    # Simulación para probar
    def sim():
        time.sleep(1)
        app.notify(True, "ejemplo.txt", ["a@ejemplo.com", "b@ejemplo.com"], 2.45, "SMTP OK\nHecho")
    threading.Thread(target=sim, daemon=True).start()
    app.mainloop()
