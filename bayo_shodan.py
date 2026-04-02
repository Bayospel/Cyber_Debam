import requests

def quick_scan(ip):
    """Fetches open ports and vulnerabilities for an IP using Shodan InternetDB."""
    try:
        url = f"https://internetdb.shodan.io/{ip}"
        response = requests.get(url, timeout=5)
        
        if response.status_status == 404:
            return "❌ No data found for this IP in the Shodan database."
        
        data = response.json()
        
        # Formatting the output
        report = f"🌐 **IP:** {data.get('ip', 'N/A')}\n"
        report += f"📁 **Hostnames:** {', '.join(data.get('hostnames', ['None']))}\n"
        report += f"🔌 **Open Ports:** {', '.join(map(str, data.get('ports', [])))}\n"
        
        vulns = data.get('vulns', [])
        if vulns:
            report += f"⚠️ **Detected Vulnerabilities:** {', '.join(vulns[:10])} (showing top 10)"
        else:
            report += "✅ **No known vulnerabilities found.**"
            
        return report
    except Exception as e:
        return f"⚠️ Scan Error: {str(e)}"
