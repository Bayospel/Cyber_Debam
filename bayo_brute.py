import requests
from bs4 import BeautifulSoup
import os

def find_form_parameters(url):
    try:
        if not url.startswith('http'): url = 'http://' + url
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Look for the login form
        form = soup.find('form')
        if not form: return None, None
        
        inputs = form.find_all('input')
        user_field = None
        pass_field = None
        
        for i in inputs:
            name = i.get('name', '').lower()
            itype = i.get('type', '').lower()
            # Identifying the target fields
            if any(x in name for x in ['user', 'email', 'login']) or itype == 'text':
                user_field = i.get('name')
            if any(x in name for x in ['pass', 'pwd']) or itype == 'password':
                pass_field = i.get('name')
        
        return user_field, pass_field
    except Exception as e:
        return None, None

def analyze_target(target):
    u_field, p_field = find_form_parameters(target)
    
    if not u_field or not p_field:
        return "[-] No valid login form detected on this target."

    report = f"""
[ BAYOSPEL BRUTE-FORCE ANALYSIS ]
----------------------------------
TARGET: {target}
DETECTED USER FIELD: {u_field}
DETECTED PASS FIELD: {p_field}

STRATEGY: 
To test this site, a security professional would use a tool like Hydra 
with the following parameters:
-L admin -P [wordlist] http-post-form "/login: {u_field}=^USER^&{p_field}=^PASS^:F=Login failed"

STATUS: ANALYZED (Attack simulation restricted on Cloud server)
----------------------------------
    """
    return report
