import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import platform
import ctypes
import os
import tkinter.filedialog as filedialog


class AntiVirusApp:
    def __init__(self, root):
        self.primary_color = "#e63946"
        # self.secondary_color = "#f1faee"
        self.dark_color = "#1e1e1e"
        self.secondary_dark_color = "#2e2e2e"
        # self.dark_color = "#1d3557"
        self.accent_color = "#a8dadc"
        self.sub_heading_color = "#cccccc"
        self.sub_sub_heading_color = "#888888"
        
        self.root = root
        self.root.title("SecureShield Antivirus")
        self.root.geometry("1000x700")
        self.root.configure(bg=self.dark_color)
        self.root.resizable(False, False)
        if platform.system() == "Windows":
            self.remove_maximize_button()
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, "assets", "icon.ico")
        
        try:
            icon_img = tk.PhotoImage(file=logo_path)
            self.root.iconphoto(False, icon_img)
        except Exception as e:
            print(f"Failed to set window icon: {e}")
        
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
        
        style.configure("Sidebar.TButton", background=self.dark_color, foreground="white", font=("Helvetica", 12), padding=(10, 10, 10, 6), anchor="center")
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
            script_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(script_dir, "assets", "logo.png")
            og_img = Image.open(logo_path)
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
            ("Quick Scan", self.show_quick_scan),
            ("Deep Scan", self),
            ("Schedule Scan", self),
            ("Quarantine", self),
            ("Settings", self)
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(sidebar, text=text, style="Sidebar.TButton", command=command)
            btn.pack(fill=tk.X, pady=5, padx=10)
            
        status_frame = tk.Frame(sidebar, bg=self.dark_color, height=100)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=15)
        
        protection_label = tk.Label(status_frame, text="Protection Status:", font=("Helvetica", 9), fg="white", bg=self.dark_color)
        protection_label.pack(anchor="w",padx=15)
        
        status_label = tk.Label(status_frame, text="ACTIVE", font=("Helvetica", 12, "bold"), fg="#4caf50", bg=self.dark_color)
        status_label.pack(anchor="w", padx=15)
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def create_status_card(self, parent, row, col, title, value, color):
        card = tk.Frame(parent, bg=self.secondary_dark_color, padx=15, pady=15, bd=0)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        title_label = tk.Label(card, text=title, font=("Helvetica", 12), fg=self.sub_heading_color, bg="#2e2e2e")
        title_label.pack(anchor="w")
        
        value_label = tk.Label(card, text=value, font=("Helvetica", 18, "bold"), fg=color, bg="#2e2e2e")
        value_label.pack(anchor="w", pady=(5, 0))
    
    def show_dashboard(self):
        self.clear_content()
        
        header = tk.Label(self.content_frame, text="System Security Dashboard", font=("Helvetica", 18, "bold"), fg="white", bg=self.dark_color)
        header.pack(anchor="w", pady=(0, 20), padx=10)
        
        cards_frame = tk.Frame(self.content_frame, bg=self.dark_color)
        cards_frame.pack(fill=tk.X, padx=10, pady=(0, 20))
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        
        self.create_status_card(cards_frame, 0, 0, "System Status", "Protected", "#4caf50")
        self.create_status_card(cards_frame, 0, 1, "Last Scan", "2 hours ago", self.accent_color)
        self.create_status_card(cards_frame, 1, 0, "Threats Detected", "0", self.primary_color)
        self.create_status_card(cards_frame, 1, 1, "Database", "Up to date", "#4caf50")
        
        activity_label = tk.Label(self.content_frame, text="Recent Activity", font=("Helvetica", 14, "bold"), fg="white", bg=self.dark_color)
        activity_label.pack(anchor="w", pady=(20, 10), padx=10)
        
        activity_frame = tk.Frame(self.content_frame, bg=self.dark_color, bd=0)
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 20))
        
        activities = [
            ("System scan completed", "No threats found", "10:30 AM"),
            ("Virus definitions updated", "Version 2.5.123", "09:15 AM"),
            ("Real-time protection", "Blocked suspicious URL", "Yesterday"),
        ]
        
        for i, (title, desc, time) in enumerate(activities):
            activity_item = tk.Frame(activity_frame, bg=self.secondary_dark_color, padx=10, pady=10)
            activity_item.pack(fill=tk.X, pady=(0, 1))
            
            title_label = tk.Label(activity_item, text=title, font=("Helvetica", 11, "bold"), fg="white", bg=self.secondary_dark_color, anchor="w")
            title_label.pack(anchor="w")
            
            desc_label = tk.Label(activity_item, text=desc, font=("Helvetica", 10), fg=self.sub_heading_color, bg=self.secondary_dark_color, anchor="w")
            desc_label.pack(anchor="w")
            
            time_label = tk.Label(activity_item, text=time, font=("Helvetica", 9), fg=self.sub_sub_heading_color, bg=self.secondary_dark_color, anchor="w")
            time_label.pack(anchor="w", pady=(5, 0))
    
    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_folder = folder_path
            self.folder_path_var.set(folder_path)
        else:
            self.selected_folder = None
            self.folder_path_var.set("No folder selected")
    
    def start_quick_scan(self):
        pass
    
    def cancel_scan(self):
        pass
    
    def show_quick_scan(self):
        self.clear_content()
        
        header = tk.Label(self.content_frame, text="Quick Scan", font=("Helvetica", 18, "bold"), fg="white", bg=self.dark_color)
        header.pack(anchor="w", pady=(0, 20), padx=10)
        
        description = tk.Label(self.content_frame, text="Scans the most vulnerable areas of your system for malware and security threats.", font=("Helvetica", 12), fg=self.sub_heading_color, bg=self.dark_color, wraplength=650, justify="left")
        description.pack(anchor="w", padx=10, pady=(0, 20))
        
        folder_frame = tk.Frame(self.content_frame, bg=self.dark_color)
        folder_frame.pack(fill=tk.X, pady=(0, 15))
        
        select_btn = ttk.Button(folder_frame, text="Select Folder to Scan", style="Red.TButton", command=self.select_folder)
        select_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.folder_path_var = tk.StringVar(value="No folder selected")
        folder_label = tk.Label(folder_frame, textvariable=self.folder_path_var, font=("Helvetica", 10), fg=self.sub_heading_color, bg=self.dark_color, anchor="w")
        folder_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        bottom_frame = tk.Frame(self.content_frame, bg=self.dark_color, pady=10)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        progress_frame = tk.Frame(bottom_frame, bg=self.dark_color)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=650, mode="determinate", style="Red.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        self.status_label = tk.Label(progress_frame, text="Ready to scan", font=("Helvetica", 10), fg=self.sub_heading_color, bg=self.dark_color)
        self.status_label.pack(anchor="w", pady=5)
        
        self.details_label = tk.Label(progress_frame, text="", font=("Helvetica", 9), fg=self.sub_sub_heading_color, bg=self.dark_color)
        self.details_label.pack(anchor="w")
        
        button_frame = tk.Frame(bottom_frame, bg=self.dark_color)
        button_frame.pack(fill=tk.X)
        
        self.scan_button = ttk.Button(button_frame, text="Start Quick Scan", style="Red.TButton", command=self.start_quick_scan)
        self.scan_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_button = ttk.Button(button_frame, text="Cancel", style="Red.TButton", state="disabled", command=self.cancel_scan)
        self.cancel_button.pack(side=tk.LEFT, padx=(0, 10))
  
        
if __name__ == "__main__":
    root = tk.Tk()
    app = AntiVirusApp(root)
    root.mainloop()