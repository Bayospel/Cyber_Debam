import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import requests

OPENCAGE_KEY = "60f755b8fa124caf8e766c27758d4b23"
TRESTLE_KEY = "2KCmXE58pz1H1sPz9kV2Kq4wT24Ve675zqFFa2Ud"
geocoder_api = OpenCageGeocode(OPENCAGE_KEY)

def track_number(number_str):
    try:
        parsed_number = phonenumbers.parse(number_str)
        location_desc = geocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en")
        
        # --- IDENTITY DEBUG BLOCK ---
        identity_report = ""
        trestle_url = f"https://api.trestleiq.com/v1/phone_enrichment?phone={number_str}"
        headers = {"x-api-key": TRESTLE_KEY, "Accept": "application/json"}
        
        try:
            t_res = requests.get(trestle_url, headers=headers, timeout=5)
            if t_res.status_code == 200:
                data = t_res.json()
                person = data.get('person')
                if person:
                    name = person.get('name', 'N/A')
                    dob = person.get('date_of_birth', 'N/A')
                    identity_report = f"\n👤 IDENTITY FOUND:\nName: {name}\nDOB: {dob}"
                else:
                    identity_report = "\n👤 IDENTITY: No personal record found (Business/VOIP)."
            else:
                # THIS LINE WILL TELL US IF THE KEY IS BAD
                identity_report = f"\n⚠️ IDENTITY ERROR: API returned status {t_res.status_code}"
        except Exception as e:
            identity_report = f"\n[!] Identity Timeout: {str(e)}"

        # --- GEOLOCATION ---
        results = geocoder_api.geocode(location_desc)
        lat, lng, addr = 0, 0, "Unknown"
        if results and len(results) > 0:
            lat, lng = results[0]['geometry']['lat'], results[0]['geometry']['lng']
            addr = results[0]['formatted']

        report = f"""
[ DEBAM AI - DEEP TRACE REPORT ]
---------------------------
Target: {number_str}
Carrier: {service_provider if service_provider else 'Searching...'}
{identity_report}
Location: {location_desc}
Region: {addr}
Coordinates: {lat}, {lng}
---------------------------
Status: ACCESS SUCCESSFUL
"""
        return True, report, lat, lng
    except Exception as e:
        return False, f"System Error: {e}", 0, 0
