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
        r = requests.get(link, headers=HEADERS, timeout=10)
        
        # જો Cricbuzz બ્લોક કરે તો Error મેસેજ આપશે
        if r.status_code != 200:
            return jsonify({"error": f"Cricbuzz blocked request: {r.status_code}"})

        page = BeautifulSoup(r.text, "html.parser") # lxml ની જગ્યાએ html.parser વાપરો
        
        # મેચ શોધવા માટેના Tags (Cricbuzz ના લેટેસ્ટ ક્લાસ મુજબ)
        matches = page.find_all("div", class_="cb-lv-scrs-col")
        
        live_list = []
        for m in matches:
            if m.text.strip():
                live_list.append(m.text.strip())
        
        return jsonify(live_list)
    except Exception as e:
        # જો કોઈ ભૂલ આવે તો તે અહીં દેખાશે
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
