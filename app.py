import streamlit as st
import os
import random
import time
from groq import Groq
from supabase import create_client, Client
import bayo_track
import bayo_recon
import bayo_exploit
import bayo_brute
import bayo_shodan  # Ensure bayo_shodan.py is in your repo
import logo_data    # This loads your 870KB logo instantly from your new file
import streamlit.components.v1 as components

# --- 1. TACTICAL UI SETUP ---
st.set_page_config(page_title="BAYOSPEL GLOBAL OS", layout="wide", initial_sidebar_state="expanded")

# --- 2. THE SUPABASE ENGINE ---
# Make sure these are in your Streamlit Secrets!
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("CRITICAL: Supabase Secrets missing. Check your Dashboard!")
    st.stop()

# --- 3. THE GATEKEEPER & AUTH SYSTEM (FIXED WELCOME SCREEN) ---
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

if not st.session_state.access_granted:
    st.markdown(
        f"""
        <style>
            .gatekeeper-container {{
                background-color: #050505;
                height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                position: fixed;
                top: 0; left: 0; width: 100%;
                z-index: 99999;
                font-family: 'Courier New', monospace;
            }}
            .welcome-text {{
                color: #00FF41;
                font-size: 35px;
                font-weight: bold;
                margin-top: 20px;
                text-transform: uppercase;
                letter-spacing: 5px;
                text-shadow: 0 0 20px #00FF41;
            }}
            .boss-text {{
                color: white;
                font-size: 18px;
                margin-top: 10px;
                letter-spacing: 8px;
                opacity: 0.8;
                margin-bottom: 20px;
            }}
            .glow-img {{
                border-radius: 50%;
                box-shadow: 0 0 60px #00FF41;
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); opacity: 0.8; }}
                50% {{ transform: scale(1.05); opacity: 1; }}
                100% {{ transform: scale(1); opacity: 0.8; }}
            }}
            /* Tab Styling for Auth */
            .stTabs [data-baseweb="tab-list"] {{ gap: 30px; justify-content: center; }}
            .stTabs [data-baseweb="tab"] {{
                background-color: transparent;
                border: 1px solid #00FF41;
                color: #00FF41 !important;
                padding: 10px 30px;
                border-radius: 5px;
            }}
            .stTabs [aria-selected="true"] {{
                background-color: #00FF41 !important;
                color: black !important;
            }}
            #MainMenu, footer, header {{ visibility: hidden; }}
        </style>
        <div class="gatekeeper-container">
            <img src="{logo_data.LOGO_BASE64}" width="250" class="glow-img">
            <div class="welcome-text">WELCOME TO DEBAM AI OS</div>
            <div class="boss-text">CREATED BY THE BIG BOSS BAYONLE</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Position the Auth UI correctly
    st.write("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    
    _, auth_col, _ = st.columns([1, 1.8, 1])
    
    with auth_col:
        auth_tab, reg_tab, reset_tab = st.tabs(["🔑 LOGIN", "📝 SIGN UP", "🛰️ RECOVERY"])
        
        with auth_tab:
            email_input = st.text_input("EMAIL", placeholder="commander@bayospel.os")
            pass_input = st.text_input("PASSWORD", type="password")
            if st.button("INITIALIZE SYSTEM ACCESS", use_container_width=True):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email_input, "password": pass_input})
                    st.success("ACCESS GRANTED. SYNCING...")
                    st.session_state.access_granted = True
                    time.sleep(1)
                    st.rerun()
                except Exception:
                    st.error("INVALID CREDENTIALS. ACCESS DENIED.")

        with reg_tab:
            st.markdown("<h4 style='color:white; text-align:center;'>NEW COMMANDER REGISTRATION</h4>", unsafe_allow_html=True)
            new_name = st.text_input("CHOOSE USERNAME")
            new_email = st.text_input("OPERATIONAL EMAIL")
            new_phone = st.text_input("PHONE (WITH COUNTRY CODE)")
            new_pass = st.text_input("CREATE ACCESS PASSCODE", type="password")
            
            if st.button("EXECUTE REGISTRATION", use_container_width=True):
                try:
                    res = supabase.auth.sign_up({
                        "email": new_email,
                        "password": new_pass,
                        "options": {
                            "data": {
                                "full_name": new_name,
                                "phone_number": new_phone
                            }
                        }
                    })
                    st.info("Verification sent! Confirm your email to log in.")
                except Exception as e:
                    st.error(f"REGISTRATION FAILED: {e}")

        with reset_tab:
            st.markdown("<p style='color:gray;'>Enter email to receive a secure recovery link.</p>", unsafe_allow_html=True)
            r_email = st.text_input("RECOVERY EMAIL")
            if st.button("SEND RECOVERY SIGNAL", use_container_width=True):
                try:
                    supabase.auth.reset_password_for_email(r_email)
                    st.success("Check your inbox for reset instructions.")
                except:
                    st.error("System failed to find email.")
    st.stop()

# --- 4. PWA INSTALLATION ENGINE ---
components.html(
    """
    <script>
    navigator.serviceWorker.getRegistrations().then(function(registrations) {
        for(let registration of registrations) { registration.unregister(); }
    });
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function() {
        navigator.serviceWorker.register('https://raw.githubusercontent.com/Bayospel/cyber_debam/main/service-worker.js');
      });
    }
    </script>
    <link rel="manifest" href="https://raw.githack.com/Bayospel/cyber_debam/main/manifest.json?v=2">
    <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/Bayospel/cyber_debam/main/logo.png">
    """,
    height=0,
)

# --- 5. THE ULTIMATE VISIBILITY FIX (CSS + CHAT BACKGROUND) ---
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
    
    [data-testid="stSidebar"] {{ background-color: #0a0a0a; border-right: 1px solid #00FF41; }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {{ color: #FFFFFF !important; }}
    
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
    [data-testid="stChatMessageAvatarAssistant"] span {{ display: none !important; }}

    .stChatMessage p {{ color: #FFFFFF !important; font-size: 1.1rem !important; line-height: 1.6; }}
    .stChatMessage strong {{ color: #00FF41 !important; }}
    .stChatInput textarea {{ color: #00FF41 !important; }}
    .stButton>button {{ background-color: #00FF41; color: black; font-weight: bold; width: 100%; border-radius: 10px; border: none; }}
    .stButton>button:hover {{ background-color: #00cc33; color: white; }}
</style>
""", unsafe_allow_html=True)

