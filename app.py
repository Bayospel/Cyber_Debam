import streamlit as st
import os
from groq import Groq
import bayo_track
import bayo_recon
import bayo_exploit
import bayo_brute

# --- TACTICAL UI SETUP ---
st.set_page_config(page_title="BAYOSPEL GLOBAL OS", layout="wide")

# THE ULTIMATE VISIBILITY FIX
st.markdown("""
<style>
    /* Main Background */
    .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
    
    /* Sidebar Text Visibility */
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #00FF41; }
    [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { 
        color: #FFFFFF !important; 
    }
    [data-testid="stSidebar"] .st-emotion-cache-167880x { color: #00FF41 !important; }

    /* CHAT BUBBLE FIX */
    .stChatMessage { background-color: #1a1a1a !important; border: 1px solid #333; border-radius: 10px; padding: 10px; }
    .stChatMessage p, .stChatMessage li, .stChatMessage span { 
        color: #FFFFFF !important; 
        font-size: 1.1rem !important;
    }
    .stChatMessage strong { color: #00FF41 !important; }

    /* Input Box Placeholder & Text */
    .stChatInput textarea { color: #00FF41 !important; }
    
    /* Buttons */
    .stButton>button { background-color: #00FF41; color: black; font-weight: bold; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- CORE ENGINE ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_manual():
    try:
        with open("brain/manual.txt", "r") as f:
            return f.read()
    except:
        return "You are Debam (Bayospel), a tactical AI created by Bayonle. Use Naija slang."

# --- SIDEBAR ---
st.sidebar.title("💀 BAYOSPEL OS v4.0")
st.sidebar.markdown(f"<span style='color:#00FF41'>Commander:</span> <span style='color:white'>Bayonle</span>", unsafe_allow_html=True)
menu = st.sidebar.radio("SQUAD SELECTION", ["AI Commander", "Web Recon (Scanner)", "Target Tracker (OSINT)", "Exploit Lab (CVE)", "Brute Force Simulator"])

# --- MODULE 1: AI COMMANDER ---
if menu == "AI Commander":
    st.title("📟 TACTICAL BRAIN INTERFACE")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # CHANGED PLACEHOLDER TEXT HERE
    if prompt := st.chat_input("Debam is awaiting your order..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": get_manual()}] + st.session_state.messages
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- MODULE 2: RECON ---
elif menu == "Web Recon (Scanner)":
    st.title("🌐 WEB RECONNAISSANCE")
    target = st.text_input("Enter Target URL:")
    if st.button("Start Scan"):
        st.code(bayo_recon.full_recon(target) if target else "Need a target, Boss.")

# --- MODULE 3: TRACKER ---
elif menu == "Target Tracker (OSINT)":
    st.title("📍 GLOBAL TARGET TRACKER")
    phone = st.text_input("Enter Phone Number:")
    if st.button("Deep Trace"):
        st.write(bayo_track.track_number(phone) if phone else "Need a number.")

# --- MODULE 4: EXPLOIT ---
elif menu == "Exploit Lab (CVE)":
    st.title("💉 EXPLOIT & VULN LAB")
    cve = st.text_input("Enter CVE ID:")
    if st.button("Fetch Data"):
        st.info(bayo_exploit.get_exploit_info(cve))

# --- MODULE 5: BRUTE FORCE ---
elif menu == "Brute Force Simulator":
    st.title("🔑 AUTHENTICATION TESTER")
    if st.button("Start Sim"):
        # Fixed the function call to prevent AttributeError
        try:
            result = bayo_brute.run_sim()
            st.success(result)
        except Exception as e:
            st.error(f"Module Error: {e}")

st.sidebar.markdown("---")
st.sidebar.write("📡 Status: **ONLINE**")
