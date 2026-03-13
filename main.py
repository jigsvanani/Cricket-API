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
        # NDTV Sports જલ્દી બ્લોક નથી કરતું
        link = "https://sports.ndtv.com/cricket/live-scores"
        r = requests.get(link, headers=HEADERS, timeout=15)
        
        page = BeautifulSoup(r.text, "html.parser")
        live_list = []

        # NDTV ના લાઈવ સ્કોર કાર્ડ્સ શોધવા માટે
        matches = page.find_all("div", class_="sp-scr_cd")
        
        for m in matches:
            # ટીમ અને સ્કોરની માહિતી ભેગી કરવી
            data = m.get_text(separator=" ").strip()
            if data:
                # વધારાની સ્પેસ દૂર કરવી
                clean_data = " ".join(data.split())
                live_list.append(clean_data)
        
        if not live_list:
            return jsonify(["No live matches found on NDTV at the moment."])
            
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


