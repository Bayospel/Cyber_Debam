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
    /* Main App Background */
    .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #00FF41; }
    
    /* FIX: Force Chat Message Text to be WHITE and Readable */
    .stChatMessage { background-color: #1a1a1a !important; border: 1px solid #333; margin-bottom: 10px; border-radius: 10px; }
    .stChatMessage p { color: #FFFFFF !important; font-size: 1.1rem; font-weight: 500; }
    
    /* Input Boxes */
    .stTextInput>div>div>input { background-color: #111; color: #00FF41; border: 1px solid #00FF41; }
    
    /* Buttons */
    .stButton>button { background-color: #00FF41; color: black; font-weight: bold; width: 100%; border-radius: 5px; }
    .stButton>button:hover { background-color: #008F11; color: white; }

    /* Titles */
    h1, h2, h3 { color: #00FF41 !important; }
</style>
""", unsafe_allow_html=True)

# --- CORE ENGINE ---
# This pulls the key you saved in Streamlit Settings > Secrets
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
    </style>
    """, unsafe_allow_html=True)


client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- SIDEBAR COMMAND CENTER ---
st.sidebar.title("💀 BAYOSPEL OS v4.0")
menu = st.sidebar.radio("SQUAD SELECTION", [
    "AI Commander", 
    "Web Recon (Scannest.markdown("""
    <style>
    /* Main App Background */
    .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
    
    /* Input Boxes */
    .stTextInput>div>div>input { background-color: #111; color: #00FF41; border: 1px solid #00FF41; }
    
    /* Buttons */
    .stButton>button { background-color: #00FF41; color: black; font-weight: bold; border-radius: 0px; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #00FF41; }

    /* FIX: Force Chat Message Text Visibility */
    .stChatMessage { background-color: #1a1a1a !important; border: 1px solid #333; margin-bottom: 10px; border-radius: 10px; }
    .stChatMessage p { color: #FFFFFF !important; font-size: 1.1rem; }
    
    /* Chat Input Bar at bottom */
    .stChatInputContainer { background-color: #050505 !important; }
    </style>
    """, unsafe_allow_html=True)
r)", 
    "Target Tracker (OSINT)", 
    "Exploit Lab (CVE)", 
    "Brute Analyzer (Sniffer)"
])

# --- 1. AI COMMANDER (Integrated with Brain) ---
if menu == "AI Commander":
    st.title("📟 TACTICAL BRAIN INTERFACE")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Commander, awaiting orders..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Pull private context from bayo_reader
        brain_data = bayo_reader.get_context_prompt()

        with st.chat_message("assistant"):
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"You are Bayospel Cloud AI. Use Naija slang. {brain_data}"}
                ] + st.session_state.messages
            )
            reply = res.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

# --- 2. WEB RECON (bayo_recon) ---
elif menu == "Web Recon (Scanner)":
    st.title("📡 GLOBAL RECONNAISSANCE")
    target = st.text_input("Enter Target URL:")
    if st.button("Initialize Full Recon"):
        if target:
            with st.spinner("Probing target..."):
                report = bayo_recon.full_recon(target)
                st.code(report)
        else: st.error("Target missing, Boss.")

# --- 3. TARGET TRACKER (bayo_track) ---
elif menu == "Target Tracker (OSINT)":
    st.title("📍 GEOSPATIAL TRACKING")
    val = st.text_input("Enter Number (+234...) or IP:")
    if st.button("Deep Trace"):
        with st.spinner("Scanning satellite data..."):
            success, report, lat, lng = bayo_track.track_number(val)
            if success:
                st.success("Target Pinpointed!")
                st.markdown(report)
                if lat != 0:
                    st.map(data={"lat": [lat], "lon": [lng]})
            else:
                st.error(report)

# --- 4. EXPLOIT LAB (bayo_exploit) ---
elif menu == "Exploit Lab (CVE)":
    st.title("🔬 VULNERABILITY RESEARCH")
    query = st.text_input("Software/Service Name (e.g. Apache):")
    if st.button("Fetch NIST CVEs"):
        with st.spinner("Querying NIST Database..."):
            results = bayo_exploit.search_cve(query)
            st.markdown(results)

# --- 5. BRUTE ANALYZER (bayo_brute) ---
elif menu == "Brute Analyzer (Sniffer)":
    st.title("💀 FORM SNIFFER & ANALYZER")
    login_url = st.text_input("Enter Login Page URL:")
    if st.button("Sniff Form Parameters"):
        with st.spinner("Analyzing HTML structure..."):
            analysis = bayo_brute.analyze_target(login_url)
            st.code(analysis)

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
