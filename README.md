# Final project - Footdle

## Project description

Our project was designed with the intention to entertain the user with a game of Footdle— a football-themed twist on the popular game Wordle. Instead of guessing words, players attempt to identify a mystery footballer. With each guess, hints reveal whether key attributes like Position, Age, League, Country, Club, and Market Value match the secret player. To add a competitive edge, users can also challenge the computer to see who guesses correctly first. Data for the players are scraped from [Transfermarkt][https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop]. In addition to the game, users can browse a full list of players and view detailed player statistics.

## Setting up

To set up and run the project locally, the steps explained below need to be followed.

### 1. Clone or download the repository
### 2. Check your version of Python (Python 3.10 or greater required)
### 3. Install the required packages listed in requirements.txt
### 4. Run the project.
```
streamlit run projekt.py
```

## Details
### Data

The data used for this project is sourced from two platforms, [Wikipedia][https://en.wikipedia.org/wiki/Main_Page] and [Transfermarkt][https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop]. The former is used to download player's pictures shown in Player's Statistics page, the latter uses the list of most expensive football players and scrapes the first 100 of them. The data are stored for an hour, after an hour, the data are scraped again.

### Footdle explained

Authors: Jakub Čejchan, Veronika Stuchlíková