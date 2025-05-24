import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import platform
import ctypes


class AntiVirusApp:
    def __init__(self, root):
        self.primary_color = "#e63946"
        # self.secondary_color = "#f1faee"
        self.dark_color = "#1e1e1e"
        # self.dark_color = "#1d3557"
        # self.accent_color = "#a8dadc"
        
        self.root = root
        self.root.title("SecureShield Antivirus")
        self.root.geometry("1000x700")
        self.root.configure(bg=self.dark_color)
        self.root.resizable(False, False)
        if platform.system() == "Windows":
            self.remove_maximize_button()
        
        self.create_styles()
        
        self.main_frame = tk.Frame(self.root, bg=self.dark_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_sidebar()
        
        self.content_frame = tk.Frame(self.main_frame, bg=self.dark_color)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.show_dashboard()
        
        self.scan_running = False
        self.progress_value = 0
        self.scan_thread = None
        
    def remove_maximize_button(self):
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())

        GWL_STYLE = -16
        WS_MAXIMIZEBOX = 0x00010000
        WS_THICKFRAME = 0x00040000

        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
        style &= ~WS_MAXIMIZEBOX  # Remove maximize button
        style &= ~WS_THICKFRAME   # Prevent resizing

        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
        ctypes.windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0020)  # SWP_NOSIZE | SWP_NOMOVE | SWP_FRAMECHANGED

        
    def create_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Red.Horizontal.TProgressbar", 
                        troughcolor="#1e1e1e", 
                        background=self.primary_color,
                        bordercolor=self.primary_color,
                        lightcolor=self.primary_color,
                        darkcolor=self.primary_color)
        
        style.configure("TButton", 
                        background=self.primary_color, 
                        foreground="white", 
                        font=("Helvetica", 10, "bold"),
                        borderwidth=0)
        style.map("TButton",
                 background=[("active", "#c1121f"), ("pressed", "#780000")],
                 foreground=[("active", "white"), ("pressed", "white")])
        
        style.configure("Red.TButton", 
                        background=self.primary_color, 
                        foreground="white", 
                        font=("Helvetica", 12, "bold"),
                        padding=10)
        style.map("Red.TButton",
                 background=[("active", "#c1121f"), ("pressed", "#780000")],
                 foreground=[("active", "white"), ("pressed", "white")])
        
        style.configure("Sidebar.TButton", bacground=self.dark_color, foreground="white", font=("Helvetica", 12), padding=10, anchor="center")
        style.map("Sidebar.TButton",
                 background=[("active", "#2e2e2e"), ("pressed", "#3e3e3e")],
                 foreground=[("active", self.primary_color), ("pressed", self.primary_color)])
    
    def create_sidebar(self):
        sidebar = tk.Frame(self.main_frame, width=200, bg=self.dark_color, bd=0, relief=tk.SOLID)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        logo_frame = tk.Frame(sidebar, bg=self.dark_color, height=150)
        logo_frame.pack(fill=tk.X)
        
        try:
            og_img = Image.open("./assets/logo.png")
            rs_img = og_img.resize((80, 80), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(rs_img)
            
            logo_img_label = tk.Label(logo_frame, image=self.logo_img, bg=self.dark_color)
            logo_img_label.pack(pady=(20, 5))
            
            logo_label = tk.Label(logo_frame, bg=self.dark_color, text="SecureShield", font=("Helvatica", 16, "bold"), fg=self.primary_color)
            logo_label.pack(pady=(5, 0))
            
            subtitle = tk.Label(logo_frame, text="Antivirus", font=("Helvetica", 14), fg="white", bg=self.dark_color)
            subtitle.pack(pady=(0, 10))
        except Exception as e:
            logo_label = tk.Label(logo_frame, bg=self.dark_color, text="SecureShield", font=("Helvatica", 16, "bold"), fg=self.primary_color)
            logo_label.pack(pady=(20, 5))
            
            subtitle = tk.Label(logo_frame, text="Antivirus", font=("Helvetica", 14), fg="white", bg=self.dark_color)
            subtitle.pack(pady=(0, 20))
            
            print(f"Error loading logo image: {e}")
        
        separator = ttk.Separator(sidebar, orient="horizontal")
        separator.pack(fill=tk.X, padx=20, pady=10)
        
        nav_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Quick Scan", self),
            ("Deep Scan", self),
            ("Schedule Scan", self),
            ("Quarantine", self),
            ("Settings", self)
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(sidebar, text=text, style="Sidebar.TButton", command=command)
            btn.pack(fill=tk.X, pady=2)
            
        status_frame = tk.Frame(sidebar, bg=self.dark_color, height=100)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=15)
        
        protection_label = tk.Label(status_frame, text="Protection Status:", font=("Helvetica", 9), fg="white", bg=self.dark_color)
        protection_label.pack(anchor="w",padx=15)
        
        status_label = tk.Label(status_frame, text="ACTIVE", font=("Helvetica", 12, "bold"), fg="#4caf50", bg=self.dark_color)
        status_label.pack(anchor="w", padx=15)
    
    def show_dashboard(self):
        pass
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = AntiVirusApp(root)
    root.mainloop()