import subprocess

def full_recon(target):
    print(f"[!] Starting Full Reconnaissance on: {target}")
    
    # 1. WHOIS
    print("[+] Gathering WHOIS data...")
    whois_data = subprocess.getoutput(f"whois {target} | grep -E 'Registrar:|Creation Date:|Registry Expiry Date:'")
    
    # 2. DNS DIG
    print("[+] Digging for DNS records...")
    dns_data = subprocess.getoutput(f"dig {target} +short")
    
    # 3. NMAP (Fast Scan)
    print("[+] Scanning common ports...")
    nmap_data = subprocess.getoutput(f"nmap -F {target} | grep 'open'")
    
    report = f"""
    RECON REPORT FOR: {target}
    --------------------------
    WHOIS: {whois_data if whois_data else "No public data found."}
    IP ADDRESSES: {dns_data if dns_data else "Could not resolve IP."}
    OPEN PORTS: {nmap_data if nmap_data else "No common ports open."}
    """
    return report
