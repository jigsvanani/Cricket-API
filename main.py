from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# સૌથી શક્તિશાળી Headers (જે બ્રાઉઝર જેવું જ વર્તન કરશે)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

@app.route('/')
def website():
    return render_template('index.html')

@app.route('/live')
def live_matches():
    try:
        # સ્ત્રોત: ESPN Cricinfo (આ સૌથી વધુ સ્ટેબલ છે)
        link = "https://www.espncricinfo.com/live-cricket-score"
        r = requests.get(link, headers=HEADERS, timeout=15)
        
        # જો સર્વર બ્લોક કરે તો તે અહીં દેખાશે
        if r.status_code != 200:
            return jsonify([f"Error: Server returned status {r.status_code}. The site might be blocking Vercel."])

        page = BeautifulSoup(r.text, "html.parser")
        live_list = []

        # ESPN Cricinfo ના લાઈવ કાર્ડ્સ શોધવા (નવા Tags મુજબ)
        # આ Tags બદલાતા રહે છે, એટલે મેં ૩ અલગ અલગ રીત વાપરી છે
        matches = page.find_all("div", class_="ds-flex ds-flex-col ds-mt-2 ds-mb-2")
        
        if not matches:
            matches = page.find_all("div", class_="ds-p-0")

        for m in matches:
            text = m.get_text(separator=" ").strip()
            if text and len(text) > 10: # બહુ ટૂંકો ડેટા ના લેવો
                clean_data = " ".join(text.split())
                live_list.append(clean_data)
        
        if not live_list:
            return jsonify(["No live matches found or Scraper needs update."])
            
        return jsonify(live_list)
        
    except Exception as e:
        return jsonify([f"System Error: {str(e)}"])

@app.route('/schedule')
def schedule():
    try:
        # NDTV પર પાછા જઈએ કારણ કે તેનું શેડ્યૂલ સરળ છે
        link = "https://sports.ndtv.com/cricket/schedules-fixtures"
        r = requests.get(link, headers=HEADERS, timeout=15)
        page = BeautifulSoup(r.text, "html.parser")
        
        schedule_list = []
        containers = page.find_all("div", class_="sp-scr_cd")
        
        for item in containers:
            data = item.get_text(separator=" ").strip()
            if data:
                schedule_list.append(" ".join(data.split()))

        return jsonify(schedule_list if schedule_list else ["Schedule not found."])
    except Exception as e:
        return jsonify([f"Schedule Error: {str(e)}"])

if __name__ == "__main__":
    app.run()
