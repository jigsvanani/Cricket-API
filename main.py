from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import json

app = Flask(__name__)

# Headers ને ગ્લોબલ કરી દીધા જેથી દરેક ફંક્શનમાં વાપરી શકાય
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

@app.route('/players/<player_name>', methods=['GET'])
def get_player(player_name):
    query = f"{player_name} cricbuzz profile"
    profile_link = None
    try:
        # Search results માંથી પહેલી લિંક લેવી
        for link in search(query, num_results=10):
            if "cricbuzz.com/profiles/" in link:
                profile_link = link
                break
        
        if not profile_link:
            return jsonify({"error": "No player profile found"}), 404
            
        source = requests.get(profile_link, headers=headers).text
        soup = BeautifulSoup(source, "lxml")
        
        # પ્રોફાઇલનો મુખ્ય વિભાગ
        name = soup.find("h1", class_="cb-font-40").text.strip()
        country = soup.find("h3", class_="cb-font-18 text-gray").text.strip()
        
        # બાકીની વિગતો માટે ડિક્શનરી બનાવવી
        player_data = {
            "name": name,
            "country": country,
            "profile_url": profile_link,
            "batting_stats": {},
            "bowling_stats": {}
        }
        
        # આંકડાઓ (Stats) કાઢવા માટે ટેબલ લોજિક અહીં ઉમેરી શકાય...
        return jsonify(player_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/schedule')
def schedule():
    url = "https://www.cricbuzz.com/cricket-schedule/upcoming-series/international"
    try:
        source = requests.get(url, headers=headers).text
        soup = BeautifulSoup(source, "lxml")
        
        # Cricbuzz schedule page structure
        match_containers = soup.find_all("div", class_="cb-col-100 cb-col")
        matches = []

        for container in match_containers:
            date_div = container.find("div", class_="cb-lv-grn-strip")
            match_div = container.find("div", class_="cb-ovr-flo")
            
            if date_div and match_div:
                matches.append({
                    "date": date_div.text.strip(),
                    "match": match_div.text.strip()
                })
        
        return jsonify(matches)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/live')
def live_matches():
    url = "https://www.cricbuzz.com/cricket-match/live-scores"
    try:
        source = requests.get(url, headers=headers).text
        soup = BeautifulSoup(source, "lxml")
        
        # તમારી અગાઉની સ્ક્રીનશોટ મુજબના ક્લાસ અહીં વાપર્યા છે
        match_cards = soup.find_all("div", class_="flex flex-col gap-2")
        
        live_list = []
        for card in match_cards:
            # મેચનું નામ અને સ્કોર ટેક્સ્ટ તરીકે લેવા
            summary = card.text.strip()
            # લાઈવ ટેક્સ્ટને ક્લીન કરવું (વધારાની સ્પેસ કાઢવી)
            clean_summary = " ".join(summary.split())
            if clean_summary:
                live_list.append(clean_summary)
        
        return jsonify({"live_matches": live_list})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def website():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
