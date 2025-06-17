
from packages import requests, pd, BeautifulSoup, wikipedia, st

# ----------------------------
# Get player image from Wikipedia
# ----------------------------
@st.cache_data(ttl=3600)
def get_wikipedia_image(player_name):
    try:
        page_title = wikipedia.search(player_name)[0]
        page = wikipedia.page(page_title)
        response = requests.get(page.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        infobox = soup.find('table', {'class': 'infobox'})
        if infobox:
            img = infobox.find('img')
            if img:
                return "https:" + img['src']
    except Exception:
        return None
    

# ----------------------------
# Players scrape
# ----------------------------
POSITION_MAP = {
    "Goalkeeper": "GK",
    "Left-Back": "LB",
    "Right-Back": "RB",
    "Centre-Back": "CB",
    "Defensive Midfield": "CDM",
    "Attacking Midfield": "CAM",
    "Central Midfield": "CM",
    "Centre-Forward": "ST",
    "Left Winger": "LW",
    "Right Winger": "RW",
    "Second Striker": "CF",
}

CLUB_TO_LEAGUE = {
    # Bundesliga
    "Bayern Munich": "Bundesliga",
    "Borussia Dortmund": "Bundesliga",
    "RB Leipzig": "Bundesliga",
    "Bayer 04 Leverkusen": "Bundesliga",
    "Eintracht Frankfurt": "Bundesliga",
    # Campeonato Brasileiro Série A
    "Sociedade Esportiva Palmeiras": "Campeonato Brasileiro Série A",
    # La Liga
    "Real Madrid": "La Liga",
    "FC Barcelona": "La Liga",
    "Atlético de Madrid": "La Liga",
    "Villarreal CF": "La Liga",
    "Real Sociedad": "La Liga",
    "Athletic Bilbao": "La Liga",
    # Ligue 1
    "Paris Saint-Germain": "Ligue 1",
    # Premier League
    "Manchester United": "Premier League",
    "Manchester City": "Premier League",
    "Chelsea FC": "Premier League",
    "Arsenal FC": "Premier League",
    "Liverpool FC": "Premier League",
    "Newcastle United": "Premier League",
    "Tottenham Hotspur": "Premier League",
    "Brighton & Hove Albion": "Premier League",
    "Everton FC": "Premier League",
    "Brentford FC": "Premier League",
    "Crystal Palace": "Premier League",
    "Aston Villa": "Premier League",
    "Nottingham Forest": "Premier League",
    "Wolverhampton Wanderers": "Premier League",
    # Primeira Liga
    "FC Porto": "Primeira Liga",
    "Sporting CP": "Primeira Liga",
    # Serie A
    "Juventus FC": "Serie A",
    "AC Milan": "Serie A",
    "Inter Milan": "Serie A",
    "Atalanta BC": "Serie A",
    # Süper Lig
    "Galatasaray": "Süper Lig",
}

def convert_market_value(mv_string):
    mv_string = mv_string.replace('€', '').replace(',', '').strip().lower()
    if mv_string.endswith('m'):
        num = float(mv_string[:-1])
        return int(num) if num.is_integer() else num
    return None

@st.cache_data(ttl=3600)
def get_players():
    headers = {'User-Agent': 'Mozilla/5.0'}
    base_url = "https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop"
    data = []
    for page in range(1, 5):  # Pages 1 to 4 = 100 players
        url = f"{base_url}?page={page}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")
        table = soup.find("table", class_="items")
        rows = table.find_all("tr", class_=["odd", "even"])
        for row in rows:
            tds = row.find_all("td")
            if len(tds) >= 9:
                name = tds[3].text.strip()
                age = tds[5].text.strip()
                market_value_str = tds[8].text.strip()
                market_value = convert_market_value(market_value_str)
                position = tds[4].text.strip()
                position_short = POSITION_MAP.get(position, position)
                country_img = tds[6].find("img")
                country = country_img["title"] if country_img else ""
                club_img = tds[7].find("img") 
                club = club_img["alt"] if club_img else "" 
                league = CLUB_TO_LEAGUE.get(club, "Unknown")
                data.append({
                    "Name": name,
                    "Position": position_short,
                    "Age": age,
                    "Country": country,
                    "Club": club,
                    "League": league,
                    "Market Value (€ mil.)": market_value
                })
    df = pd.DataFrame(data)
    return df