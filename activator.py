# Windows Activator v1.0 - "OngbayActivate" (FINAL)
# Branding: Made By Ongbay
# Python 3.9+ required
# Run as Administrator
# Install: pip install customtkinter

import customtkinter as ctk
import subprocess
import threading
import os
import sys
from tkinter import messagebox

# --- Appearance ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# --- Activation Functions ---
def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def check_activation_status(log_callback):
    log_callback("[*] Checking Windows activation status...")
    # Run slmgr /xpr and let the Windows Script Host popup appear
    subprocess.Popen("slmgr /xpr", shell=True)
    return True, "✅ Check the popup window for activation status."

def activate_windows(version, log_callback):
    log_callback("[*] Starting Windows activation...")
    log_callback(f"[*] Version: {version}")
    
    # Edition to KMS client key mapping
    keys = {
        "Windows 10/11 Home": "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
        "Windows 10/11 Home N": "3KHY7-WNT83-DGQKR-F7HPR-844BM",
        "Windows 10/11 Home Single Language": "7HNRX-D7KGG-3C4B8-JG4XW-TDWQY",
        "Windows 10/11 Home Country Specific": "PVMJN-6DFY6-9CCP6-7BKTT-D3WVR",
        "Windows 10/11 Pro": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
        "Windows 10/11 Pro N": "MH37W-N47XK-V7XM9-C7227-GCQG9",
        "Windows 10/11 Pro Workstation": "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J",
        "Windows 10/11 Pro Workstation N": "9FNHH-K3HBT-3W4TD-6383H-6XYWF",
        "Windows 10/11 Education": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
        "Windows 10/11 Education N": "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ",
        "Windows 10/11 Enterprise": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
        "Windows 10/11 Enterprise N": "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4"
    }
    
    product_key = keys.get(version)
    if not product_key:
        log_callback("[!] Unknown Windows version.")
        return False
    
    # Run activation steps
    steps = [
        (f'slmgr /ipk {product_key}', "Installing product key..."),
        ('slmgr /skms kms8.msguides.com', "Setting KMS server..."),
        ('slmgr /ato', "Activating Windows...")
    ]
    
    for cmd, msg in steps:
        log_callback(f"[*] {msg}")
        output = run_cmd(cmd)
        log_callback(output)
        if "Error" in output or "0xC004" in output:
            log_callback(f"[!] Failed at step: {msg}")
            return False
    
    log_callback("[✓] Activation completed!")
    return True