# --- 6. SMART KEY ROTATOR ENGINE ---
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
        You speak English, Yoruba, and Pidgin fluently. 
        Mix them naturally (e.g. 'Boss, mo ti set, iyalaya won!'). 
        Use slang like: Abeg, Omo, No shaking, Standard, Correct. 
        Respect Bayonle as the Only Boss."""

# --- 7. SIDEBAR SYSTEM ---
st.sidebar.image(logo_data.LOGO_BASE64, use_container_width=True)
st.sidebar.title("💀 DEBAM OS v4.8")
st.sidebar.markdown(f"<span style='color:#00FF41'>Commander:</span> <span style='color:white'>Bayonle</span>", unsafe_allow_html=True)

menu = st.sidebar.radio("SQUAD SELECTION", [
    "AI Commander", 
    "Web Recon (Scanner)", 
    "Network Eye (Shodan)", 
    "Target Tracker (OSINT)", 
    "Exploit Lab (CVE)", 
    "Brute Force Simulator",
    "Phish-Check (URL Analyzer)"
])

st.sidebar.markdown("---")
if st.sidebar.button("LOCK SYSTEM (LOGOUT)"):
    st.session_state.access_granted = False
    st.rerun()

# --- 8. FUNCTIONAL MODULES ---

# MODULE 1: AI COMMANDER
if menu == "AI Commander":
    st.title("📟 TACTICAL BRAIN INTERFACE")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Talk to Debam (Eng/Yor/Pid)..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            client = get_groq_client()
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": get_manual()}] + st.session_state.messages
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except:
                st.error("COMMUNICATION ERROR: SIGNAL LOST.")

# MODULE 2: WEB RECON
elif menu == "Web Recon (Scanner)":
    st.title("🌐 WEB RECONNAISSANCE")
    st.write("Deep analysis of target website infrastructure.")
    target = st.text_input("Enter Target URL (e.g., example.com):")
    if st.button("Start Full Recon Scan"):
        if target:
            with st.spinner("Executing tactical recon scripts..."):
                try:
                    result = bayo_recon.full_recon(target)
                    st.code(result)
                except Exception as e:
                    st.error(f"Recon Error: {e}")
        else:
            st.warning("Commander, provide a target URL first!")

# MODULE 3: NETWORK EYE (SHODAN)
elif menu == "Network Eye (Shodan)":
    st.title("👁️ NETWORK EYE: IP ENRICHMENT")
    st.write("Direct Shodan integration for port and vulnerability analysis.")
    ip_input = st.text_input("Enter Target IP Address:")
    if st.button("Run Instant Shodan Scan"):
        if ip_input:
            with st.spinner("Querying Global Intelligence..."):
                try:
                    result = bayo_shodan.quick_scan(ip_input)
                    st.info(result)
                except Exception as e:
                    st.error(f"Shodan Module Error: {e}")
        else:
            st.warning("I need an IP address to scan, Boss!")

# MODULE 4: TARGET TRACKER
elif menu == "Target Tracker (OSINT)":
    st.title("📍 GLOBAL TARGET TRACKER")
    st.write("Phone number intelligence and carrier tracing.")
    phone = st.text_input("Enter Phone Number (with country code):")
    if st.button("Initialize Deep Trace"):
        if phone:
            with st.spinner("Tracking signal markers..."):
                try:
                    # Added OpenCage/BayoTrack integration check
                    result = bayo_track.track_number(phone)
                    st.write(result)
                except Exception as e:
                    st.error(f"Tracker Error: {e}")
        else:
            st.warning("Need a phone number for the trace.")

# MODULE 5: EXPLOIT LAB
elif menu == "Exploit Lab (CVE)":
    st.title("💉 EXPLOIT & VULN LAB")
    st.write("Search the global CVE database for specific vulnerabilities.")
    cve = st.text_input("Enter CVE ID (e.g., CVE-2021-44228):")
    if st.button("Fetch Exploit Intelligence"):
        if cve:
            with st.spinner("Searching exploit databases..."):
                try:
                    info = bayo_exploit.get_exploit_info(cve)
                    st.info(info)
                except Exception as e:
                    st.error(f"Exploit Lab Error: {e}")

# MODULE 6: BRUTE FORCE SIMULATOR
elif menu == "Brute Force Simulator":
    st.title("🔑 AUTHENTICATION TESTER")
    st.write("Simulate brute force resistance and password entropy.")
    if st.button("Execute Attack Simulation"):
        try:
            with st.spinner("Running entropy calculations..."):
                res = bayo_brute.run_sim()
                st.success(res)
        except Exception as e:
            st.error(f"Simulator Error: {e}")

# MODULE 7: PHISH-CHECK
elif menu == "Phish-Check (URL Analyzer)":
    st.title("🎣 PHISH-CHECK ANALYZER")
    st.write("Scan links for malicious patterns or phishing signatures.")
    url_input = st.text_input("Enter URL to analyze:")
    if st.button("Run Link Analysis"):
        if url_input:
            with st.spinner("Analyzing URL structure..."):
                if "http://" in url_input:
                    st.error("🚨 MALICIOUS: Link uses insecure HTTP. High Risk!")
                elif any(word in url_input.lower() for word in ["login", "verify", "update", "bank"]):
                    st.warning("⚠️ SUSPICIOUS: URL contains phishing keywords.")
                else:
                    st.success("✅ Link appears standard.")

# --- 9. FOOTER STATUS ---
st.sidebar.markdown("---")
st.sidebar.write("📡 Status: **ONLINE**")
st.sidebar.write("⚡ Connection: **ENCRYPTED**")
st.sidebar.write("📟 Interface: **v4.8 (SUPABASE)**")
