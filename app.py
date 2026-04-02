import streamlit as st
import os
from groq import Groq
import bayo_track
import bayo_recon
import bayo_exploit
import bayo_brute

# --- TACTICAL UI SETUP ---
st.set_page_config(page_title="BAYOSPEL GLOBAL OS", layout="wide")

# CUSTOM CSS FOR HACKER THEME & TEXT VISIBILITY
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #00FF41; }
    .stChatMessage { background-color: #1a1a1a !important; border: 1px solid #333; margin-bottom: 10px; border-radius: 10px; }
    .stChatMessage p { color: #FFFFFF !important; font-size: 1.1rem; font-weight: 500; }
    .stTextInput>div>div>input { background-color: #111; color: #00FF41; border: 1px solid #00FF41; }
    .stButton>button { background-color: #00FF41; color: black; font-weight: bold; width: 100%; border-radius: 5px; }
    .stButton>button:hover { background-color: #008F11; color: white; }
    h1, h2, h3 { color: #00FF41 !important; }
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

# --- SIDEBAR COMMAND CENTER ---
st.sidebar.title("💀 BAYOSPEL OS v4.0")
st.sidebar.write("Commander: **Bayonle**")
menu = st.sidebar.radio("SQUAD SELECTION", [
    "AI Commander", 
    "Web Recon (Scanner)", 
    "Target Tracker (OSINT)", 
    "Exploit Lab (CVE)", 
    "Brute Force Simulator"
])

# --- MODULE 1: AI COMMANDER (DEBAM) ---
if menu == "AI Commander":
    st.title("📟 TACTICAL BRAIN INTERFACE")
    st.subheader("System Name: Debam")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("Commander, awaiting orders..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            manual_context = get_manual()
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": manual_context}] + st.session_state.messages
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- MODULE 2: WEB RECON ---
elif menu == "Web Recon (Scanner)":
    st.title("🌐 WEB RECONNAISSANCE")
    target_url = st.text_input("Enter Target URL (e.g., google.com):")
    if st.button("Start Deep Scan"):
        if target_url:
            with st.spinner("Scanning infrastructure..."):
                results = bayo_recon.full_recon(target_url)
                st.code(results)
        else:
            st.warning("Input a target, Boss!")

# --- MODULE 3: TARGET TRACKER ---
elif menu == "Target Tracker (OSINT)":
    st.title("📍 GLOBAL TARGET TRACKER")
    phone = st.text_input("Enter Phone Number (with +country code):")
    if st.button("Deep Trace"):
        if phone:
            with st.spinner("Pinging satellites..."):
                report = bayo_track.track_number(phone)
                st.write(report)
        else:
            st.warning("Provide a number for the trace.")

# --- MODULE 4: EXPLOIT LAB ---
elif menu == "Exploit Lab (CVE)":
    st.title("💉 EXPLOIT & VULN LAB")
    cve_id = st.text_input("Enter CVE ID or Service (e.g., Apache):")
    if st.button("Fetch Exploit Data"):
        with st.spinner("Searching database..."):
            data = bayo_exploit.get_exploit_info(cve_id)
            st.info(data)

# --- MODULE 5: BRUTE FORCE SIM ---
elif menu == "Brute Force Simulator":
    st.title("🔑 AUTHENTICATION TESTER")
    st.write("Simulating local security audit...")
    if st.button("Start Sim"):
        result = bayo_brute.run_sim()
        st.success(result)

st.sidebar.markdown("---")
st.sidebar.write("📡 Status: **ONLINE**")
