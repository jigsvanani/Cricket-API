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

from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from googlesearch import search

app = Flask(__name__)

# નવી હેડર્સ લિસ્ટ
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

@app.route('/')
def website():
    return render_template('index.html')

@app.route('/live')
def live_matches():
    try:
        # NDTV Sports નો ઉપયોગ (Cricbuzz બ્લોક કરે છે એટલે)
        link = "https://sports.ndtv.com/cricket/live-scores"
        r = requests.get(link, headers=HEADERS, timeout=15)
        
        page = BeautifulSoup(r.text, "html.parser")
        live_list = []

        # NDTV ના લાઈવ સ્કોર કાર્ડ્સ
        matches = page.find_all("div", class_="sp-scr_cd")
        
        for m in matches:
            data = m.get_text(separator=" ").strip()
            if data:
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
        # NDTV Sports Schedule page
        link = "https://sports.ndtv.com/cricket/schedules-fixtures"
        r = requests.get(link, headers=HEADERS, timeout=15)
        
        page = BeautifulSoup(r.text, "html.parser")
        schedule_list = []

        # NDTV પર શેડ્યૂલ માટેના ટેગ્સ
        containers = page.find_all("div", class_="sp-scr_cd") # મેચ કાર્ડ્સ
        
        for item in containers:
            data = item.get_text(separator=" ").strip()
            if data:
                clean_data = " ".join(data.split())
                schedule_list.append(clean_data)

        if not schedule_list:
            return jsonify(["No upcoming matches found in schedule."])
            
        return jsonify(schedule_list)
    except Exception as e:
        return jsonify({"error": str(e)})

# Player Search Route (તમારો ઓરિજિનલ કોડ અહીં આવશે)
@app.route('/players/<player_name>', methods=['GET'])
def get_player(player_name):
    # ... (તમારો પ્લેયર સર્ચ વાળો કોડ)
    return jsonify({"message": "Player search logic here"})

if __name__ == "__main__":
    app.run()



