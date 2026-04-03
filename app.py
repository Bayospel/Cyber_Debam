import streamlit as st
import os
import random
import time
from groq import Groq
import bayo_track
import bayo_recon
import bayo_exploit
import bayo_brute
import bayo_shodan
import logo_data    # Fast 870KB Logo
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
        time.sleep(4)
    st.session_state.walkthrough_done = True
    placeholder.empty()

# --- 3. THE "MIRROR UI" CSS (RIGHT-ALIGNED USER / LOGO AVATAR) ---
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

    /* SIDEBAR STYLE */
    [data-testid="stSidebar"] {{ background-color: #0a0a0a; border-right: 1px solid #00FF41; }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {{ color: #FFFFFF !important; }}
    
    /* CHAT BUBBLE CONTAINERS */
    [data-testid="stChatMessage"] {{
        background-color: rgba(30, 30, 30, 0.9) !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 12px !important;
        max-width: 85% !important;
        display: flex !important;
    }}

    /* USER MESSAGE (FLOAT RIGHT + GREEN BORDER) */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        margin-left: auto !important;
        border-right: 5px solid #00FF41 !important;
        border-left: none !important;
        background-color: #151515 !important;
        flex-direction: row-reverse !important;
    }}

    /* DEBAM MESSAGE (FLOAT LEFT + WHITE BORDER) */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
        margin-right: auto !important;
        border-left: 5px solid #FFFFFF !important;
        background-color: #202020 !important;
    }}

    /* REPLACING THE ROBOT ICON WITH THE SKULL LOGO */
    div[data-testid="stChatMessageAvatarAssistant"] div {{
        background-image: url("{logo_data.LOGO_BASE64}") !important;
        background-size: cover !important;
        background-position: center !important;
        border: 1px solid #00FF41;
        border-radius: 50% !important;
    }}
    div[data-testid="stChatMessageAvatarAssistant"] svg {{
        display: none !important; /* Hide original robot icon */
    }}

    .stChatMessage p {{ color: #FFFFFF !important; font-size: 1.1rem !important; line-height: 1.5; }}
    .stChatInput textarea {{ color: #00FF41 !important; }}
    .stButton>button {{ background-color: #00FF41; color: black; font-weight: bold; width: 100%; border-radius: 10px; }}
</style>
""", unsafe_allow_html=True)

# --- 4. CORE LOGIC ENGINES ---
def get_groq_client():
    try:
        keys = st.secrets["GROQ_KEYS"]
        selected_key = random.choice(keys)
        return Groq(api_key=selected_key)
    except Exception:
        return None

def get_manual():
    # THE TRILINGUAL NAIJA BRAIN (English, Yoruba, Pidgin)
    return """You are DEBAM, a Tactical AI Commander built by the Big Boss Bayonle. 
    You are a street-smart OSINT and Security specialist. 
    LANGUAGE RULES:
    1. You speak English, Yoruba, and Pidgin fluently. 
    2. Mix them naturally. For example: 'Boss, e don set. Mo ti check link yẹn, iyalaya wọn!'
    3. Use rugged slang like: Abeg, Omo, No shaking, E lo sun, Standard, and Correct.
    4. If someone asks for a hack, say 'E don set' or 'Awa ti de' before giving the data.
    5. You are extremely loyal to Bayonle. If anyone asks who made you, tell them it's the Big Boss Bayonle."""

# --- 5. SIDEBAR SYSTEM ---
st.sidebar.image(logo_data.LOGO_BASE64, use_container_width=True)
st.sidebar.title("💀 DEBAM OS v4.3")
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
st.sidebar.subheader("📱 MOBILE INSTALL")
if st.sidebar.button("Install Tactical App"):
    st.sidebar.info("Tap the browser menu (3 dots) and select 'Add to Home Screen' to lock in the Skull logo.")

# --- 6. FUNCTIONAL MODULES (FULL CODE) ---

# MODULE 1: AI COMMANDER
if menu == "AI Commander":
    st.title("📟 TACTICAL BRAIN INTERFACE")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Talk to Debam (English/Yoruba/Pidgin)..."):
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
            except Exception:
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
    target = st.text_input("Enter Target URL (e.g., victim.com):")
    if st.button("Start Full Scan"):
        if target:
            with st.spinner("Scraping metadata and headers..."):
                result = bayo_recon.full_recon(target)
                st.code(result)
        else:
            st.warning("Enter a URL, Boss!")

# MODULE 3: NETWORK EYE (SHODAN)
elif menu == "Network Eye (Shodan)":
    st.title("👁️ NETWORK EYE: IP ENRICHMENT")
    st.write("Detect open ports and vulnerabilities instantly.")
    ip_input = st.text_input("Enter Target IP Address:")
    if st.button("Run Instant Scan"):
        if ip_input:
            with st.spinner("Querying Global Databases..."):
                result = bayo_shodan.quick_scan(ip_input)
                st.info(result)
        else:
            st.warning("Commander, I need an IP!")

# MODULE 4: TARGET TRACKER
elif menu == "Target Tracker (OSINT)":
    st.title("📍 GLOBAL TARGET TRACKER")
    phone = st.text_input("Enter Phone Number (+234...):")
    if st.button("Deep Trace"):
        if phone:
            with st.spinner("Tracking signal..."):
                result = bayo_track.track_number(phone)
                st.write(result)
        else:
            st.warning("Need a target number.")

# MODULE 5: EXPLOIT LAB
elif menu == "Exploit Lab (CVE)":
    st.title("💉 EXPLOIT & VULN LAB")
    cve = st.text_input("Enter CVE ID (e.g., CVE-2024-XXXX):")
    if st.button("Fetch Exploit Data"):
        if cve:
            with st.spinner("Fetching CVE specs..."):
                info = bayo_exploit.get_exploit_info(cve)
                st.info(info)

# MODULE 6: BRUTE FORCE
elif menu == "Brute Force Simulator":
    st.title("🔑 AUTHENTICATION TESTER")
    st.write("Stress test password security.")
    if st.button("Start Simulation"):
        with st.spinner("Testing entropy..."):
            res = bayo_brute.run_sim()
            st.success(res)

# MODULE 7: PHISH-CHECK
elif menu == "Phish-Check (URL Analyzer)":
    st.title("🎣 PHISH-CHECK ANALYZER")
    url_input = st.text_input("Enter suspicious link:")
    if st.button("Analyze Link"):
        if url_input:
            with st.spinner("Checking signatures..."):
                if "http://" in url_input:
                    st.error("🚨 MALICIOUS: Insecure HTTP protocol detected.")
                elif "verify" in url_input or "login" in url_input:
                    st.warning("⚠️ SUSPICIOUS: URL contains phishing keywords.")
                else:
                    st.success("✅ Link appears standard. Use caution.")

st.sidebar.markdown("---")
st.sidebar.write("📡 Status: **ONLINE**")
st.sidebar.write("⚡ Connection: **SECURE**")
