# Final project - Footdle

## Project description

Our project was designed with the intention to entertain the user with a game of Footdle— a football-themed twist on the popular game Wordle. Instead of guessing words, players attempt to identify a mystery footballer. With each guess, hints reveal whether key attributes like Position, Age, League, Country, Club, and Market Value match the secret player. To add a competitive edge, users can also challenge the computer to see who guesses correctly first. Data for the players are scraped from [Transfermarkt](https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop). In addition to the game, users can browse a full list of players and view detailed player statistics.

## Setting up

To set up and run the project locally, the steps explained below need to be followed.

 **1. Clone or download the repository**

 **2. Check your version of Python (Python 3.10 or greater required)**

 **3. Install the required packages listed in requirements.txt**

 **4. Run the project.**
```
streamlit run projekt.py
```

## Details
### Data

The data used for this project is sourced from two platforms, [Wikipedia](https://en.wikipedia.org/wiki/Main_Page) and [Transfermarkt](https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop). The former is used to download player's pictures shown in Player's Statistics page, the latter uses the list of most expensive football players and scrapes the first 100 of them. The data are stored for an hour, after an hour, the data are scraped again.

### Footdle explained

Footdle is a football-themed guessing game where your goal is to identify a hidden player from a list of the top 100 most valuable footballers, which are (re)scraped every hour. Each time you guess a player, the game gives you feedback on how close you are in terms of various attributes like position, age, nationality, club, league, and market value. Correct guesses light up in green, incorrect ones in red, arrows show whether the hidden player's attribute is higher or lower than your guess.

**Against computer mode**
In computer mode, competitive edge is added. Before the game starts, you choose a difficulty level. The difiiculty level determines with what probability the bot makes a contaminated guess, i.e. with what probability the bot chooses a false positive as their guess (choosing an incorrect player even when it has enough information to narrow it down). After every guess you make, the bot takes its turn. The game ends when either you or the computer identifies the secret player, or both do on the same turn, resulting in a draw.

Authors: Jakub Čejchan, Veronika Stuchlíková