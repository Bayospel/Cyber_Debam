import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import requests

# --- SYSTEM KEYS ---
OPENCAGE_KEY = "60f755b8fa124caf8e766c27758d4b23"
TRESTLE_KEY = "2KCmXE58pz1H1sPz9kV2Kq4wT24Ve675zqFFa2Ud"

geocoder_api = OpenCageGeocode(OPENCAGE_KEY)

def track_number(number_str):
    try:
        # 1. BASIC PARSING
        parsed_number = phonenumbers.parse(number_str)
        location_desc = geocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en")

        # 2. DEEP IDENTITY TRACE
        identity_report = ""
        trestle_url = f"https://api.trestleiq.com/v1/phone_enrichment?phone={number_str}"
        headers = {"x-api-key": TRESTLE_KEY, "Accept": "application/json"}
        
        try:
            t_res = requests.get(trestle_url, headers=headers, timeout=5)
            if t_res.status_code == 200:
                data = t_res.json()
                person = data.get('person', {})
                name = person.get('name', 'UNKNOWN')
                dob = person.get('date_of_birth', 'N/A')
                relatives = ", ".join([r.get('name') for r in person.get('relatives', [])[:2]])
                
                identity_report = f"\n👤 IDENTITY MASK BYPASSED:\nName: {name}\nDOB: {dob}\nFamily: {relatives if relatives else 'None Found'}"
        except:
            identity_report = "\n[!] Identity server timeout."

        # 3. PRECISE GEOLOCATION
        results = geocoder_api.geocode(location_desc)
        lat, lng, addr = 0, 0, "Unknown"

        if results and len(results) > 0:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
            addr = results[0]['formatted']

        # 4. FINAL TACTICAL REPORT
        report = f"""
[ DEBAM AI - DEEP TRACE REPORT ]
---------------------------
Target: {number_str}
Carrier: {service_provider}
{identity_report}
Location: {location_desc}
Precise Region: {addr}
Coordinates: {lat}, {lng}
---------------------------
Status: ACCESS SUCCESSFUL
"""
        return True, report, lat, lng

    except Exception as e:
        return False, f"Error: {e}", 0, 0
        return False, f"Error: {e}. Ensure you include the + sign (e.g., +1...)", 0, 0
👤 IDENTITY MASK BYPASSED:
Full Name: {name}
Date of Birth: {dob}
Associates: {relatives if relatives else 'None Found'}
---------------------------"""
        except:
            identity_report = "\n[!] Identity server timeout or non-US target."

        # 3. PRECISE GEOLOCATION (OpenCage)
        results = geocoder_api.geocode(location_desc)
        lat, lng, precise_address = 0, 0, "Unknown"

        if results and len(results) > 0:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
            precise_address = results[0]['formatted']

        # 4. FINAL TACTICAL REPORT
        report = f"""
[ DEBAM AI - DEEP TRACE REPORT ]
---------------------------
Target: {number_str}
Carrier: {service_provider}
{identity_report}
Location: {location_desc}
Precise Region: {precise_address}
Coordinates: {lat}, {lng}
Map: https://www.google.com/maps?q={lat},{lng}
---------------------------
Status: ACCESS SUCCESSFUL
"""
        return True, report, lat, lng

    except Exception as e:
        return False, f"Error: {e}. Ensure you include the + sign (e.g., +1...)", 0, 0
            return True, report, lat, lng
        else:
            return False, "Boss, I see the region but I no fit get the coordinates.", 0, 0

    except Exception as e:
        return False, f"Error: {e}. Ensure you include the + sign (e.g., +234...)", 0, 0
