
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
from dateutil import parser
import re
from bs4 import BeautifulSoup
import streamlit as st
import wikipedia
import warnings as warnings
import time


# ------------------------------------------
# Define multiple clubs with their slugs & IDs
# ------------------------------------------
clubs = {
    "Chelsea": ("chelsea-fc", 631),
    "Manchester City": ("manchester-city", 281),
    "Arsenal": ("fc-arsenal", 11),
    "Liverpool": ("fc-liverpool", 31)
}

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
# Scraping function with caching
# ----------------------------
@st.cache_data(ttl=3600)
def get_players(club_slug, club_id, club_name):
    url = f"https://www.transfermarkt.com/{club_slug}/startseite/verein/{club_id}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="items")
    players = {}

    if table:
        rows = table.find_all("tr", class_=["odd", "even"])
        for row in rows[:15]:  # Limit to 15 players
            try:
                name = row.find("td", class_="hauptlink").a.text.strip()

                tds = row.find_all("td")
                position = tds[4].text.strip()
                age = tds[5].text.strip()
                market_value = tds[-1].text.strip()

                nationality_img = tds[6].find("img")
                nationality = nationality_img["title"] if nationality_img else "Unknown"

                img_url = get_wikipedia_image(name)

                players[name] = {
                    "Date of Birth (Age)": age,
                    "Country of Birth": nationality,
                    "Position": position,
                    "Market Value": market_value,
                    "Club": club_name,
                    "Image": img_url
                }
            except Exception as e:
                print("Error with row:", e)
                continue

    return players


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

def convert_market_value(mv_string):
    mv_string = mv_string.replace('€', '').replace(',', '').strip().lower()
    if mv_string.endswith('m'):
        num = float(mv_string[:-1])
        return int(num) if num.is_integer() else num
    return None

def get_players2():
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
                data.append({
                    "Name": name,
                    "Position": position_short,
                    "Age": age,
                    "Country": country,
                    "Club": club,
                    "Market Value (€ mil.)": market_value
                })
    df = pd.DataFrame(data)
    return df


# ----------------------------
# Sidebar Navigation
# ----------------------------
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

with st.sidebar:
    st.title("Navi")
    if st.button("Home"):
        st.session_state.page = 'Home'
    if st.button("Stats"):
        st.session_state.page = 'Stats'
    if st.button('FootDle'):
        st.session_state.page = 'FootDle'
    if st.button("Players"): 
        st.session_state.page = 'Players'

# ----------------------------
# Home Page
# ----------------------------
if st.session_state.page == 'Home':
    st.title("Welcome to the Football App")
    st.write("Use the sidebar to navigate!")

# ----------------------------
# Stats Page
# ----------------------------
elif st.session_state.page == 'Stats':
    st.title("Football Player Stats")

    club_choice = st.selectbox("Choose a club", list(clubs.keys()))
    club_slug, club_id = clubs[club_choice]

    players = get_players(club_slug, club_id, club_choice)

    if players:
        player_choice = st.selectbox("Choose a player", list(players.keys()))
        player_data = players[player_choice]

        st.subheader(f"{player_choice}")
        col1, col2 = st.columns([1, 2])

        with col1:
            if player_data.get("Image"):
                st.image(player_data["Image"], width=200)
            else:
                st.write("No image found.")

        with col2:
            for key in ["Date of Birth (Age)", "Country of Birth", "Position","Market Value", "Club"]:
                st.write(f"**{key}**: {player_data[key]}")
    else:
        st.error("Could not load player data.")

