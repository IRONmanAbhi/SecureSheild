import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, filedialog, messagebox
import platform
import ctypes
import os
import threading
import random
import time
from engine import Engine

class AntiVirusApp:
    def __init__(self, root):
        # Initialize colors
        self.primary_color = "#e63946"
        self.dark_color = "#1e1e1e"
        self.secondary_dark_color = "#2e2e2e"
        self.ternary_dark_color = "#3e3e3e"
        self.accent_color = "#a8dadc"
        self.heading_color = "#ffffff"
        self.sub_heading_color = "#cccccc"
        self.sub_sub_heading_color = "#888888"
        
        # Initialize the antivirus engine
        self.scanner = Engine("malware_hashes.txt")
        
        # Initialize the main window
        self.root = root
        self.root.title("SecureShield Antivirus")
        self.root.geometry("1000x700")
        self.root.configure(bg=self.dark_color)
        self.root.resizable(False, False)
        if platform.system() == "Windows":
            self.remove_maximize_button()
        
        # Set window icon
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, "assets", "icon.ico")
        
        try:
            icon_img = tk.PhotoImage(file=logo_path)
            self.root.iconphoto(False, icon_img)
        except Exception as e:
            print(f"Failed to set window icon: {e}")
        
        self.create_styles()
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg=self.dark_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_sidebar()
        
        # Create content frame
        self.content_frame = tk.Frame(self.main_frame, bg=self.dark_color)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.show_dashboard()
        
        # Initialize variables
        self.start_with_windows = True
        self.show_notifications = True
        self.send_anonymous_stats = False
        self.check_updates = True
        
        self.real_time_protection = True
        self.suspicious_websites_protection = True
        
        self.scan_system_files = False
        
        self.check_updates_daily = True
        self.download_updates_automatically = True
        
        self.scan_running = False
        self.progress_value = 0
        self.scan_thread = None
        
    def remove_maximize_button(self):
        # Remove maximize button and prevent resizing on Windows
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
        # Create custom styles for the application
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Red.Horizontal.TProgressbar", troughcolor=self.dark_color, background=self.primary_color, bordercolor=self.primary_color, lightcolor=self.primary_color, darkcolor=self.primary_color)
        
        style.configure("TButton", background=self.primary_color, foreground=self.heading_color, font=("Helvetica", 10, "bold"), borderwidth=0)
        style.map("TButton", background=[("active", "#c1121f"), ("pressed", "#780000")], foreground=[("active", self.heading_color), ("pressed", self.heading_color)])
        
        style.configure("Red.TButton", background=self.primary_color, foreground=self.heading_color, font=("Helvetica", 12, "bold"), padding=10)
        style.map("Red.TButton", background=[("active", "#c1121f"), ("pressed", "#780000")], foreground=[("active", self.heading_color), ("pressed", self.heading_color)])
        
        style.configure("Sidebar.TButton", background=self.dark_color, foreground=self.heading_color, font=("Helvetica", 12), padding=(10, 10, 10, 6), anchor="center")
        style.map("Sidebar.TButton", background=[("active", self.secondary_dark_color), ("pressed", self.ternary_dark_color)], foreground=[("active", self.primary_color), ("pressed", self.primary_color)])
        
        style.configure("TNotebook", background=self.dark_color, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.secondary_dark_color, foreground="white", lightcolor=self.dark_color, borderwidth=0, padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#1f1f1f")], foreground=[("selected", "white")])
        
        style.configure("Switch.TCheckbutton", background=self.dark_color, foreground="white", font=("Helvetica", 10), focuscolor=self.dark_color)
        style.map("Switch.TCheckbutton", background=[("active", self.dark_color)], foreground=[("active", "white")])
    
    def create_sidebar(self):
        # Create sidebar with navigation buttons
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
            
            subtitle = tk.Label(logo_frame, text="Antivirus", font=("Helvetica", 14), fg=self.heading_color, bg=self.dark_color)
            subtitle.pack(pady=(0, 10))
        except Exception as e:
            logo_label = tk.Label(logo_frame, bg=self.dark_color, text="SecureShield", font=("Helvatica", 16, "bold"), fg=self.primary_color)
            logo_label.pack(pady=(20, 5))
            
            subtitle = tk.Label(logo_frame, text="Antivirus", font=("Helvetica", 14), fg=self.heading_color, bg=self.dark_color)
            subtitle.pack(pady=(0, 20))
            
            print(f"Error loading logo image: {e}")
        
        separator = ttk.Separator(sidebar, orient="horizontal")
        separator.pack(fill=tk.X, padx=20, pady=10)
        
        nav_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Quick Scan", self.show_quick_scan),
            ("Deep Scan", self.show_deep_scan),
            ("Schedule Scan", self.show_scheduled),
            ("Quarantine", self.show_quarantine),
            ("Settings", self.show_settings)
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(sidebar, text=text, style="Sidebar.TButton", command=command)
            btn.pack(fill=tk.X, pady=5, padx=10)
            
        status_frame = tk.Frame(sidebar, bg=self.dark_color, height=100)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=15)
        
        protection_label = tk.Label(status_frame, text="Protection Status:", font=("Helvetica", 9), fg=self.heading_color, bg=self.dark_color)
        protection_label.pack(anchor="w",padx=15)
        
        status_label = tk.Label(status_frame, text="ACTIVE", font=("Helvetica", 12, "bold"), fg="#4caf50", bg=self.dark_color)
        status_label.pack(anchor="w", padx=15)
    
    def clear_content(self):
        # Clear the content frame before loading new content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def create_status_card(self, parent, row, col, title, value, color):
        # Create a status card with title and value
        card = tk.Frame(parent, bg=self.secondary_dark_color, padx=15, pady=15, bd=0)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        title_label = tk.Label(card, text=title, font=("Helvetica", 12), fg=self.sub_heading_color, bg=self.secondary_dark_color)
        title_label.pack(anchor="w")
        
        value_label = tk.Label(card, text=value, font=("Helvetica", 18, "bold"), fg=color, bg=self.secondary_dark_color)
        value_label.pack(anchor="w", pady=(5, 0))
    
    def show_dashboard(self):
        # Show the dashboard content
        self.clear_content()
        
        header = tk.Label(self.content_frame, text="System Security Dashboard", font=("Helvetica", 18, "bold"), fg=self.heading_color, bg=self.dark_color)
        header.pack(anchor="w", pady=(0, 20), padx=10)
        
        cards_frame = tk.Frame(self.content_frame, bg=self.dark_color)
        cards_frame.pack(fill=tk.X, padx=10, pady=(0, 20))
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        
        self.create_status_card(cards_frame, 0, 0, "System Status", "Protected", "#4caf50")
        self.create_status_card(cards_frame, 0, 1, "Last Scan", "2 hours ago", self.accent_color)
        self.create_status_card(cards_frame, 1, 0, "Threats Detected", "0", self.primary_color)
        self.create_status_card(cards_frame, 1, 1, "Database", "Up to date", "#4caf50")
        
        activity_label = tk.Label(self.content_frame, text="Recent Activity", font=("Helvetica", 14, "bold"), fg=self.heading_color, bg=self.dark_color)
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
            
            title_label = tk.Label(activity_item, text=title, font=("Helvetica", 11, "bold"), fg=self.heading_color, bg=self.secondary_dark_color, anchor="w")
            title_label.pack(anchor="w")
            
            desc_label = tk.Label(activity_item, text=desc, font=("Helvetica", 10), fg=self.sub_heading_color, bg=self.secondary_dark_color, anchor="w")
            desc_label.pack(anchor="w")
            
            time_label = tk.Label(activity_item, text=time, font=("Helvetica", 9), fg=self.sub_sub_heading_color, bg=self.secondary_dark_color, anchor="w")
            time_label.pack(anchor="w", pady=(5, 0))
    
    def select_folder(self):
        # Open a dialog to select a folder for scanning
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_folder = folder_path
            self.folder_path_var.set(folder_path)
            self.scanner.folder_scan(folder_path)
        else:
            self.selected_folder = None
            self.folder_path_var.set("No folder selected")
    
    def start_quick_scan(self):
        # Start the quick scan process
        if self.scan_running:
            return
        
        self.scan_running = True
        self.progress_value = 0
        self.progress_bar["value"] = 0
        self.scan_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.status_label.config(text="Scanning...")
        
        self.scan_thread = threading.Thread(target=self.run_scan_simulation)
        self.scan_thread.daemon = True
        self.scan_thread.start()
        
    def run_scan_simulation(self):
        # Simulate a scan process with a progress bar
        total_files = 100
        scanned_files = 0
        self.progress_value = 0
        self.update_scan_progress("", scanned_files, total_files)
        while self.scan_running and scanned_files < total_files:
            time.sleep(random.uniform(0.05, 0.2))
            scanned_files += 1
            self.progress_value = int((scanned_files / total_files) * 100)
            self.update_scan_progress("", scanned_files, total_files)
            if scanned_files == total_files:
                self.complete_scan()
                return
            
    def update_scan_progress(self, current_location, scanned_files, total_files):
        # Update the scan progress bar and status labels
        self.details_label.config(text=f"Scanning {current_location} ({scanned_files}/{total_files})")
        self.progress_bar["value"] = self.progress_value
        self.status_label.config(text=f"Scanning... {self.progress_value}%")
        
    def complete_scan(self):
        # Complete the scan and update the UI
        self.scan_running = False
        self.status_label.config(text="Scan completed successfully")
        self.details_label.config(text="No threats detected")
        self.scan_button.config(state="normal")
        self.cancel_button.config(state="disabled")
        messagebox.showinfo("Scan Complete", "Quick scan completed successfully. No threats were detected.")
    
    def cancel_scan(self):
        # Cancel the ongoing scan
        if self.scan_running:
            self.scan_running = False
            self.status_label.config(text="Scan cancelled")
            self.scan_button.config(state="normal")
            self.cancel_button.config(state="disabled")
    
    def show_quick_scan(self):
        # Show the quick scan interface
        self.clear_content()
        
        header = tk.Label(self.content_frame, text="Quick Scan", font=("Helvetica", 18, "bold"), fg=self.heading_color, bg=self.dark_color)
        header.pack(anchor="w", pady=(0, 20), padx=10)
        
        description = tk.Label(self.content_frame, text="Scans the most vulnerable areas of your system for malware and security threats.", font=("Helvetica", 12), fg=self.sub_heading_color, bg=self.dark_color, wraplength=650, justify="left")
        description.pack(anchor="w", padx=10, pady=(0, 20))
        
        folder_frame = tk.Frame(self.content_frame, bg=self.dark_color)
        folder_frame.pack(fill=tk.X, pady=(0, 15))
        
        select_btn = ttk.Button(folder_frame, text="Select Folder to Scan", style="Red.TButton", command=self.select_folder)
        select_btn.pack(side=tk.LEFT, padx=(10, 10))
        
        self.folder_path_var = tk.StringVar(value="No folder selected")
        folder_label = tk.Label(folder_frame, textvariable=self.folder_path_var, font=("Helvetica", 10), fg=self.sub_heading_color, bg=self.dark_color, anchor="w")
        folder_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        bottom_frame = tk.Frame(self.content_frame, bg=self.dark_color, pady=10)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        progress_frame = tk.Frame(bottom_frame, bg=self.dark_color)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=650, mode="determinate", style="Red.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, pady=10, padx=(0, 10))
        
        self.status_label = tk.Label(progress_frame, text="Ready to scan", font=("Helvetica", 10), fg=self.sub_heading_color, bg=self.dark_color)
        self.status_label.pack(anchor="w", pady=5)
        
        self.details_label = tk.Label(progress_frame, text="", font=("Helvetica", 9), fg=self.sub_sub_heading_color, bg=self.dark_color)
        self.details_label.pack(anchor="w")
        
        button_frame = tk.Frame(bottom_frame, bg=self.dark_color)
        button_frame.pack(fill=tk.X)
        
        self.scan_button = ttk.Button(button_frame, text="Start Quick Scan", style="Red.TButton", command=self.start_quick_scan, padding=(10, 12, 10, 10))
        self.scan_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_button = ttk.Button(button_frame, text="Cancel", style="Red.TButton", state="disabled", command=self.cancel_scan, padding=(10, 13, 10, 9))
        self.cancel_button.pack(side=tk.LEFT, padx=(0, 10))
  
    def show_deep_scan(self):
        # Show the deep scan interface
        self.clear_content()
        
        header = tk.Label(self.content_frame, text="Deep Scan", font=("Helvetica", 18, "bold"), fg=self.heading_color, bg=self.dark_color)
        header.pack(anchor="w", pady=(0, 20), padx=10)
        
        description = tk.Label(self.content_frame, text="Performs a comprehensive scan of your entire system to detect and remove all types of malware.", font=("Helvetica", 12), fg=self.sub_heading_color, bg=self.dark_color, wraplength=650, justify="left")
        description.pack(anchor="w", padx=10, pady=(0, 20))
        
        placeholder_label = tk.Label(self.content_frame, text="Deep Scan feature is under development.", font=("Helvetica", 20), fg=self.sub_heading_color, bg=self.dark_color)
        placeholder_label.pack(anchor="w", padx=10)
    
    def save_scan_frequency(self):
        # Save the selected scan frequency
        selected_freq = self.scan_frequency.get()
        messagebox.showinfo("Scan Frequency", f"Scan frequency set to: {selected_freq}")
    
    def show_scheduled(self):
        # Show the scheduled scans interface
        self.clear_content()
        
        header = tk.Label(self.content_frame, text="Scheduled Scans", font=("Helvetica", 18, "bold"), fg=self.heading_color, bg=self.dark_color)
        header.pack(anchor="w", pady=(0, 20), padx=10)
        
        description = tk.Label(self.content_frame, text="Manage your scheduled scans to ensure regular system checks.", font=("Helvetica", 12), fg=self.sub_heading_color, bg=self.dark_color, wraplength=650, justify="left")
        description.pack(anchor="w", padx=10, pady=(0, 20))
        
        scan_option_frame = tk.Frame(self.content_frame, bg=self.dark_color)
        scan_option_frame.pack(anchor="w", padx=10, pady=(0, 20))

        scan_option_label = tk.Label(scan_option_frame, text="Scan Frequency:", font=("Helvetica", 18, "bold"), fg=self.heading_color, bg=self.dark_color)
        scan_option_label.pack(anchor="w", pady=(0, 5))

        self.scan_frequency = tk.StringVar(value="Monthly")

        frequencies = ["Daily", "Monthly", "Yearly"]
        for freq in frequencies:
            rb = tk.Radiobutton(scan_option_frame, text=freq, variable=self.scan_frequency, value=freq, font=("Helvetica", 13), fg=self.heading_color, bg=self.dark_color, selectcolor="#444444", activebackground=self.dark_color, activeforeground=self.heading_color, borderwidth=0, highlightthickness=0, relief="flat")
            rb.pack(anchor="w", pady=(5, 10))
            
        self.scan_button = ttk.Button(self.content_frame, text="Save Schedule", style="Red.TButton", command=self.save_scan_frequency, padding=(10, 12, 10, 10))
        self.scan_button.pack(side=tk.LEFT, padx=(10, 10))
        
    def show_empty_quarantine(self):
        empty_frame = tk.Frame(self.content_frame, bg=self.secondary_dark_color, padx=20, pady=30)
        empty_frame.pack(fill=tk.BOTH, expand=True)
        
        empty_frame.pack_propagate(False)
        center_frame = tk.Frame(empty_frame, bg=self.secondary_dark_color)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        shield_label = tk.Label(center_frame, text="🛡️", font=("Helvetica", 48), fg=self.primary_color, bg=self.secondary_dark_color)
        shield_label.pack()
        
        empty_label = tk.Label(center_frame, text="No Items in Quarantine", font=("Helvetica", 16, "bold"), fg=self.heading_color, bg=self.secondary_dark_color)
        empty_label.pack(pady=(10, 5))
        
        info_label = tk.Label(center_frame, text="Your system is clean! No malicious files have been detected.", font=("Helvetica", 10), fg=self.sub_heading_color, bg=self.secondary_dark_color)
        info_label.pack()
    
    def show_quarantine(self):
        # Show the quarantine management interface
        self.clear_content()
        
        header = tk.Label(self.content_frame, text="Quarantine", font=("Helvetica", 18, "bold"), fg=self.heading_color, bg=self.dark_color)
        header.pack(anchor="w", pady=(0, 20), padx=10)
        
        description = tk.Label(self.content_frame, text="Manage quarantined files that have been detected as threats.", font=("Helvetica", 12), fg=self.sub_heading_color, bg=self.dark_color, wraplength=650, justify="left")
        description.pack(anchor="w", padx=10, pady=(0, 20))
        
        self.show_empty_quarantine()
        
    def create_settings_section(self, parent, title, options, pady=(0, 0)):
        # Create a settings section with a title and options
        section = tk.Frame(parent, bg=self.dark_color, pady=10)
        section.pack(fill=tk.X, pady=pady)
        
        title_label = tk.Label(section, text=title, font=("Helvetica", 12, "bold"), fg=self.heading_color, bg=self.dark_color)
        title_label.pack(anchor="w", pady=(0, 10), padx=(10, 0))
        
        # Store references to BooleanVars
        if not hasattr(self, 'settings_vars'):
            self.settings_vars = {}
        
        for text, default in options:
            option_frame = tk.Frame(section, bg=self.dark_color, pady=3)
            option_frame.pack(fill=tk.X, padx=(10, 0))
            
            var = tk.BooleanVar(value=default)
            self.settings_vars[text] = var
            switch = ttk.Checkbutton(option_frame, text=text, variable=var, style="Switch.TCheckbutton")
            switch.pack(anchor="w", padx=(10, 0))
    
    def check_for_updates(self):
        # Simulate checking for updates
        messagebox.showinfo("Updates", "Checking for updates... Your antivirus is up to date!")
        
    def save_settings(self):
        # Save the settings and show a confirmation message
        label_to_var = {
            "Start with Windows": "start_with_windows",
            "Show notifications": "show_notifications",
            "Send anonymous usage statistics": "send_anonymous_stats",
            "Check for updates automatically": "check_updates",
            "Enable real-time file protection": "real_time_protection",
            "Block suspicious websites": "suspicious_websites_protection",
            "Scan system files": "scan_system_files",
            "Check for updates daily": "check_updates_daily",
            "Download updates automatically": "download_updates_automatically"
        }
    
        for label, var_name in label_to_var.items():
            if label in self.settings_vars:
                setattr(self, var_name, self.settings_vars[label].get())
        messagebox.showinfo("Settings", "Settings saved successfully.")
    
    def show_settings(self):
        # Show the settings interface
        self.clear_content()
        
        header = tk.Label(self.content_frame, text="Settings", font=("Helvetica", 18, "bold"), fg=self.heading_color, bg=self.dark_color)
        header.pack(anchor="w", pady=(0, 20), padx=10)
        
        description = tk.Label(self.content_frame, text="Configure your antivirus settings to customize protection.", font=("Helvetica", 12), fg=self.sub_heading_color, bg=self.dark_color, wraplength=650, justify="left")
        description.pack(anchor="w", padx=10, pady=(0, 20))
        
        notebook = ttk.Notebook(self.content_frame, style="TNotebook")
        notebook.pack(fill=tk.BOTH, expand=True)
        
        general_tab = tk.Frame(notebook, bg=self.dark_color)
        protection_tab = tk.Frame(notebook, bg=self.dark_color)
        update_tab = tk.Frame(notebook, bg=self.dark_color)
        advanced_tab = tk.Frame(notebook, bg=self.dark_color)
        
        notebook.add(general_tab, text="General")
        notebook.add(protection_tab, text="Protection")
        notebook.add(update_tab, text="Updates")
        
        self.create_settings_section(general_tab, "Application Settings", [
            ("Start with Windows", self.start_with_windows),
            ("Show notifications", self.show_notifications),
            ("Send anonymous usage statistics", self.send_anonymous_stats),
            ("Check for updates automatically", self.check_updates)
        ])
        
        self.create_settings_section(protection_tab, "Real-time Protection", [
            ("Enable real-time file protection", self.real_time_protection),
            ("Block suspicious websites", self.suspicious_websites_protection)
        ])
        
        self.create_settings_section(protection_tab, "Scan Settings", [
            ("Scan system files", self.scan_system_files)
        ], pady=(20, 0))
        
        self.create_settings_section(update_tab, "Update Settings", [
            ("Check for updates daily", self.check_updates_daily),
            ("Download updates automatically", self.download_updates_automatically)
        ])
        
        update_frame = tk.Frame(update_tab, bg=self.dark_color, pady=20)
        update_frame.pack(fill=tk.X)
        
        last_update_label = tk.Label(update_frame, text="Last update: Today at 08:24 AM", font=("Helvetica", 10), fg=self.sub_heading_color, bg=self.dark_color)
        last_update_label.pack(side=tk.LEFT)
        
        update_button = ttk.Button(update_frame, text="Check for Updates", command=self.check_for_updates)
        update_button.pack(side=tk.RIGHT)
        
        
        save_frame = tk.Frame(self.content_frame, bg=self.dark_color, pady=15)
        save_frame.pack(fill=tk.X)
        
        save_button = ttk.Button(save_frame, text="Save Settings", style="Red.TButton", command=self.save_settings)
        save_button.pack(side=tk.RIGHT)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = AntiVirusApp(root)
    root.mainloop()