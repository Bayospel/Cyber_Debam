import streamlit as st
from groq import Groq
import os, requests, subprocess, datetime

# --- IMPORT YOUR BAYOSPEL MODULES ---
import bayo_track
import bayo_recon
import bayo_reader

# --- TACTICAL UI ---
st.set_page_config(page_title="BAYOSPEL CLOUD OS", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FF41; font-family: monospace; }
    .stTextInput>div>div>input { background-color: #111; color: #00FF41; border: 1px solid #00FF41; }
    .stButton>button { background-color: #00FF41; color: black; width: 100%; border-radius: 0px; }
    </style>
    """, unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- HACKING LOGIC ---
def find_admin_pages(url):
    if not url.startswith('http'): url = 'http://' + url
    paths = ['/admin', '/login', '/wp-admin', '/admin.php', '/panel', '/dashboard']
    found_urls = []
    for path in paths:
        try:
            full_url = url.rstrip('/') + path
            r = requests.get(full_url, timeout=3)
            if r.status_code == 200: found_urls.append(full_url)
        except: continue
    return found_urls

# --- MAIN INTERFACE ---
st.title("💀 BAYOSPEL TACTICAL CLOUD")

menu = st.sidebar.radio("COMMAND CENTER", ["AI Commander", "Web Recon", "Target Tracker", "Exploit Lab"])

# --- MODULE 1: AI COMMANDER ---
if menu == "AI Commander":
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Enter Command..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Handle "Write a script" inside AI
        if "write a script" in prompt.lower() or "code this" in prompt.lower():
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Write only python code, no explanations."}, {"role": "user", "content": prompt}]
            )
            code = res.choices[0].message.content
            st.code(code, language='python')
        else:
            with st.chat_message("assistant"):
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "You are Bayospel Cloud AI. Use Naija slang. You are a pro hacker."}] + st.session_state.messages
                )
                reply = res.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

# --- MODULE 2: WEB RECON ---
elif menu == "Web Recon":
    target = st.text_input("Target URL (e.g. example.com):")
    col1, col2 = st.columns(2)
    
    if col1.button("Find Admin Pages"):
        with st.spinner("Scanning..."):
            found = find_admin_pages(target)
            if found: 
                for f in found: st.success(f"FOUND: {f}")
            else: st.error("No doors found.")

    if col2.button("Crawl Inputs"):
        try:
            r = requests.get(target if target.startswith('http') else 'http://'+target)
            if "<input" in r.text: st.warning("Found input fields! Ready for injection.")
            else: st.info("Site looks clean.")
        except: st.error("Target unreachable.")

# --- MODULE 3: TARGET TRACKER ---
elif menu == "Target Tracker":
    val = st.text_input("Enter IP or Phone Number:")
    if st.button("Deep Trace"):
        # Calling your bayo_track file
        st.info(f"Initiating Bayo_Track logic for {val}...")
        try:
            # Assuming your bayo_track has a function called track_number
            result = bayo_track.track_number(val) 
            st.write(result)
        except Exception as e:
            st.error(f"Error in bayo_track: {e}")

# --- MODULE 4: EXPLOIT LAB ---
elif menu == "Exploit Lab":
    st.warning("EXPERIMENTAL: Most tools require local installation.")
    cmd_type = st.selectbox("Action", ["Stalk (Sherlock)", "SQLMap Inject", "Payload (MSF)"])
    target_data = st.text_input("Input Data (Username/URL/LHOST):")
    
    if st.button("Execute"):
        if cmd_type == "Stalk (Sherlock)":
            st.info(f"Searching for {target_data} across social platforms...")
            # This is a simulation since Sherlock isn't on Streamlit servers
            st.write(f"Note: To run real Sherlock, please use the Termux version of Bayospel.")
        elif cmd_type == "SQLMap Inject":
            st.code(f"python3 sqlmap.py -u {target_data} --batch")
            st.info("Command generated. Streamlit Cloud blocks active SQL injections for safety.")