# ----------------------------
# Footdle Page
# ----------------------------
elif st.session_state.page == 'FootDle':
    st.title("Footdle - Guess the Player!")

    # --- Initial state setup ---
    if "footdle_started" not in st.session_state:
        st.session_state.footdle_started = False
    if "footdle_secret" not in st.session_state:
        st.session_state.footdle_secret = None
    if "footdle_guesses" not in st.session_state:
        st.session_state.footdle_guesses = []

    if not st.session_state.footdle_started:
        if st.button("Start"):
            player_df = get_players2()
            st.session_state.footdle_player_df = player_df
            secret_row = player_df.sample(1).iloc[0]
            st.session_state.footdle_secret = secret_row.to_dict()
            st.session_state.footdle_guesses = []
            st.session_state.footdle_started = True

    if st.session_state.footdle_started:
        player_df = st.session_state.get("footdle_player_df", get_players2())
        player_names = player_df["Name"].tolist()

        col1, col2 = st.columns([4, 1])
        with col1:
            guess = st.selectbox(
                "Type or pick a player's name:",
                options=[""] + player_names,
                key="footdle_select"
            )
        with col2:
            # Button is always visible
            if st.button("Guess"):
                if guess and guess not in st.session_state.footdle_guesses:
                    st.session_state.footdle_guesses.append(guess)

        secret = st.session_state.footdle_secret

        # Headers row (always visible, one row at the top)
        headers_html = """
        <div style="display:grid;grid-template-columns:160px repeat(5, 120px);gap:18px;margin-bottom:2px;">
            <div></div>
            <div style="text-align:center;font-weight:bold;">POSITION</div>
            <div style="text-align:center;font-weight:bold;">AGE</div>
            <div style="text-align:center;font-weight:bold;">COUNTRY</div>
            <div style="text-align:center;font-weight:bold;">CLUB</div>
            <div style="text-align:center;font-weight:bold;">VALUE (€ mil.) </div>
        </div>
        """
        st.markdown(headers_html, unsafe_allow_html=True)

        # --- Show guess boxes for each attempt ---
        arrow_up_svg = f"""
        <svg width="28" height="28" style="vertical-align:middle;opacity:0.7;" viewBox="0 0 16 16"><path fill="black" d="M8 4l4 8H4z"/></svg>
        """
        arrow_down_svg = f"""
        <svg width="28" height="28" style="vertical-align:middle;opacity:0.7;transform: rotate(180deg);" viewBox="0 0 16 16"><path fill="black" d="M8 4l4 8H4z"/></svg>
        """

        # ... (inside your guess loop)
        for idx, guessed_name in enumerate(st.session_state.footdle_guesses):
            guess_row = player_df[player_df["Name"] == guessed_name].iloc[0]
            correct = {
                "Position": guess_row["Position"] == secret["Position"],
                "Age": guess_row["Age"] == secret["Age"],
                "Country": guess_row["Country"] == secret["Country"],
                "Club": guess_row["Club"] == secret["Club"],
                "Market Value (€ mil.)": guess_row["Market Value (€ mil.)"] == secret["Market Value (€ mil.)"]
            }
            values = {
                "Position": guess_row["Position"],
                "Age": guess_row["Age"],
                "Country": guess_row["Country"],
                "Club": guess_row["Club"],
                "Market Value (€ mil.)": guess_row["Market Value (€ mil.)"]
            }

            def get_bg(col):
                return "#3dcc4a" if correct[col] else "#df2222"

            # ARROW LOGIC
            def arrow_html(guess, real, correct):
                if correct:
                    return ""
                try:
                    guess = int(guess)
                    real = int(real)
                    if guess < real:
                        return arrow_up_svg
                    elif guess > real:
                        return arrow_down_svg
                except:
                    pass
                return ""

            age_arrow = arrow_html(values["Age"], secret["Age"], correct["Age"])
            mv_arrow = arrow_html(values["Market Value (€ mil.)"], secret["Market Value (€ mil.)"], correct["Market Value (€ mil.)"])

            # Use grid for alignment, name in first cell only (not inside a box)
            html = f"""
            <div style="display:grid;grid-template-columns:160px repeat(5, 120px);gap:18px;align-items:center;margin-bottom:10px;">
                <div style="font-weight:bold;font-size:1.1em;color:white;letter-spacing:1px;">{guessed_name}</div>
                <div style="border:6px solid black; background:{get_bg('Position')}; border-radius:7px; height:90px;display:flex;align-items:center;justify-content:center;font-size:2em;">{values['Position']}</div>
                <div style="border:6px solid black; background:{get_bg('Age')}; border-radius:7px; height:90px;display:flex;align-items:center;justify-content:center;font-size:2em;position:relative;">
                    <span>{values['Age']}</span>
                    <span style="margin-left:8px;">{age_arrow}</span>
                </div>
                <div style="border:6px solid black; background:{get_bg('Country')}; border-radius:7px; height:90px;display:flex;align-items:center;justify-content:center;font-size:1.4em;">{values['Country']}</div>
                <div style="border:6px solid black; background:{get_bg('Club')}; border-radius:7px; height:90px;display:flex;align-items:center;justify-content:center;white-space:normal;text-align:center;font-size:1.2em;">{values['Club']}</div>
                <div style="border:6px solid black; background:{get_bg('Market Value (€ mil.)')}; border-radius:7px; height:90px;display:flex;align-items:center;justify-content:center;font-size:2em;position:relative;">
                    <span>{values['Market Value (€ mil.)']}</span>
                    <span style="margin-left:8px;">{mv_arrow}</span>
                </div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)

            # Win condition
            if all(correct.values()):
                st.success(f"🎉 YOU WIN! THE PLAYER WAS **{secret['Name']}**!")
                st.session_state.footdle_started = False
                break

        # ---- Below the guesses table ----
        col_restart, col_giveup = st.columns([1, 1])
        with col_restart:
            if st.button("Restart"):
                st.session_state.footdle_started = False
                st.session_state.footdle_secret = None
                st.session_state.footdle_guesses = []
        with col_giveup:
            if st.button("Give Up"):
                answer = st.session_state.footdle_secret["Name"] if st.session_state.footdle_secret else "unknown"
                st.info(f"😴 You gave up! The answer was: **{answer}**")
                st.session_state.footdle_started = False
                st.session_state.footdle_secret = None
                st.session_state.footdle_guesses = []
# ----------------------------
# Players Page
# ----------------------------
elif st.session_state.page == 'Players':
    st.title("Top 100 Most Valuable Players")
    df = get_players2()
    st.dataframe(df, hide_index=True)

