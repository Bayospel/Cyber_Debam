import streamlit as st
import os
import random
import time
from groq import Groq
import bayo_track
import bayo_recon
import bayo_exploit
import bayo_brute
import bayo_shodan  # Ensure bayo_shodan.py is in your repo
import logo_data    # This loads your 870KB logo instantly from your new file
import streamlit.components.v1 as components

# --- 1. TACTICAL UI SETUP ---
st.set_page_config(page_title="BAYOSPEL GLOBAL OS", layout="wide")

# --- 2. INSTANT WELCOME SPLASH SCREEN ---
if "walkthrough_done" not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(
            f"""
            <style>
                .welcome-container {{
                    background-color: #050505;
                    height: 100vh;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    z-index: 9999;
                }}
                .welcome-text {{
                    color: #00FF41;
                    font-family: 'Courier New', monospace;
                    font-size: 26px;
                    margin-top: 20px;
                    font-weight: bold;
                    text-transform: uppercase;
                    letter-spacing: 3px;
                }}
                .boss-text {{
                    color: white;
                    font-family: 'Courier New', monospace;
                    font-size: 16px;
                    margin-top: 10px;
                    letter-spacing: 5px;
                    opacity: 0.8;
                }}
                .glow-img {{
                    border-radius: 50%;
                    box-shadow: 0 0 30px #00FF41;
                    animation: pulse 2s infinite;
                }}
                @keyframes pulse {{
                    0% {{ transform: scale(1); opacity: 0.8; }}
                    50% {{ transform: scale(1.05); opacity: 1; }}
                    100% {{ transform: scale(1); opacity: 0.8; }}
                }}
            </style>
            <div class="welcome-container">
                <img src="{logo_data.LOGO_BASE64}" width="250" class="glow-img">
                <div class="welcome-text">WELCOME TO DEBAM AI</div>
                <div class="boss-text">CREATED BY THE BIG BOSS BAYONLE</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(4) # Splash stays for 4 seconds
    st.session_state.walkthrough_done = True
    placeholder.empty()

# --- 3. PWA INSTALLATION ENGINE ---
components.html(
    """
    <script>
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function() {
        navigator.serviceWorker.register('https://raw.githubusercontent.com/Bayospel/cyber_debam/main/service-worker.js');
      });
    }
    </script>
    <link rel="manifest" href="https://raw.githack.com/Bayospel/cyber_debam/main/manifest.json?v=2">
    """,
    height=0,
)

# --- 4. THE ULTIMATE VISIBILITY FIX (CSS + BACKGROUND) ---
st.markdown(f"""
<style>
    .stApp {{ 
        background-color: #050505; 
        color: #00FF41; 
        font-family: 'Courier New', monospace; 
        background-image: linear-gradient(rgba(5, 5, 5, 0.92), rgba(5, 5, 5, 0.92)), url("{logo_data.LOGO_BASE64}");
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        background-size: 45%;
    }}
    [data-testid="stSidebar"] {{ background-color: #0a0a0a; border-right: 1px solid #00FF41; }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {{ color: #FFFFFF !important; }}
    .stChatMessage {{ background-color: #1a1a1a !important; border: 1px solid #333; border-radius: 10px; padding: 10px; opacity: 0.95; }}
    .stChatMessage p, .stChatMessage li, .stChatMessage span {{ color: #FFFFFF !important; font-size: 1.1rem !important; }}
    .stChatMessage strong {{ color: #00FF41 !important; }}
    .stChatInput textarea {{ color: #00FF41 !important; }}
    .stButton>button {{ background-color: #00FF41; color: black; font-weight: bold; width: 100%; border: none; }}
    .stButton>button:hover {{ background-color: #00cc33; color: white; }}
</style>
""", unsafe_allow_html=True)

# --- 5. CORE LOGIC ENGINES ---
def get_groq_client():
    try:
        keys = st.secrets["GROQ_KEYS"]
        selected_key = random.choice(keys)
        return Groq(api_key=selected_key)
    except Exception as e:
        st.error("Secrets Error: Check your GROQ_KEYS list!")
        return None

def get_manual():
    try:
        with open("brain/manual.txt", "r") as f:
            return f.read()
    except:
        return "You are Debam (Bayospel), a tactical AI created by Bayonle. Use Naija slang."

# --- 6. SIDEBAR SYSTEM ---
st.sidebar.image(logo_data.LOGO_BASE64, use_container_width=True)
st.sidebar.title("💀 DEBAM OS v4.0")
st.sidebar.markdown(f"<span style='color:#00FF41'>Commander:</span> <span style='color:white'>Bayonle</span>", unsafe_allow_html=True)

menu = st.sidebar.radio("SQUAD SELECTION", [
    "AI Commander", 
    "Web Recon (Scanner)", 
    "Network Eye (Shodan)", 
    "Target Tracker (OSINT)", 
    "Exploit Lab (CVE)", 
    "Brute Force Simulator"
])

st.sidebar.markdown("---")
st.sidebar.subheader("📱 MOBILE INSTALL")
if st.sidebar.button("Install Tactical App"):
    st.sidebar.info("Tap the browser menu (3 dots) and select 'Add to Home Screen' to lock in the Skull logo.")

# --- 7. FUNCTIONAL MODULES ---

# MODULE 1: AI COMMANDER
if menu == "AI Commander":
    st.title("📟 TACTICAL BRAIN INTERFACE")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Debam is awaiting your order..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            client = get_groq_client()
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": get_manual()}] + st.session_state.messages
                )
                full_response = response.choices[0].message.content
            except Exception:
                # Key Rotation Failover
                client = get_groq_client()
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": get_manual()}] + st.session_state.messages
                )
                full_response = response.choices[0].message.content

            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# MODULE 2: WEB RECON
elif menu == "Web Recon (Scanner)":
    st.title("🌐 WEB RECONNAISSANCE")
    target = st.text_input("Enter Target URL (e.g., example.com):")
    if st.button("Start Scan"):
        if target:
            with st.spinner("Analyzing target..."):
                result = bayo_recon.full_recon(target)
                st.code(result)
        else:
            st.warning("Need a target, Boss.")

# MODULE 3: NETWORK EYE (SHODAN)
elif menu == "Network Eye (Shodan)":
    st.title("👁️ NETWORK EYE: IP ENRICHMENT")
    st.write("Detect open ports and vulnerabilities instantly via Shodan.")
    ip_input = st.text_input("Enter Target IP Address:")
    if st.button("Run Instant Scan"):
        if ip_input:
            with st.spinner("Querying Shodan Global Database..."):
                result = bayo_shodan.quick_scan(ip_input)
                st.info(result)
        else:
            st.warning("Commander, I need an IP address to scan!")

# MODULE 4: TARGET TRACKER
elif menu == "Target Tracker (OSINT)":
    st.title("📍 GLOBAL TARGET TRACKER")
    phone = st.text_input("Enter Phone Number (with country code):")
    if st.button("Deep Trace"):
        if phone:
            with st.spinner("Tracking signal..."):
                result = bayo_track.track_number(phone)
                st.write(result)
        else:
            st.warning("Need a number, Boss.")

# MODULE 5: EXPLOIT LAB
elif menu == "Exploit Lab (CVE)":
    st.title("💉 EXPLOIT & VULN LAB")
    cve = st.text_input("Enter CVE ID (e.g., CVE-2021-44228):")
    if st.button("Fetch Data"):
        if cve:
            with st.spinner("Searching vulnerability database..."):
                info = bayo_exploit.get_exploit_info(cve)
                st.info(info)
        else:
            st.warning("Please enter a CVE ID.")

# MODULE 6: BRUTE FORCE
elif menu == "Brute Force Simulator":
    st.title("🔑 AUTHENTICATION TESTER")
    st.write("Testing password strength and brute force resilience.")
    if st.button("Start Simulation"):
        try:
            with st.spinner("Running simulation..."):
                res = bayo_brute.run_sim()
                st.success(res)
        except Exception as e:
            st.error(f"Module Error: {e}")

# --- 8. FOOTER STATUS ---
st.sidebar.markdown("---")
st.sidebar.write("📡 Status: **ONLINE**")
st.sidebar.write("⚡ Connection: **ENCRYPTED**")
