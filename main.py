import requests
import streamlit as st
from datetime import datetime
import os

# Title
st.title("🌍 IP & Location Finder")

st.set_page_config(page_title="IP Tracker", layout="centered")

# Function to get the public IP
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        response.raise_for_status()
        return response.json().get('ip', 'Unavailable')
    except Exception as e:
        st.error(f"Error getting IP: {e}")
        return 'Unavailable'


# Function to get location info
def get_location(ip_address):
    try:
        url = f'https://ipinfo.io/{ip_address}/json'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error getting location: {e}")
        return {}


# Save data to nicely formatted TXT file
def save_to_txt(ip, location):
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"ip_location_{timestamp}.txt"

    data = (
        "📍 IP & Location Info\n"
        "-------------------------\n"
        f"Public IP   : {ip}\n"
        f"City        : {location.get('city', 'Not available')}\n"
        f"Region      : {location.get('region', 'Not available')}\n"
        f"Country     : {location.get('country', 'Not available')}\n"
        f"Coordinates : {location.get('loc', 'Not available')}\n"
    )

    # Save using UTF-8 encoding
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

    st.success(f"📁 Info saved to `{filename}`")



# Main logic
public_ip = get_public_ip()
location = get_location(public_ip)

# Display info
st.write(f"**Public IP:** {public_ip}")
st.write(f"**City:** {location.get('city', 'Not available')}")
st.write(f"**Region:** {location.get('region', 'Not available')}")
st.write(f"**Country:** {location.get('country', 'Not available')}")
st.write(f"**Coordinates:** {location.get('loc', 'Not available')}")

# Map
coords = location.get("loc", "")
if coords:
    try:
        lat, lon = map(float, coords.split(","))
        st.map({"lat": [lat], "lon": [lon]})
    except ValueError:
        st.warning("Could not parse coordinates for map display.")

# Save to text file
save_to_txt(public_ip, location)

# Final sassy flair
st.title("I got you, now run before the hackers do ;).")

#streamlit run main.py
