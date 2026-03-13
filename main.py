from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# તમારી API KEY અહીં નાખો (CricketData.org માંથી મળેલી)
API_KEY = "c1e3e885-689d-45dd-9b38-1e36c50b9895"

@app.route('/')
def website():
    return render_template('index.html')

@app.route('/live')
def live_matches():
    try:
        # CricketData API endpoint
        url = f"https://api.cricketdata.org/v1/currentMatches?apikey={API_KEY}"
        r = requests.get(url)
        data = r.json()
        
        live_list = []
        if data.get("status") == "success":
            for match in data.get("data", []):
                # જો મેચ ચાલુ હોય (Live) તો જ લેવી
                if match.get("matchStarted"):
                    match_info = f"{match['name']} - {match['status']}"
                    live_list.append(match_info)
        
        return jsonify(live_list if live_list else ["No live matches found."])
    except Exception as e:
        return jsonify([f"API Error: {str(e)}"])

@app.route('/schedule')
def schedule():
    try:
        url = f"https://api.cricketdata.org/v1/matches?apikey={API_KEY}"
        r = requests.get(url)
        data = r.json()
        
        schedule_list = []
        if data.get("status") == "success":
            for match in data.get("data", [])[:10]: # પહેલા ૧૦ મેચ
                schedule_list.append(f"{match['date']}: {match['name']}")
                
        return jsonify(schedule_list if schedule_list else ["Schedule not found."])
    except Exception as e:
        return jsonify([f"Schedule Error: {str(e)}"])

if __name__ == "__main__":
    app.run()
