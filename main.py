from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# તમારી સાચી API Key
API_KEY = "c1e3e885-689d-45dd-9b38-1e36c50b9895"
BASE_URL = "https://api.cricapi.com/v1"

@app.route('/')
def website():
    return render_template('index.html')

@app.route('/live')
def live_matches():
    try:
        # ડોક્યુમેન્ટેશન મુજબ 'currentMatches' એન્ડપોઈન્ટ
        url = f"{BASE_URL}/currentMatches?apikey={API_KEY}&offset=0"
        r = requests.get(url, timeout=15)
        response = r.json()
        
        live_list = []
        if response.get("status") == "success":
            for match in response.get("data", []):
                # મેચ લાઈવ હોય તો જ લેવી
                if match.get("matchStarted"):
                    # ટીમનું નામ અને સ્કોર/સ્ટેટસ
                    info = f"{match['name']} | Status: {match['status']}"
                    live_list.append(info)
        
        return jsonify(live_list if live_list else ["No live matches right now."])
    except Exception as e:
        return jsonify([f"Error: {str(e)}"])

@app.route('/schedule')
def schedule():
    try:
        # ડોક્યુમેન્ટેશન મુજબ 'matches' એન્ડપોઈન્ટ આવનારી મેચો માટે
        url = f"{BASE_URL}/matches?apikey={API_KEY}&offset=0"
        r = requests.get(url, timeout=15)
        response = r.json()
        
        schedule_list = []
        if response.get("status") == "success":
            # આવનારી ૧૫ મેચો બતાવવી
            for match in response.get("data", [])[:15]:
                date = match.get("date", "TBA")
                schedule_list.append(f"{date}: {match['name']} ({match['matchType'].upper()})")
                
        return jsonify(schedule_list if schedule_list else ["No schedule found."])
    except Exception as e:
        return jsonify([f"Error: {str(e)}"])

@app.route('/players/<player_name>')
def get_player(player_name):
    try:
        # ૧. પહેલા પ્લેયરને નામથી સર્ચ કરો (ID મેળવવા માટે)
        search_url = f"{BASE_URL}/playersList?apikey={API_KEY}&search={player_name}"
        search_r = requests.get(search_url)
        search_data = search_r.json()
        
        if search_data.get("status") != "success" or not search_data.get("data"):
            return jsonify({"error": "Player not found"})
            
        # ૨. પહેલા પ્લેયરની ID લો
        player_id = search_data["data"][0]["id"]
        
        # ૩. પ્લેયરની આખી પ્રોફાઇલ મેળવો
        info_url = f"{BASE_URL}/playerInfo?apikey={API_KEY}&id={player_id}"
        info_r = requests.get(info_url)
        info_data = info_r.json()
        
        if info_data.get("status") == "success":
            p = info_data["data"]
            return jsonify({
                "name": p.get("name"),
                "country": p.get("country"),
                "role": p.get("role"),
                "image": p.get("playerImg"),
                "stats": "Check documentation for full stats display"
            })
            
        return jsonify({"error": "Could not fetch stats"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run()
