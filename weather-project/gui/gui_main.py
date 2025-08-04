import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import json
import os
from data.data import fetch_current_weather
from features.theme import ThemeSelector
from features.forecast import get_forecast, get_local_weather_emoji

# Optional imports for image handling
try:
    from PIL import Image, ImageTk
    import requests
    from io import BytesIO
    IMAGES_AVAILABLE = True
except ImportError:
    IMAGES_AVAILABLE = False
    print("Pillow not installed. Using emoji fallbacks for weather icons.")

class WeatherDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("600x700")

        self.latest_weather_data = None
        self.current_temp_f = None

        # Expanded theme configuration with more options
        self.themes = {
            "flatly": {  # Sky Blue theme - Much more blue like the sky
                "bg_color": "#87ceeb",  # Sky blue background
                "fg_color": "#1e90ff", # Dodger blue accents
                "text_color": "#000080",  # Navy blue text
                "display_name": "Sky Blue"
            },
            "superhero": {  # Dark theme
                "bg_color": "#2c3e50",
                "fg_color": "#4e73df",
                "text_color": "#FFFFFF",
                "display_name": "Dark Blue"
            },
            "forest": {  # Green nature theme
                "bg_color": "#2d5016",
                "fg_color": "#4caf50",
                "text_color": "#e8f5e8",
                "display_name": "Forest Green"
            },
            "sunset": {  # Orange/red theme
                "bg_color": "#3e2723",
                "fg_color": "#ff6f00",
                "text_color": "#fff3e0",
                "display_name": "Sunset Orange"
            },
            "ocean": {  # Blue ocean theme
                "bg_color": "#0d47a1",
                "fg_color": "#29b6f6",
                "text_color": "#e3f2fd",
                "display_name": "Ocean Blue"
            },
            "lavender": {  # Purple theme - Much more purple
                "bg_color": "#663399",  # Rich purple background
                "fg_color": "#da70d6",  # Orchid purple accents
                "text_color": "#f8f0ff",  # Very light purple-white text
                "display_name": "Royal Purple"
            },
            "arctic": {  # Light blue/white theme
                "bg_color": "#f8f9fa",
                "fg_color": "#17a2b8",
                "text_color": "#212529",
                "display_name": "Arctic White"
            },
            "midnight": {  # Very dark theme
                "bg_color": "#121212",
                "fg_color": "#bb86fc",
                "text_color": "#ffffff",
                "display_name": "Midnight Black"
            },
            "autumn": {  # Brown/orange theme
                "bg_color": "#5d4037",
                "fg_color": "#ff8a65",
                "text_color": "#efebe9",
                "display_name": "Autumn Brown"
            },
            "mint": {  # Mint green theme
                "bg_color": "#e8f5e8",
                "fg_color": "#00695c",
                "text_color": "#2e2e2e",
                "display_name": "Mint Fresh"
            }
        }
        
        # Load saved theme preference or default to superhero
        self.settings_file = "weather_settings.json"
        self.current_theme = self.load_theme_preference()
        
        # Initialize theme colors first
        theme_config = self.themes.get(self.current_theme)
        self.bg_color = theme_config["bg_color"]
        self.fg_color = theme_config["fg_color"]
        self.text_color = theme_config["text_color"]
        
        # Create scrollable main frame
        self.create_scrollable_frame()
        self.create_widgets()
        
        # Apply theme after widgets are created
        self.apply_theme(self.current_theme)
        
        self.compare_button = None
        self.compare_frame = None
        self.forecast_frame = None

        # Initialize theme selector window reference to None
        self.theme_selector_window = None

    def load_theme_preference(self):
        """Load saved theme preference from JSON file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    saved_theme = settings.get('theme', 'superhero')
                    # Validate that the saved theme exists
                    if saved_theme in self.themes:
                        return saved_theme
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            pass
        
        # Default to superhero if no valid saved theme
        return 'superhero'

    def save_theme_preference(self, theme):
        """Save theme preference to JSON file"""
        try:
            settings = {}
            # Load existing settings if file exists
            if os.path.exists(self.settings_file):
                try:
                    with open(self.settings_file, 'r') as f:
                        settings = json.load(f)
                except (json.JSONDecodeError, KeyError):
                    settings = {}
            
            # Update theme setting
            settings['theme'] = theme
            
            # Save to file
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
                
        except Exception as e:
            print(f"Error saving theme preference: {e}")

    def get_theme_list(self):
        """Get list of available themes with display names"""
        return [(key, value["display_name"]) for key, value in self.themes.items()]

    def create_scrollable_frame(self):
        # Create canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(self.root, bg=self.bg_color)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_color)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.root.bind("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_widgets(self):
        # Use scrollable_frame instead of self.root for all widgets
        parent = self.scrollable_frame
        parent.configure(bg=self.bg_color)

        title_label = tk.Label(parent, text="Weather Dashboard",
                               font=('Arial', 18, 'bold'),
                               bg=self.fg_color, fg="white", pady=10)
        title_label.pack(fill=tk.X)

        input_frame = tk.Frame(parent, bg=self.bg_color)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="City:", bg=self.bg_color, fg=self.text_color).grid(row=0, column=0, padx=5, sticky=tk.W)
        self.city_entry = ttk.Entry(input_frame, width=20)
        self.city_entry.grid(row=0, column=1, padx=5)
        self.city_entry.insert(0, "New York")

        tk.Label(input_frame, text="Unit:", bg=self.bg_color, fg=self.text_color).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.temp_unit = tk.StringVar(value="F")
        unit_frame = tk.Frame(input_frame, bg=self.bg_color)
        unit_frame.grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(unit_frame, text="F", command=self.temp_unit_update, variable=self.temp_unit, value="F").pack(side=tk.LEFT)
        ttk.Radiobutton(unit_frame, text="C", command=self.temp_unit_update, variable=self.temp_unit, value="C").pack(side=tk.LEFT)

        button_frame = tk.Frame(parent, bg=self.bg_color)
        button_frame.pack(pady=5)

        update_btn = tk.Button(button_frame, text="Update", command=self.update_display,
                               bg=self.fg_color, fg="white", activebackground=self.fg_color)
        update_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = tk.Button(button_frame, text="Clear", command=self.clear_inputs,
                              bg=self.fg_color, fg="white", activebackground=self.fg_color)
        clear_btn.pack(side=tk.LEFT, padx=5)

        forecast_btn = tk.Button(button_frame, text="5-Day Forecast", command=self.show_forecast,
                                bg=self.fg_color, fg="white", activebackground=self.fg_color)
        forecast_btn.pack(side=tk.LEFT, padx=5)

        theme_btn = tk.Button(button_frame, text="Change Theme",
                      command=self.open_theme_selector,
                      bg=self.fg_color, fg="white", activebackground=self.fg_color)
        theme_btn.pack(side=tk.LEFT, padx=5)

        # Current weather display
        result_frame = tk.Frame(parent, bg=self.bg_color)
        result_frame.pack(pady=15, fill=tk.X)

        # Weather icon and main info frame
        weather_main_frame = tk.Frame(result_frame, bg=self.bg_color)
        weather_main_frame.pack(fill=tk.X, padx=10)

        # Left side for weather icon
        self.icon_frame = tk.Frame(weather_main_frame, bg=self.bg_color)
        self.icon_frame.pack(side=tk.LEFT, padx=(0, 15))

        # Right side for weather info
        info_frame = tk.Frame(weather_main_frame, bg=self.bg_color)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.loc_label = tk.Label(info_frame, text="Location: --", 
                                  bg=self.bg_color, fg=self.text_color, font=('Arial', 12))
        self.loc_label.pack(anchor="w", pady=2)

        self.temp_label = tk.Label(info_frame, text="Temperature: --", 
                                   bg=self.bg_color, fg=self.text_color, font=('Arial', 12))
        self.temp_label.pack(anchor="w", pady=2)

        self.humidity_label = tk.Label(info_frame, text="Humidity: --", 
                                       bg=self.bg_color, fg=self.text_color, font=('Arial', 12))
        self.humidity_label.pack(anchor="w", pady=2)

        self.precip_label = tk.Label(info_frame, text="Precipitation: --", 
                                     bg=self.bg_color, fg=self.text_color, font=('Arial', 12))
        self.precip_label.pack(anchor="w", pady=2)

        self.condition_label = tk.Label(info_frame, text="Conditions: --", 
                                        bg=self.bg_color, fg=self.text_color, font=('Arial', 12))
        self.condition_label.pack(anchor="w", pady=2)

    def load_weather_icon(self, icon_code, size=(60, 60)):
        """Load weather icon from OpenWeatherMap or return emoji as fallback"""
        if not IMAGES_AVAILABLE:
            return None
            
        try:
            from features.forecast import get_weather_icon_url
            icon_url = get_weather_icon_url(icon_code)
            response = requests.get(icon_url, timeout=5)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                image = image.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Could not load icon {icon_code}: {e}")
        
        # Fallback: return None and we'll use emoji
        return None

    def update_current_weather_icon(self, icon_code):
        """Update the current weather icon display"""
        # Clear existing icon
        for widget in self.icon_frame.winfo_children():
            widget.destroy()

        # Try to load actual weather icon
        icon_photo = self.load_weather_icon(icon_code, size=(80, 80))
        
        if icon_photo:
            # Use actual weather icon
            icon_label = tk.Label(self.icon_frame, image=icon_photo, bg=self.bg_color)
            icon_label.image = icon_photo  # Keep a reference
            icon_label.pack()
        else:
            # Use emoji fallback
            emoji = get_local_weather_emoji(icon_code)
            emoji_label = tk.Label(self.icon_frame, text=emoji, font=('Arial', 48), bg=self.bg_color)
            emoji_label.pack()

    def show_forecast(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name first.")
            return

        try:
            print(f"Fetching forecast for: {city}")  # Debug print
            forecast_data = get_forecast(city)
            print(f"Forecast data received: {len(forecast_data)} days")  # Debug print
            
            # Hide old forecast if exists
            if self.forecast_frame:
                self.forecast_frame.destroy()

            self.forecast_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
            self.forecast_frame.pack(pady=10, fill=tk.X, padx=20)

            # Title
            title_label = tk.Label(self.forecast_frame, text="5-Day Forecast", font=('Arial', 14, 'bold'),
                    bg=self.bg_color, fg=self.fg_color)
            title_label.pack(pady=(0, 10))

            # Check if we have forecast data
            if not forecast_data:
                tk.Label(self.forecast_frame, text="No forecast data available", 
                        bg=self.bg_color, fg=self.text_color).pack()
                return

            # Create a simple horizontal container instead of canvas for now
            forecast_container = tk.Frame(self.forecast_frame, bg=self.bg_color)
            forecast_container.pack(fill=tk.X, pady=5)

            # Create forecast cards - limit to first 5 days and skip today if it's partial
            forecast_items = list(forecast_data.items())
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            
            # Skip today's forecast if it's incomplete (start from tomorrow)
            start_index = 1 if forecast_items and forecast_items[0][0] == today else 0
            forecast_items = forecast_items[start_index:start_index+5]
            
            print(f"Creating {len(forecast_items)} forecast cards")  # Debug print
            
            for i, (date, data) in enumerate(forecast_items):
                print(f"Creating card for {date}: {data['description']}")  # Debug print
                
                # Create forecast card with fixed size
                forecast_card = tk.Frame(forecast_container, bg=self.text_color, relief=tk.RAISED, bd=2)
                forecast_card.pack(side=tk.LEFT, padx=8, pady=5, fill=tk.Y)
                
                # Inner frame with theme colors
                inner_frame = tk.Frame(forecast_card, bg=self.bg_color, padx=8, pady=8)
                inner_frame.pack(fill=tk.BOTH, expand=True)

                # Weather icon or emoji
                icon_photo = self.load_weather_icon(data['icon'], size=(40, 40))
                
                if icon_photo:
                    icon_label = tk.Label(inner_frame, image=icon_photo, bg=self.bg_color)
                    icon_label.image = icon_photo  # Keep a reference
                    icon_label.pack(pady=(0, 5))
                else:
                    emoji = get_local_weather_emoji(data['icon'])
                    emoji_label = tk.Label(inner_frame, text=emoji, font=('Arial', 24), bg=self.bg_color)
                    emoji_label.pack(pady=(0, 5))

                # Temperature conversion
                unit = self.temp_unit.get()
                high_temp = data['high'] if unit == "F" else (data['high'] - 32) * 5 / 9
                low_temp = data['low'] if unit == "F" else (data['low'] - 32) * 5 / 9

                # Format date nicely
                try:
                    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%a\n%b %d')
                except Exception as e:
                    print(f"Date formatting error: {e}")
                    formatted_date = date

                # Date
                date_label = tk.Label(inner_frame, text=formatted_date, 
                                    bg=self.bg_color, fg=self.text_color, 
                                    font=('Arial', 9, 'bold'), justify=tk.CENTER)
                date_label.pack(pady=(0, 3))

                # Condition (shortened)
                condition_text = data['description'].title()
                if len(condition_text) > 15:
                    condition_text = condition_text[:12] + "..."
                    
                condition_label = tk.Label(inner_frame, text=condition_text, 
                                         bg=self.bg_color, fg=self.text_color, 
                                         font=('Arial', 7), justify=tk.CENTER)
                condition_label.pack(pady=(0, 3))

                # Temperature
                temp_label = tk.Label(inner_frame, 
                                    text=f"H: {high_temp:.0f}°\nL: {low_temp:.0f}°", 
                                    bg=self.bg_color, fg=self.text_color, 
                                    font=('Arial', 8), justify=tk.CENTER)
                temp_label.pack()

            print("Forecast display completed")  # Debug print
            
            # Force update of the scrollable region
            self.scrollable_frame.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        except ValueError as ve:
            print(f"ValueError in forecast: {ve}")
            messagebox.showerror("Invalid City", f"Forecast error: {str(ve)}")
        except Exception as e:
            print(f"Exception in forecast: {e}")
            messagebox.showerror("Error", f"Unable to fetch forecast data: {str(e)}")
            import traceback
            traceback.print_exc()  # Print full stack trace for debugging

    def update_display(self):
        city = self.city_entry.get().strip()
        unit = self.temp_unit.get()

        if not city:
            messagebox.showerror("Error", "City name cannot be empty.")
            return

        try:
            data = fetch_current_weather(city)

            self.latest_weather_data = data
            temp = data['main']['temp']
            self.current_temp_f = temp
            humidity = data['main']['humidity']
            precip = data.get('rain', {}).get('1h', 0)
            condition = data['weather'][0]['description'].title()
            city_name = data['name']
            icon_code = data['weather'][0]['icon']

            if unit == "F":
                display_temp = temp
            else:
                display_temp = (temp - 32) * 5 / 9

            self.temp_label.config(text=f"Temperature: {round(display_temp, 1)}°{unit}")
            self.humidity_label.config(text=f"Humidity: {humidity}%")
            self.precip_label.config(text=f"Precipitation: {precip} in")
            self.condition_label.config(text=f"Conditions: {condition}")
            self.loc_label.config(text=f"Location: {city_name}")

            # Update weather icon
            self.update_current_weather_icon(icon_code)

            # Show compare button if not already there
            if self.compare_button is None:
                self.compare_button = tk.Button(self.scrollable_frame, text="Compare City",
                    command=self.compare_cities,
                    bg=self.fg_color, fg="white", activebackground=self.fg_color)
                self.compare_button.pack(pady=5)

        except ValueError as ve:
            messagebox.showerror("Invalid City", str(ve))
        except Exception as e:
            print(f"Unhandled error: {e}")
            messagebox.showerror("Error", "An unexpected error occurred while fetching weather data.")

    def temp_unit_update(self):
        if self.current_temp_f is not None:
            unit = self.temp_unit.get()
            if unit == "F":
                display_temp = self.current_temp_f
            else:
                display_temp = (self.current_temp_f - 32) * 5 / 9
            self.temp_label.config(text=f"Temperature: {round(display_temp, 1)}°{unit}")

    def clear_inputs(self):
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, "New York")
        self.temp_unit.set("F")
        self.temp_label.config(text="Temperature: --")
        self.humidity_label.config(text="Humidity: --")
        self.precip_label.config(text="Precipitation: --")
        self.condition_label.config(text="Conditions: --")
        self.loc_label.config(text="Location: --")
        self.latest_weather_data = None
        self.current_temp_f = None

        # Clear weather icon
        for widget in self.icon_frame.winfo_children():
            widget.destroy()

        # Hide compare button if exists
        if self.compare_button:
            self.compare_button.destroy()
            self.compare_button = None

        # Hide compare result if exists
        if self.compare_frame:
            self.compare_frame.destroy()
            self.compare_frame = None

        # Hide forecast if exists
        if self.forecast_frame:
            self.forecast_frame.destroy()
            self.forecast_frame = None

    def compare_cities(self):
        second_city = simpledialog.askstring("Compare City", "Enter a second city to compare:")
        if not second_city:
            return

        city1 = self.latest_weather_data['name']
        if second_city.strip().lower() == city1.lower():
            messagebox.showerror("Same City", "Please enter a different city to compare.")
            return

        try:
            data = fetch_current_weather(second_city)
            temp = data['main']['temp']
            if self.temp_unit.get() == "C":
                temp = (temp - 32) * 5 / 9
            humidity = data['main']['humidity']
            precip = data.get('rain', {}).get('1h', 0)
            condition = data['weather'][0]['description'].title()
            name = data['name']

            # Hide old comparison frame if it exists
            if self.compare_frame:
                self.compare_frame.destroy()

            self.compare_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
            self.compare_frame.pack(pady=5)

            tk.Label(self.compare_frame, text=f"--- Compared With ---", font=('Arial', 12, 'bold'),
                    bg=self.bg_color, fg=self.fg_color).pack()

            tk.Label(self.compare_frame, text=f"Location: {name}", bg=self.bg_color, fg=self.text_color).pack()
            tk.Label(self.compare_frame, text=f"Temperature: {round(temp, 1)}°{self.temp_unit.get()}",
                    bg=self.bg_color, fg=self.text_color).pack()
            tk.Label(self.compare_frame, text=f"Humidity: {humidity}%", bg=self.bg_color, fg=self.text_color).pack()
            tk.Label(self.compare_frame, text=f"Precipitation: {precip} in", bg=self.bg_color, fg=self.text_color).pack()
            tk.Label(self.compare_frame, text=f"Conditions: {condition}", bg=self.bg_color, fg=self.text_color).pack()

        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Unable to fetch data for the second city.")

    def apply_theme(self, theme):
        # Apply the theme and update colors
        self.current_theme = theme
        theme_config = self.themes.get(theme)
        if not theme_config:
            # Fallback to superhero if theme not found
            print(f"Theme '{theme}' not found, using superhero theme")
            theme = "superhero"
            theme_config = self.themes.get(theme)

        self.bg_color = theme_config["bg_color"]
        self.fg_color = theme_config["fg_color"]
        self.text_color = theme_config["text_color"]

        # Save the theme preference
        self.save_theme_preference(theme)

        # Update canvas and scrollable frame colors
        if hasattr(self, 'canvas'):
            self.canvas.configure(bg=self.bg_color)
        if hasattr(self, 'scrollable_frame'):
            self.scrollable_frame.configure(bg=self.bg_color)

        self.root.configure(bg=self.bg_color)
        
        # Update all widgets with new theme
        self.update_all_widgets_theme()

    def update_all_widgets_theme(self):
        """Update all widgets in the application with the current theme"""
        # Update root window widgets
        for widget in self.root.winfo_children():
            self.update_widget_theme(widget)
        
        # Update scrollable frame widgets
        if hasattr(self, 'scrollable_frame'):
            self.update_widget_theme(self.scrollable_frame)

    def update_widget_theme(self, widget):
        try:
            if isinstance(widget, (tk.Label, tk.Frame, tk.Button, tk.Canvas)):
                widget.configure(bg=self.bg_color)
                if isinstance(widget, (tk.Label, tk.Button)):
                    widget.configure(fg=self.text_color)
        except tk.TclError:
            pass  # Some widgets don't support these options
        
        # Recursively update child widgets
        for child in widget.winfo_children():
            self.update_widget_theme(child)

    def open_theme_selector(self):
        # More robust check to prevent multiple theme selector windows
        if self.theme_selector_window is not None:
            try:
                # Try to bring existing window to front
                self.theme_selector_window.lift()
                self.theme_selector_window.focus_force()
                return
            except (tk.TclError, AttributeError):
                # Window was destroyed but reference wasn't cleared
                self.theme_selector_window = None

        # Create the theme selector - let it create its own window
        # Don't create a Toplevel here since ThemeSelector creates its own
        def theme_callback(theme):
            self.apply_theme(theme)
            # Clear the reference when theme is applied
            self.theme_selector_window = None
        
        # Create the theme selector and let it manage its own window
        theme_selector = ThemeSelector(self.root, theme_callback, self.get_theme_list(), self.current_theme)
        self.theme_selector_window = theme_selector.window
        
        # Set up proper cleanup when window is closed
        def on_window_destroy():
            self.theme_selector_window = None
        
        self.theme_selector_window.protocol("WM_DELETE_WINDOW", lambda: [
            on_window_destroy(),
            self.theme_selector_window.destroy() if self.theme_selector_window else None
        ])

def main():
    root = tk.Tk()
    app = WeatherDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()