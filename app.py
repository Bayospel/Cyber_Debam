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

# --- 3. PWA INSTALLATION ENGINE ---
components.html(
    """
    <script>
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function() {
        navigator.worker.register('https://raw.githubusercontent.com/Bayospel/cyber_debam/main/service-worker.js');
      });
    }
    </script>
    <link rel="manifest" href="https://raw.githack.com/Bayospel/cyber_debam/main/manifest.json?v=2">
    """,
    height=0,
)

# --- 4. GEMINI-STYLE UI CSS ---
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
    
    /* SIDEBAR STYLE */
    [data-testid="stSidebar"] {{ background-color: #0a0a0a; border-right: 1px solid #00FF41; }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {{ color: #FFFFFF !important; }}
    
    /* GEMINI-STYLE CHAT BUBBLES */
    .stChatMessage {{ 
        background-color: rgba(26, 26, 26, 0.8) !important; 
        border: 1px solid #333 !important; 
        border-radius: 15px !important; 
        margin-bottom: 15px !important; 
        padding: 15px !important; 
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }}
    
    /* User Border (Green) */
    [data-testid="stChatMessage"]:nth-child(odd) {{
        border-left: 5px solid #00FF41 !important;
    }}
    
    /* Debam Border (White/Silver) */
    [data-testid="stChatMessage"]:nth-child(even) {{
        border-left: 5px solid #FFFFFF !important;
        background-color: rgba(35, 35, 35, 0.9) !important;
    }}

    .stChatMessage p {{ color: #FFFFFF !important; font-size: 1.1rem !important; line-height: 1.6; }}
    .stChatMessage strong {{ color: #00FF41 !important; }}
    .stChatInput textarea {{ color: #00FF41 !important; }}
    
    /* BUTTONS */
    .stButton>button {{ background-color: #00FF41; color: black; font-weight: bold; width: 100%; border-radius: 8px; border: none; }}
    .stButton>button:hover {{ background-color: #00cc33; color: white; }}
</style>
""", unsafe_allow_html=True)

# --- 5. CORE LOGIC ENGINES ---
def get_groq_client():
    try:
        keys = st.secrets["GROQ_KEYS"]
        selected_key = random.choice(keys)
        return Groq(api_key=selected_key)
    except Exception:
        return None

def get_manual():
    # NAIJA SLANG UPGRADE
    return "You are DEBAM, a Tactical AI Commander built by the Big Boss Bayonle. You are a street-smart hacker from Lagos. Your talk must be rugged but professional. Use Naija slang like: Abeg, Omo, No shaking, Iyalaya won, Street ti take over, Standard, and Correct. If a user asks for a hack, tell them 'E don set' before giving info. Always respect Bayonle as the Only Boss."

# --- 6. SIDEBAR SYSTEM ---
st.sidebar.image(logo_data.LOGO_BASE64, use_container_width=True)
st.sidebar.title("💀 DEBAM OS v4.1")
st.sidebar.markdown(f"<span style='color:#00FF41'>Commander:</span> <span style='color:white'>Bayonle</span>", unsafe_allow_html=True)

menu = st.sidebar.radio("SQUAD SELECTION", [
    "AI Commander", 
    "Web Recon (Scanner)", 
    "Network Eye (Shodan)", 
    "Target Tracker (OSINT)", 
    "Exploit Lab (CVE)", 
    "Brute Force Simulator",
    "Phish-Check (URL Analyer)" # NEW TOOL
])

st.sidebar.markdown("---")
st.sidebar.subheader("📱 MOBILE INSTALL")
if st.sidebar.button("Install Tactical App"):
    st.sidebar.info("Tap the browser menu (3 dots) and select 'Add to Home Screen' to lock in the Skull logo.")

# --- 7. FUNCTIONAL MODULES ---

# MODULE 1: AI COMMANDER (GEMINI STYLE)
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
    target = st.text_input("Enter Target URL:")
    if st.button("Start Scan"):
        if target:
            with st.spinner("Analyzing..."):
                st.code(bayo_recon.full_recon(target))

# MODULE 3: NETWORK EYE (SHODAN)
elif menu == "Network Eye (Shodan)":
    st.title("👁️ NETWORK EYE: IP ENRICHMENT")
    ip_input = st.text_input("Enter Target IP Address:")
    if st.button("Run Instant Scan"):
        if ip_input:
            st.info(bayo_shodan.quick_scan(ip_input))

# MODULE 4: TARGET TRACKER
elif menu == "Target Tracker (OSINT)":
    st.title("📍 GLOBAL TARGET TRACKER")
    phone = st.text_input("Enter Phone Number:")
    if st.button("Deep Trace"):
        st.write(bayo_track.track_number(phone) if phone else "Need a number.")

# MODULE 5: EXPLOIT LAB
elif menu == "Exploit Lab (CVE)":
    st.title("💉 EXPLOIT & VULN LAB")
    cve = st.text_input("Enter CVE ID:")
    if st.button("Fetch Data"):
        st.info(bayo_exploit.get_exploit_info(cve))

# MODULE 6: BRUTE FORCE
elif menu == "Brute Force Simulator":
    st.title("🔑 AUTHENTICATION TESTER")
    if st.button("Start Simulation"):
        st.success(bayo_brute.run_sim())

# MODULE 7: PHISH-CHECK (NEW TOOL)
elif menu == "Phish-Check (URL Analyer)":
    st.title("🎣 PHISH-CHECK ANALYZER")
    st.write("Scan URLs for suspicious patterns or phishing characteristics.")
    url_input = st.text_input("Enter URL to analyze:")
    if st.button("Analyze Link"):
        if url_input:
            with st.spinner("Checking for malicious signatures..."):
                # Simulation of logic (You can expand this in a new bayo_phish.py later)
                suspicious_keywords = ["login", "verify", "update", "bank", "secure", "signin"]
                is_sus = any(word in url_input.lower() for word in suspicious_keywords)
                if "https" not in url_input:
                    st.error("🚨 DANGER: Link is not secure (HTTP). High Phishing risk!")
                elif is_sus:
                    st.warning("⚠️ CAUTION: URL contains suspicious keywords (e.g., 'login'). Verify source.")
                else:
                    st.success("✅ Link looks standard. Proceed with caution.")
        else:
            st.warning("Commander, drop the link first!")

st.sidebar.markdown("---")
st.sidebar.write("📡 Status: **ONLINE**")
st.sidebar.write("⚡ Connection: **ENCRYPTED**")
