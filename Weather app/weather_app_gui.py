import requests
import tkinter as tk
from tkinter import messagebox
import geocoder  # Import the geocoder library for GPS integration

# Replace 'your_api_key_here' with your OpenWeatherMap API key
API_KEY = "ae17d659f0b77f007aba37f96c48838e"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(location):
    # Determine the parameters for the API request
    if location.lower() == "current":
        try:
            # Use geocoder to get the user's location based on IP address
            g = geocoder.ip('me')
            lat, lon = g.latlng
            if lat is None or lon is None:
                messagebox.showerror("Error", "Could not determine your location.")
                return None
            params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get location: {e}")
            return None
    else:
        params = {"q": location, "appid": API_KEY, "units": "metric"}

    # Try to fetch data from the API
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Check for errors in the response
        data = response.json()  # Convert the response to JSON (a Python dictionary)
        
        # Extract the weather information we need
        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }
        return weather
    
    # Handle errors if the API call fails
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("Error", f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.RequestException as err:
        messagebox.showerror("Error", f"Error fetching data: {err}")
        return None

def display_weather():
    # Get the location from the input field
    location = entry.get()
    # Check if the input is empty
    if not location:
        messagebox.showwarning("Input Error", "Please enter a city, ZIP code, or 'current'.")
        return
    
    # Fetch the weather data
    weather = get_weather_data(location)
    if weather:
        # Update the label with the weather information
        result_label.config(
            text=f"City: {weather['city']}\n"
                 f"Temperature: {weather['temperature']}°C\n"
                 f"Humidity: {weather['humidity']}%\n"
                 f"Conditions: {weather['description'].capitalize()}"
        )
    else:
        # Display an error message if no data is returned
        result_label.config(text="Could not fetch weather data.")

# Create the main GUI window
root = tk.Tk()
root.title("Weather App")
root.geometry("300x300")  # Set window size (width x height)

# Add a label to prompt the user
label = tk.Label(root, text="Enter City, ZIP Code, or 'current':")
label.pack(pady=10)  # Add some padding

# Add an input field (Entry widget)
entry = tk.Entry(root, width=20)
entry.pack()

# Add a button to fetch the weather
button = tk.Button(root, text="Get Weather", command=display_weather)
button.pack(pady=10)

# Add a label to display the weather results
result_label = tk.Label(root, text="", justify="left", font=("Arial", 12))
result_label.pack(pady=10)

# Start the GUI event loop
root.mainloop()