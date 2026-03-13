from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from googlesearch import search

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

@app.route('/')
def website():
    return render_template('index.html')

@app.route('/live')
def live_matches():
    try:
        link = "https://www.cricbuzz.com/cricket-match/live-scores"
        # timeout વધાર્યો છે અને headers વાપર્યા છે
        r = requests.get(link, headers=HEADERS, timeout=15)
        
        if r.status_code != 200:
            return jsonify({"error": f"Cricbuzz server status: {r.status_code}"})

        # જો Cricbuzz બ્લોક કરે તો પેજમાં 'captcha' કે 'bot' શબ્દ હશે
        if "captcha" in r.text.lower() or "bot" in r.text.lower():
            return jsonify(["Security Check: Cricbuzz is blocking the request. Please try after some time."])

        page = BeautifulSoup(r.text, "html.parser")
        live_list = []

        # મેચ કાર્ડ્સ શોધવા માટે અલગ-અલગ ક્લાસ ટ્રાય કરવા
        # રીત ૧: લેટેસ્ટ ક્લાસ
        matches = page.find_all("div", class_="cb-mtch-lst")
        
        # રીત ૨: જો રીત ૧ ફેલ જાય તો
        if not matches:
            matches = page.find_all("div", class_="cb-scr-wll-chvrn")
            
        # રીત ૩: તમારો ઓરિજિનલ ક્લાસ
        if not matches:
            matches = page.find_all("div", class_="cb-lv-scrs-col")

        for m in matches:
            # get_text(separator=" ") વાપરવાથી સ્કોર અને ટીમનું નામ સ્પષ્ટ વંચાશે
            data = m.get_text(separator=" ").strip()
            if data:
                # બિનજરૂરી સ્પેસ દૂર કરવી
                clean_data = " ".join(data.split())
                live_list.append(clean_data)
        
        if not live_list:
            return jsonify(["No live matches found at the moment."])
            
        return jsonify(live_list)
        
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/schedule')
def schedule():
    try:
        link = "https://www.cricbuzz.com/cricket-schedule/upcoming-series/international"
        r = requests.get(link, headers=HEADERS, timeout=10)
        page = BeautifulSoup(r.text, "html.parser")
        
        match_containers = page.find_all("div", class_="cb-lv-grn-strip")
        matches = []
        for date_div in match_containers:
            match_info = date_div.find_next_sibling("div")
            if date_div and match_info:
                matches.append(f"{date_div.text.strip()} - {match_info.text.strip()}")
        return jsonify(matches)
    except Exception as e:
        return jsonify({"error": str(e)})

# બાકીનો Player search વાળો કોડ અહીં નીચે આવશે...

if __name__ == "__main__":
    app.run()

