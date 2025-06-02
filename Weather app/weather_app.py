import requests

# Replace 'your_api_key_here' with your OpenWeatherMap API key
API_KEY = "ae17d659f0b77f007aba37f96c48838e"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(location):
    # Set up the parameters for the API request
    params = {
        "q": location,  # The city name or ZIP code entered by the user
        "appid": API_KEY,  # Your API key
        "units": "metric"  # Use Celsius for temperature
    }
    
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
        print(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Error fetching data: {err}")
        return None

def display_weather(weather):
    # Display the weather data if we got it
    if weather:
        print("\nWeather Information:")
        print(f"City: {weather['city']}")
        print(f"Temperature: {weather['temperature']}°C")
        print(f"Humidity: {weather['humidity']}%")
        print(f"Conditions: {weather['description'].capitalize()}")
    else:
        print("Could not fetch weather data. Please check your input or API key.")

def main():
    # Main function to run the app
    print("Welcome to the Weather App!")
    location = input("Enter a city name or ZIP code: ")
    weather_data = get_weather_data(location)
    display_weather(weather_data)

if __name__ == "__main__":
    main()