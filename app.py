
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Convert weather codes into readable conditions
def get_weather_condition(code):

    conditions = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing Rime Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        71: "Slight Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",
        80: "Rain Showers",
        81: "Moderate Rain Showers",
        82: "Heavy Rain Showers",
        95: "Thunderstorm"
    }

    return conditions.get(code, "Unknown Weather")


# Convert wind direction degrees into compass direction
def get_wind_direction(degrees):

    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    index = round(degrees / 45) % 8

    return directions[index]


# Weather API route
@app.route("/api/weather")
def get_weather():

    city = request.args.get("city")

    if not city:
        return jsonify({"error": "Please enter a city name"}), 400

    try:
        # Step 1: Find city coordinates
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 5,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        geo_response.raise_for_status()

        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return jsonify({"error": "City not found"}), 404

        # location = geo_data["results"][0]

        # latitude = location["latitude"]
        # longitude = location["longitude"]
        location = geo_data["results"][0]

        print("Selected location:", location)
        print("Coordinates:", location["latitude"], location["longitude"])

        latitude = location["latitude"]
        longitude = location["longitude"]

        # Step 2: Get current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "weather_code,"
                "wind_speed_10m,"
                "wind_direction_10m,"
                "surface_pressure"
            ),
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        weather_response.raise_for_status()

        weather_data = weather_response.json()
        current = weather_data["current"]

        # Step 3: Prepare data for frontend
        result = {
            "city": location["name"],
            "country": location.get("country", ""),
            "temperature": current["temperature_2m"],
            "condition": get_weather_condition(
                current["weather_code"]
            ),
            "feels_like": current["apparent_temperature"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"],
            "wind_direction": get_wind_direction(
                current["wind_direction_10m"]
            ),
            "pressure": current["surface_pressure"],
            "message": "Here is the current weather!"
        }

        return jsonify(result)

    except requests.exceptions.RequestException:
        return jsonify({
            "error": "Unable to connect to the weather service. Please try again."
        }), 503

    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Unexpected weather data received."
        }), 502


if __name__ == "__main__":
    app.run(debug=True)
