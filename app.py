import requests
import geocoder
from datetime import datetime, timedelta


def get_hanafi_prayer_times():
    # Get date input from user
    date_input = input(
        "Enter date (DD-MM-YYYY) or press Enter for today: ").strip()

    # Validate and parse date
    try:
        if date_input:
            selected_date = datetime.strptime(date_input, "%d-%m-%Y")
        else:
            selected_date = datetime.now()
    except ValueError:
        print("Invalid date format. Please use DD-MM-YYYY format.")
        return

    # Get location using IP address
    location = geocoder.ip('me')
    if not location:
        print("Could not determine location. Please check your internet connection.")
        return

    # Get coordinates
    lat, lng = location.latlng

    # Get address components
    city = location.city
    country = location.country
    address = f"{city}, {country}" if city and country else "your location"

    # API parameters
    params = {
        "latitude": lat,
        "longitude": lng,
        "method": 2,  # ISNA method
        "school": 1,  # Hanafi school
        "tune": "0,0,0,0,0,0,0,0,0",
        "date": selected_date.strftime("%d-%m-%Y")
    }

    try:
        # Get prayer times from Aladhan API
        response = requests.get(
            "http://api.aladhan.com/v1/timings", params=params)
        response.raise_for_status()

        data = response.json()
        timings = data["data"]["timings"]
        date = data["data"]["date"]["readable"]

        # Display prayer times
        print(f"\nPrayer Times for {address} ({date}) [Hanafi Method]")
        print("-" * 40)
        print(f"Fajr:    {timings['Fajr']}")
        print(f"Sunrise: {timings['Sunrise']}")
        print(f"Dhuhr:   {timings['Dhuhr']}")
        print(f"Asr:     {timings['Asr']}")
        print(f"Maghrib: {timings['Maghrib']}")
        print(f"Isha:    {timings['Isha']}")
        print("-" * 40)
        print("Note: Prayer times are calculated using Hanafi school of thought")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching prayer times: {e}")


if __name__ == "__main__":
    print("Fetching prayer times...")
    get_hanafi_prayer_times()
