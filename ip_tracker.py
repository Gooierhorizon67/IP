import streamlit as st
import requests
import datetime
from streamlit_javascript import st_javascript

# --- Page config and CSS for fun background and style
st.set_page_config(page_title="Icce--cube", layout="centered")
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                    url("https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1400&q=80");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: #fff;
    }
    .title {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        font-weight: bold;
        font-size: 3rem;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 5px;
        color: #ff6600;
        text-shadow: 2px 2px #000;
    }
    .subtitle {
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 30px;
        color: #ffd966;
        text-shadow: 1px 1px #000;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Glowing sunset</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Run before the hackers do! 🏃‍♂️💨</div>', unsafe_allow_html=True)


# Get client IP via JS
ip = st_javascript(
    "await fetch('https://api.ipify.org?format=json').then(res => res.json()).then(data => data.ip)"
)

if ip:
    st.success(f"Your IP: {ip}")
    st.markdown('<div class="subtitle">See ya lil bro 👋</div>', unsafe_allow_html=True)

    try:
        loc = requests.get(f"https://ipinfo.io/{ip}/json").json()
        city = loc.get("city", "N/A")
        country = loc.get("country", "N/A")
        timezone = loc.get("timezone", "N/A")

        st.write(f"City: {city}")
        st.write(f"Country: {country}")
        st.write(f"Timezone: {timezone}")

        if "loc" in loc:
            lat, lon = map(float, loc["loc"].split(","))
            st.map({"lat": [lat], "lon": [lon]})

        # Save to file
        log_entry = f"{datetime.datetime.now()} - IP: {ip} | City: {city} | Country: {country} | Timezone: {timezone}\n"
        with open("ip_log.txt", "a") as log:
            log.write(log_entry)

    except Exception as e:
        st.error(f"Could not fetch location info: {e}")
else:
    st.info("Waiting for your browser to send the IP...")