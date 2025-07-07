import tkinter as tk
from tkinter import ttk, messagebox
from data.data import fetch_current_weather

class WeatherDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("420x350")

        self.latest_weather_data = None
        self.current_temp_f = None

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.bg_color = "#E6E6FA"
        self.fg_color = "#5D3A7D"
        self.text_color = "#333333"
        self.root.configure(bg=self.bg_color)

        title_label = tk.Label(self.root, text="Weather Dashboard",
                               font=('Arial', 18, 'bold'),
                               bg=self.fg_color, fg="white", pady=10)
        title_label.pack(fill=tk.X)

        input_frame = tk.Frame(self.root, bg=self.bg_color)
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

        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=5)

        update_btn = tk.Button(button_frame, text="Update", command=self.update_display,
                               bg=self.fg_color, fg="white", activebackground=self.fg_color)
        update_btn.pack(side=tk.LEFT, padx=10)

        clear_btn = tk.Button(button_frame, text="Clear", command=self.clear_inputs,
                              bg=self.fg_color, fg="white", activebackground=self.fg_color)
        clear_btn.pack(side=tk.LEFT, padx=10)

        result_frame = tk.Frame(self.root, bg=self.bg_color)
        result_frame.pack(pady=15)

        self.temp_label = tk.Label(result_frame, text="Temperature: --", bg=self.bg_color, fg=self.text_color, font=('Arial', 12))
        self.temp_label.pack(anchor="w", padx=10, pady=2)

        self.humidity_label = tk.Label(result_frame, text="Humidity: --", bg=self.bg_color, fg=self.text_color, font=('Arial', 12))
        self.humidity_label.pack(anchor="w", padx=10, pady=2)

        self.precip_label = tk.Label(result_frame, text="Precipitation: --", bg=self.bg_color, fg=self.text_color, font=('Arial', 12))
        self.precip_label.pack(anchor="w", padx=10, pady=2)

        self.condition_label = tk.Label(result_frame, text="Conditions: --", bg=self.bg_color, fg=self.text_color, font=('Arial', 12))
        self.condition_label.pack(anchor="w", padx=10, pady=2)

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

            if unit == "F":
                display_temp = temp
            else:
                display_temp = (temp - 32) * 5 / 9

            self.temp_label.config(text=f"Temperature: {round(display_temp, 1)}°{unit}")
            self.humidity_label.config(text=f"Humidity: {humidity}%")
            self.precip_label.config(text=f"Precipitation: {precip} in")
            self.condition_label.config(text=f"Conditions: {condition}")

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
        self.latest_weather_data = None
        self.current_temp_f = None

def main():
    root = tk.Tk()
    app = WeatherDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
