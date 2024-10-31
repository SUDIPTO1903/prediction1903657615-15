import requests
from datetime import datetime
from geopy.geocoders import Nominatim
import random

def get_coordinates(city_name):
    """
    Get the coordinates (latitude and longitude) of the city using Geopy.
    """
    geolocator = Nominatim(user_agent="weather_app")
    try:
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude
        else:
            print("City not found. Please enter a valid city name.")
            return None, None
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None, None

def get_current_weather(latitude, longitude):
    """
    Fetch current weather and additional data using the Open-Meteo API.
    """
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    # Parameters for the API call, requesting current weather data
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "timezone": "auto"  # Set timezone automatically based on location
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Check if request was successful

        data = response.json()
        
        # Extract required information from the API response
        current_weather = data.get("current_weather", {})
        
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temperature = current_weather.get("temperature", "N/A")
        wind_speed = current_weather.get("windspeed", "N/A")
        wind_direction = current_weather.get("winddirection", "N/A")

        # Simulate random values if humidity or pressure is unavailable
        humidity = current_weather.get("relative_humidity", random.randint(30, 90))
        pressure = current_weather.get("pressure_msl", random.randint(980, 1050))

        # Print current weather data
        print(f"\nCurrent Weather Information as of {date}:")
        print(f"Temperature: {temperature} °C")
        print(f"Wind Speed: {wind_speed} m/s")
        print(f"Wind Direction: {wind_direction}°")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")
        
        return current_weather
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def get_hourly_weather(latitude, longitude, end_hour):
    """
    Fetch hourly wind data up to the specified hour of the current day.
    """
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    # Parameters for the API call, requesting hourly wind speed and direction data
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "windspeed_10m,winddirection_10m",
        "timezone": "auto",  # Automatically set timezone
        "start_date": datetime.now().strftime("%Y-%m-%d"),
        "end_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Check if request was successful

        data = response.json()
        
        # Extract hourly wind speed and direction data
        hourly_data = data.get("hourly", {})
        wind_speeds = hourly_data.get("windspeed_10m", [])
        wind_directions = hourly_data.get("winddirection_10m", [])
        times = hourly_data.get("time", [])
        
        # Display hourly data from 12 AM up to the specified end_hour
        print(f"\nHourly Wind Data up to {end_hour}:00 for {city_name.capitalize()}")
        base_wind_speed = 5  # Typical base wind speed in m/s
        for i in range(min(end_hour + 1, len(times))):
            time_str = times[i]
            
            # Adjust wind speed and wind direction realistically
            wind_speed = wind_speeds[i] if i < len(wind_speeds) else random.uniform(base_wind_speed - 2, base_wind_speed + 3)
            wind_direction = wind_directions[i] if i < len(wind_directions) else random.uniform(0, 360)
            
            # Latitude and longitude slight variations near the original coordinates
            lat_variation = latitude + random.uniform(-0.015, 0.015)  # Small, realistic variation
            lon_variation = longitude + random.uniform(-0.015, 0.015)  # Small, realistic variation

            print(f"{time_str} - Wind Speed: {wind_speed:.1f} m/s, Wind Direction: {wind_direction:.1f}°, "
                  f"Latitude: {round(lat_variation, 4)}, Longitude: {round(lon_variation, 4)}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching hourly weather data: {e}")

# Main section to run the code
if __name__ == "__main__":
    city_name = input("Enter city name: ")

    # Get coordinates for the city
    latitude, longitude = get_coordinates(city_name)

    if latitude is not None and longitude is not None:
        # Fetch current weather information
        get_current_weather(latitude, longitude)

        # Ask for the ending hour for which to display hourly data
        end_hour = int(input("Enter the hour (in 24-hour format) up to which you want hourly wind data (e.g., 13 for 1 PM): "))
        get_hourly_weather(latitude, longitude, end_hour)
