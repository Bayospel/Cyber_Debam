import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import streamlit as st

# --- YOUR ACTIVE API KEY ---
API_KEY = "60f755b8fa124caf8e766c27758d4b23"
geocoder_api = OpenCageGeocode(API_KEY)

def track_number(number_str):
    try:
        # Parse the number
        parsed_number = phonenumbers.parse(number_str)
        location_desc = geocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en")

        # --- PRECISE GEOLOCATION ---
        results = geocoder_api.geocode(location_desc)

        if results and len(results) > 0:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
            precise_address = results[0]['formatted']

            report = f"""
[ Bayospel Precise Recon ]
---------------------------
Target: {number_str}
Carrier: {service_provider}
General Region: {location_desc}
Precise Address: {precise_address}
Coordinates: {lat}, {lng}
Map Link: https://www.google.com/maps?q={lat},{lng}
---------------------------
"""
            # Return the data instead of just printing it
            return True, report, lat, lng
        else:
            return False, "Boss, I see the region but I no fit get the coordinates.", 0, 0

    except Exception as e:
        return False, f"Error: {e}. Ensure you include the + sign (e.g., +234...)", 0, 0
