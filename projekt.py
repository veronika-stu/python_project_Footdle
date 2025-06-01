
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


# ------------------------------------------
# Define multiple clubs with their slugs & IDs
# ------------------------------------------
clubs = {
    "Chelsea": ("chelsea-fc", 631),
    "Manchester City": ("manchester-city", 281),
    "Arsenal": ("fc-arsenal", 11),
    "Liverpool": ("fc-liverpool", 31),
    "Real Madrid": ("real-madrid", 418)
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