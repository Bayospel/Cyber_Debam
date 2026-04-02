import phonenumbers, os
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode

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
            print(report)

            # Save to a secret file for your records
            with open("recon_targets.txt", "a") as f:
                f.write(report)

            speech = f"Oga, I don pin am. Target is in {location_desc}. Coordinates: {lat}, {lng}."
            os.system(f'termux-tts-speak "{speech}"')
        else:
            print("[-] Geocoding failed to find precise coordinates.")
            os.system('termux-tts-speak "Boss, I see the region but I no fit get the coordinates."')

    except Exception as e:
        print(f"Error: {e}")
        os.system('termux-tts-speak "Boss, check the number format. Add + sign."')

if __name__ == "__main__":
    target = input("Enter Phone Number (+234...): ")
    track_number(target)
