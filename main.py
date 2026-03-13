from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# તમારી API Key
API_KEY = "c1e3e885-689d-45dd-9b38-1e36c50b9895"

# સર્વરને છેતરવા માટે headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

@app.route('/')
def website():
    return render_template('index.html')

@app.route('/live')
def live_matches():
    try:
        url = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0"
        # અહીં headers અને timeout ઉમેર્યા છે
        r = requests.get(url, headers=headers, timeout=15)
        response_data = r.json()
        
        live_list = []
        if response_data.get("status") == "success":
            for match in response_data.get("data", []):
                match_info = f"{match['name']} | {match['status']}"
                live_list.append(match_info)
        
        return jsonify(live_list if live_list else ["No live matches found."])
    except Exception as e:
        return jsonify([f"API Error: {str(e)}"])

@app.route('/schedule')
def schedule():
    try:
        url = f"https://api.cricapi.com/v1/matches?apikey={API_KEY}&offset=0"
        r = requests.get(url, headers=headers, timeout=15)
        response_data = r.json()
        
        schedule_list = []
        if response_data.get("status") == "success":
            for match in response_data.get("data", [])[:10]:
                schedule_list.append(f"{match['date']}: {match['name']}")
                
        return jsonify(schedule_list if schedule_list else ["Schedule not found."])
    except Exception as e:
        return jsonify([f"Schedule Error: {str(e)}"])

if __name__ == "__main__":
    app.run()
