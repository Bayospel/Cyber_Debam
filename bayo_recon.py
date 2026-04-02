import socket
import requests

def full_recon(target):
    # Clean the target (remove http if present)
    target_clean = target.replace("http://", "").replace("https://", "").split('/')[0]
    
    report_lines = [f"RECON REPORT FOR: {target_clean}", "-"*30]
    
    # 1. IP RESOLUTION (Replaces 'dig')
    try:
        ip_addr = socket.gethostbyname(target_clean)
        report_lines.append(f"IP ADDRESS: {ip_addr}")
    except:
        report_lines.append("IP ADDRESS: Could not resolve.")

    # 2. HTTP HEADER RECON (Better than WHOIS for Cloud)
    try:
        res = requests.get(f"http://{target_clean}", timeout=5)
        server = res.headers.get('Server', 'Unknown')
        report_lines.append(f"WEB SERVER: {server}")
        report_lines.append(f"STATUS CODE: {res.status_code}")
    except:
        report_lines.append("WEB SERVER: Connection failed.")

    # 3. PORT SCAN (Socket-based - Replaces 'nmap')
    # Scanning just common ports to keep it fast and avoid cloud bans
    common_ports = [80, 443, 21, 22, 8080]
    open_ports = []
    for port in common_ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target_clean, port))
        if result == 0:
            open_ports.append(str(port))
        s.close()
    
    report_lines.append(f"OPEN PORTS: {', '.join(open_ports) if open_ports else 'None detected'}")
    
    return "\n".join(report_lines)