# --- GUI ---
class ActivatorGUI:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Ongbay Windows Activator v1.0 - Made By Ongbay")
        self.window.geometry("750x650")
        self.window.resizable(False, False)
        
        self._build_ui()
        self._style_ui()
        
        # Check admin
        if not is_admin():
            messagebox.showwarning("Admin Required", "Please run as Administrator for full functionality.")
    
    def _build_ui(self):
        header = ctk.CTkLabel(
            self.window,
            text="⚡ ONGBAY WINDOWS ACTIVATOR ⚡",
            font=("Consolas", 24, "bold"),
            text_color="#00FFCC"
        )
        header.pack(pady=10)

        brand = ctk.CTkLabel(
            self.window,
            text="Made By Ongbay",
            font=("Consolas", 14),
            text_color="#FF6600"
        )
        brand.pack(pady=0)

        main = ctk.CTkFrame(self.window, fg_color="transparent")
        main.pack(pady=10, padx=20, fill="both", expand=True)

        # Windows Version Selection
        ctk.CTkLabel(main, text="Windows Version:", font=("Consolas", 14)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        versions = [
            "Windows 10/11 Home",
            "Windows 10/11 Home N",
            "Windows 10/11 Home Single Language",
            "Windows 10/11 Home Country Specific",
            "Windows 10/11 Pro",
            "Windows 10/11 Pro N",
            "Windows 10/11 Pro Workstation",
            "Windows 10/11 Pro Workstation N",
            "Windows 10/11 Education",
            "Windows 10/11 Education N",
            "Windows 10/11 Enterprise",
            "Windows 10/11 Enterprise N"
        ]
        
        self.version_combo = ctk.CTkComboBox(main, values=versions, width=320)
        self.version_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.version_combo.set("Windows 10/11 Pro")

        # Check Status Button
        self.check_btn = ctk.CTkButton(
            main,
            text="🔍 Check Activation Status",
            command=self.check_status,
            fg_color="#555555",
            hover_color="#777777",
            width=200
        )
        self.check_btn.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Status Display
        self.status_frame = ctk.CTkFrame(main, fg_color="#1A1A2E", corner_radius=8)
        self.status_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=5, sticky="ew")
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="📌 Click 'Check Activation Status' to check your Windows.",
            font=("Consolas", 13),
            text_color="#AAAAAA"
        )
        self.status_label.pack(pady=10, padx=10)

        # Activate Button
        self.activate_btn = ctk.CTkButton(
            main, 
            text="🔥 ACTIVATE WINDOWS", 
            command=self.start_activation,
            fg_color="#00AA66", 
            hover_color="#00CC88",
            width=250,
            height=40,
            font=("Consolas", 14)
        )
        self.activate_btn.grid(row=3, column=0, columnspan=2, pady=15)

        # Log area
        log_frame = ctk.CTkFrame(main)
        log_frame.grid(row=4, column=0, columnspan=2, pady=10, padx=5, sticky="nsew")
        main.grid_rowconfigure(4, weight=1)

        ctk.CTkLabel(log_frame, text="▶ Activation Log", font=("Consolas", 14, "bold"), text_color="#00FFCC").pack(anchor="w", pady=5)

        self.log_text = ctk.CTkTextbox(log_frame, font=("Consolas", 11), height=200)
        self.log_text.pack(fill="both", expand=True)

        # Info
        info_text = "⚠️ This tool uses KMS activation. Internet connection required.\n"
        info_text += "📌 Works on Windows 10 and Windows 11 (all editions)."
        ctk.CTkLabel(main, text=info_text, font=("Consolas", 11), text_color="#888888", justify="left").grid(row=5, column=0, columnspan=2, pady=10)

        # Footer
        footer = ctk.CTkLabel(self.window, text="Made By Ongbay", font=("Consolas", 10), text_color="#FF6600")
        footer.pack(side="bottom", pady=5)

    def _style_ui(self):
        self.window.configure(fg_color="#0A0A0A")

    def log(self, msg):
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")

    def check_status(self):
        self.check_btn.configure(state="disabled")
        self.log("[*] Checking activation status...")
        
        def check_thread():
            activated, msg = check_activation_status(self.log)
            self.window.after(0, lambda: self._check_done(activated, msg))
        
        threading.Thread(target=check_thread, daemon=True).start()

    def _check_done(self, activated, msg):
        self.check_btn.configure(state="normal")
        self.status_label.configure(text=msg)
        if activated:
            self.status_label.configure(text_color="#00FF66")
            self.activate_btn.configure(state="disabled", text="✅ Already Activated", fg_color="#555555")
        else:
            self.status_label.configure(text_color="#FF4444")
            self.activate_btn.configure(state="normal", text="🔥 ACTIVATE WINDOWS", fg_color="#00AA66")

    def start_activation(self):
        version = self.version_combo.get()
        self.activate_btn.configure(state="disabled")
        self.status_label.configure(text="⏳ Activating...", text_color="#FFCC00")
        self.log("[*] Starting activation process...")
        
        def activation_thread():
            success = activate_windows(version, self.log)
            self.window.after(0, lambda: self._activation_done(success))
        
        threading.Thread(target=activation_thread, daemon=True).start()

    def _activation_done(self, success):
        self.activate_btn.configure(state="normal")
        if success:
            self.status_label.configure(text="✅ Windows activated successfully!", text_color="#00FFCC")
            self.activate_btn.configure(text="✅ Activated", fg_color="#555555")
        else:
            self.status_label.configure(text="❌ Activation failed. Check log.", text_color="#FF4444")
            self.activate_btn.configure(text="🔥 RETRY", fg_color="#CC3333")

# --- Main ---
if __name__ == "__main__":
    app = ActivatorGUI()
    app.window.mainloop()