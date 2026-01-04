import customtkinter as ctk
import threading
import time
import os
from tkinter import filedialog

# --- THEME SETUP ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue") 

# --- PREMIUM PALETTE ---
COLOR_BG = "#0f1012"
COLOR_CARD = "#1a1c21"
COLOR_ACCENT = "#3B8ED0"
COLOR_SUCCESS = "#2cc985"
COLOR_TEXT = "#e1e1e6"
COLOR_TEXT_DIM = "#8d8d99"
COLOR_DIVIDER = "#2b2d31"
COLOR_HOVER = "#232529" 

# --- DUMMY LOGIC ---
try:
    from src.compressor import compress_image
    from src.privacy import strip_metadata
    from src.duplicator import find_and_remove_duplicates
except ImportError:
    def compress_image(*args, **kwargs) -> int: return 0
    def strip_metadata(*args, **kwargs): pass
    def find_and_remove_duplicates(*args, **kwargs) -> tuple[int, int]: return 0, 0

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Stealth Storage | { Quintero_Dev_Studio }")
        self.geometry("1000x720")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)

        self.folder_path = ""
        self.radio_var = ctk.IntVar(value=1)

        self.grid_columnconfigure(0, weight=3, uniform="a") 
        self.grid_columnconfigure(1, weight=7, uniform="a") 
        self.grid_rowconfigure(0, weight=1)

        # ============================================================
        # LEFT PANEL
        # ============================================================
        self.left_frame = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_DIVIDER)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        
        # HEADER
        self.frame_header = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.frame_header.pack(fill="x", pady=(30, 20), padx=20)
        
        self.logo_label = ctk.CTkLabel(self.frame_header, text="⚡ STEALTH\nSTORAGE", font=("Segoe UI", 26, "bold"), text_color=COLOR_TEXT)
        self.logo_label.pack()
        
        ctk.CTkLabel(self.frame_header, text="{ Quintero_Dev_Studio }", text_color=COLOR_ACCENT, font=("Consolas", 12, "bold")).pack(pady=(5, 0))

        ctk.CTkFrame(self.left_frame, height=2, fg_color=COLOR_DIVIDER).pack(fill="x", padx=20, pady=10)

        # 1. DATA SOURCE
        self.frame_source = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.frame_source.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(self.frame_source, text="1. DATA SOURCE", text_color=COLOR_ACCENT, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 10))

        self.btn_folder = ctk.CTkButton(self.frame_source, text="Select Folder", font=("Segoe UI", 13), fg_color="#2b2d31", hover_color="#3e4046", height=40, command=self.select_folder)
        self.btn_folder.pack(fill="x")
        self.lbl_path = ctk.CTkLabel(self.frame_source, text="No folder selected", text_color=COLOR_TEXT_DIM, font=("Segoe UI", 11))
        self.lbl_path.pack(pady=(5, 0))

        # 2. CONFIGURATION
        self.frame_config = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.frame_config.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(self.frame_config, text="2. CONFIGURATION", text_color=COLOR_ACCENT, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 10))

        # CONTENEDOR DE OPCIONES
        self.radio_container = ctk.CTkFrame(self.frame_config, fg_color="transparent")
        self.radio_container.pack(fill="x")

        # CREACIÓN DE OPCIONES CON GRID (Súper Alineación)
        self.create_grid_option(" Full Optimization", 1, "🚀", 0)
        self.create_grid_option("Privacy Only", 2, "🛡️", 1)
        self.create_grid_option(" Compression Only", 3, "📦", 2)
        self.create_grid_option(" Remove Duplicates", 4, "🧹", 3)

        # START BUTTON
        ctk.CTkLabel(self.left_frame, text="").pack(expand=True)
        self.btn_start = ctk.CTkButton(self.left_frame, text="START PROCESS", font=("Segoe UI", 14, "bold"), fg_color=COLOR_ACCENT, height=50, corner_radius=8, state="disabled", command=self.start_process)
        self.btn_start.pack(pady=30, padx=20, fill="x", side="bottom")

        # ============================================================
        # RIGHT PANEL
        # ============================================================
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.status_card = ctk.CTkFrame(self.right_frame, fg_color=COLOR_CARD, corner_radius=12, height=160, border_width=1, border_color=COLOR_DIVIDER)
        self.status_card.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.status_card.grid_propagate(False) 
        ctk.CTkLabel(self.status_card, text="SYSTEM STATUS", text_color=COLOR_TEXT_DIM, font=("Segoe UI", 11, "bold")).pack(pady=(20, 5), padx=25, anchor="w")
        self.lbl_main_status = ctk.CTkLabel(self.status_card, text="Waiting...", text_color=COLOR_TEXT, font=("Segoe UI", 34))
        self.lbl_main_status.pack(pady=5)
        self.progressbar = ctk.CTkProgressBar(self.status_card, height=8)
        self.progressbar.set(0)
        self.progressbar.pack(pady=20, padx=40, fill="x")

        self.log_card = ctk.CTkFrame(self.right_frame, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_DIVIDER)
        self.log_card.grid(row=1, column=0, sticky="nsew")
        ctk.CTkLabel(self.log_card, text="EVENT LOG", text_color=COLOR_TEXT_DIM, font=("Segoe UI", 11, "bold")).pack(pady=(20, 10), padx=25, anchor="w")
        self.log_box = ctk.CTkTextbox(self.log_card, fg_color="#131416", text_color="#00ff9d", font=("Consolas", 12))
        self.log_box.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        self.log_box.configure(state="disabled")

        self.welcome_msg()

    # --- NUEVA FUNCIÓN DE OPCIONES CON GRID ---
    def create_grid_option(self, text, val, icon, row_idx):
        # Frame contenedor
        container = ctk.CTkFrame(self.radio_container, fg_color="transparent", corner_radius=6)
        container.pack(fill="x", pady=2)
        
        # Configuramos las columnas del contenedor para que sean fijas
        container.grid_columnconfigure(0, minsize=35) # Columna para el Radio
        container.grid_columnconfigure(1, minsize=40) # Columna para el Icono (ANCHO FIJO CLAVE)
        container.grid_columnconfigure(2, weight=1)   # Columna para el Texto

        # 1. Radio Button
        r = ctk.CTkRadioButton(container, text="", variable=self.radio_var, value=val, width=20, height=20)
        r.grid(row=0, column=0, padx=(10, 0), pady=10)

        # 2. Icono (Centrado en su columna de 40px)
        icon_lbl = ctk.CTkLabel(container, text=icon, font=("Segoe UI", 16))
        icon_lbl.grid(row=0, column=1, sticky="w")

        # 3. Texto (Empezará siempre en el mismo sitio gracias a minsize de col 1)
        text_lbl = ctk.CTkLabel(container, text=text, font=("Segoe UI", 13), text_color=COLOR_TEXT)
        text_lbl.grid(row=0, column=2, sticky="w")

        # --- EVENTOS PARA SELECCIONAR ---
        def select_opt(event=None): self.radio_var.set(val)
        def on_enter(e): container.configure(fg_color=COLOR_HOVER)
        def on_leave(e): container.configure(fg_color="transparent")

        for widget in [container, icon_lbl, text_lbl]:
            widget.bind("<Button-1>", select_opt)
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"> {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def set_status(self, text, color=COLOR_TEXT):
        self.lbl_main_status.configure(text=text, text_color=color)

    def welcome_msg(self):
        self.log("Stealth Storage System initialized.")
        self.log("Dev: { Quintero_Dev_Studio }")
        self.log("Waiting for user selection...")

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path = path
            display_text = path if len(path) < 35 else path[:10] + "..." + path[-20:]
            self.lbl_path.configure(text=display_text, text_color=COLOR_TEXT)
            self.btn_start.configure(state="normal", fg_color=COLOR_SUCCESS)
            self.set_status("Ready to start", COLOR_SUCCESS)

    def start_process(self):
        if not self.folder_path: return
        self.btn_start.configure(state="disabled", text="PROCESSING...")
        self.progressbar.set(0)
        self.set_status("Processing...", COLOR_ACCENT)
        threading.Thread(target=self.worker, daemon=True).start()

    def worker(self):
        folder = self.folder_path
        mode = self.radio_var.get()
        saved = 0
        time.sleep(0.5)
        # Dentro de tu app.py
        print(f"Ruta enviada al motor: {self.folder_path}") # <--- AÑADE ESTO
        count, size = find_and_remove_duplicates(self.folder_path)
        # (Lógica simplificada para el ejemplo)
        files = [os.path.join(r, f) for r, _, fs in os.walk(folder) for f in fs if f.lower().endswith(('.jpg','.jpeg','.png'))]
        if not files:
            self.log("No valid images found.")
            self.finish(0)
            return
        for i, f in enumerate(files):
            try:
                if mode in [1, 2]: strip_metadata(f)
                if mode in [1, 3]: saved += compress_image(f)
            except: pass
            self.progressbar.set((i + 1) / len(files))
        self.finish(saved)

    def finish(self, bytes_saved):
        self.log(f"Completed. Saved: {bytes_saved / 1048576:.2f} MB")
        self.set_status("Task Finished", COLOR_SUCCESS)
        self.btn_start.configure(state="normal", text="START PROCESS", fg_color=COLOR_SUCCESS)

if __name__ == "__main__":
    app = App()
    app.mainloop()