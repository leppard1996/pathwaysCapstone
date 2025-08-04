import tkinter as tk
from tkinter import ttk

class ThemeSelector:
    def __init__(self, parent_window, apply_theme_callback, theme_list=None, current_theme="superhero"):
        self.window = tk.Toplevel(parent_window)
        self.window.title("Choose Theme")
        self.window.geometry("300x400")
        self.window.resizable(False, False)
        self.apply_theme_callback = apply_theme_callback
        
        # Default theme list if none provided (backward compatibility)
        if theme_list is None:
            theme_list = [
                ("flatly", "Light Mode (flatly)"),
                ("superhero", "Dark Mode (superhero)")
            ]
        
        self.theme_list = theme_list
        self.theme_var = tk.StringVar(value=current_theme)

        self.create_widgets()
        
        # Center the window
        self.center_window()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.window, text="Select Theme", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=15)
        
        # Create scrollable frame for themes
        canvas = tk.Canvas(self.window, height=280)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        scrollbar.pack(side="right", fill="y", padx=(0, 20))
        
        # Add radio buttons for each theme
        for theme_key, display_name in self.theme_list:
            radio_frame = tk.Frame(scrollable_frame)
            radio_frame.pack(fill="x", pady=2)
            
            tk.Radiobutton(radio_frame, 
                          text=display_name, 
                          variable=self.theme_var,
                          value=theme_key, 
                          command=self.change_theme,
                          font=("Arial", 10),
                          anchor="w").pack(fill="x", padx=10)
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        
        # Buttons frame
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=15)
        
        # Apply button
        apply_btn = tk.Button(button_frame, text="Apply", 
                             command=self.apply_and_close,
                             font=("Arial", 10), width=10)
        apply_btn.pack(side="left", padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                              command=self.window.destroy,
                              font=("Arial", 10), width=10)
        cancel_btn.pack(side="left", padx=5)

    def center_window(self):
        """Center the window on the screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def change_theme(self):
        """Preview theme change (optional - you can remove this if you don't want live preview)"""
        theme = self.theme_var.get()
        self.apply_theme_callback(theme)

    def apply_and_close(self):
        """Apply selected theme and close window"""
        theme = self.theme_var.get()
        self.apply_theme_callback(theme)
        self.window.destroy()