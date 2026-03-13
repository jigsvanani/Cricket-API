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
        
        # મુખ્ય કન્ટેનર શોધો જેમાં બધી સીરીઝ છે
        # (તમારા સ્ક્રીનશોટ મુજબનો ક્લાસ વાપર્યો છે)
        main_container = soup.find("div", class_="flex flex-col gap-2")
        
        # બધી સીરીઝના બ્લોક્સ મેળવો
        series_blocks = main_container.find_all("div", recursive=False)
        
        all_data = []

        for block in series_blocks:
            # ૧. સીરીઝનું નામ (દા.ત. ICC MEN'S T20...)
            series_header = block.find("div", class_="bg-cbGrphHdrBkg")
            if not series_header:
                continue
            series_name = series_header.text.strip()
            
            matches_in_series = []
            
            # ૨. આ સીરીઝની બધી મેચો શોધો (a tags)
            match_cards = block.find_all("a", class_="bg-cbWhite")
            
            for card in match_cards:
                # મેચની ટૂંકી વિગત (દા.ત. 8th Match, George Town)
                match_desc = card.find("div", class_="text-cbTxtSec").text.strip() if card.find("div", class_="text-cbTxtSec") else ""
                
                # ટીમો અને સ્કોર માટે ટેક્સ્ટ લાઈનો મેળવીએ
                # આમાં સામાન્ય રીતે પહેલી બે લાઈન ટીમ અને સ્કોર હોય છે
                team_scores = []
                # ટીમના નામ અને સ્કોર વાળા div શોધો
                score_divs = card.find_all("div", class_="flex justify-between items-center")
                
                for s_div in score_divs:
                    team_scores.append(s_div.text.strip())
                
                # ૩. મેચનું સ્ટેટસ (કોણ જીત્યું અથવા લાઈવ અપડેટ)
                # આ સામાન્ય રીતે છેલ્લી લાઈન હોય છે
                status = ""
                status_div = card.find("div", class_="text-cbTxtLive") or card.find("div", class_="text-cbTxtWin") or card.find("div", class_="text-cbTxtSec", recursive=False)
                if status_div:
                    status = status_div.text.strip()

                # ડેટાને વ્યવસ્થિત ડિક્શનરીમાં ગોઠવો
                match_info = {
                    "match_description": match_desc,
                    "teams_scores": team_scores,
                    "result_status": status
                }
                matches_in_series.append(match_info)
            
            # સીરીઝ મુજબ ડેટા ભેગો કરો
            all_data.append({
                "series_name": series_name,
                "matches": matches_in_series
            })
        
        return jsonify(all_data)
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def website():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

