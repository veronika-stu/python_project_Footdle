from packages import st, pd
from scrape import get_players

def footdle_page():
    st.title("Footdle - Guess the Player!")
    
    if "footdle_mode" not in st.session_state:
        st.session_state.footdle_mode = None

   
    if st.session_state.footdle_mode is None:
        st.markdown("""
        Welcome to **Footdle**!  
        - In **Solo** mode, guess the player in as few tries as possible.  
        - In **Against Computer** mode, you and the bot will compete to see who can guess first!  
        _Choose your mode below:_
        """)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Solo"):
                st.session_state.footdle_mode = "Solo"
                st.rerun()
        with col2:
            if st.button("Against Computer"):
                st.session_state.footdle_mode = "Computer"
                st.rerun()
        

        st.markdown("---")

        st.markdown("#### ▶️ How to Play:")
        st.markdown("""
        1. **Type or choose a player** from the dropdown and press **Guess**.  
        2. **Repeat** until you guess the correct player.  
        3. If you're stuck, click **Give Up** (*Solo mode*) or get beaten (*Computer mode*) to reveal the answer. 
        4. Want a fresh challenge? Click **Restart** – but note: you won’t see the current answer!
        """)

        st.markdown("#### ℹ️ How it works:")


        col3, col4 = st.columns(2)

        with col3:
            st.markdown(" 🎯 *Color Tiles*")
            st.markdown("""
            <div style="display:flex;gap:12px;align-items:center;">
                <div style="width:40px;height:40px;background:#3dcc4a;border:2px solid black;border-radius:6px;"></div>
                <span style="font-size:1em;">Green = Correct</span>
            </div>
            <div style="display:flex;gap:12px;align-items:center;margin-top:10px;">
                <div style="width:40px;height:40px;background:#df2222;border:2px solid black;border-radius:6px;"></div>
                <span style="font-size:1em;">Red = Incorrect</span>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown("🔼🔽 *Arrows*")
            st.markdown("""
            <div style="display:flex;gap:12px;align-items:center;margin-bottom:12px;">
                <div style="width:40px;height:40px;background:#df2222;border:2px solid black;border-radius:6px;
                            display:flex;align-items:center;justify-content:center;font-size:1.2em;">
                    ▲
                </div>
                <span style="font-size:1em;">Arrow Up = Actual value is higher</span>
            </div>
            <div style="display:flex;gap:12px;align-items:center;">
                <div style="width:40px;height:40px;background:#df2222;border:2px solid black;border-radius:6px;
                            display:flex;align-items:center;justify-content:center;font-size:1.2em;">
                    ▼
                </div>
                <span style="font-size:1em;">Arrow Down = Actual value is lower</span>
            </div>
            """, unsafe_allow_html=True) 


        st.markdown("---")
        st.markdown("*Tip: For the best experience, hide the sidebar by clicking the arrow in the top right.*")

        st.stop()



   
    if st.button("⬅ Back to mode select"):
        st.session_state.footdle_mode = None
        st.session_state.footdle_started = False
        st.session_state.footdle_secret = None
        st.session_state.footdle_guesses = []
        st.session_state.footdle_gave_up_message = False
        st.session_state.footdle_win_message = False
        st.rerun()

    # === SOLO MODE ===
    if st.session_state.footdle_mode == "Solo":
        
        if "footdle_started" not in st.session_state:
            st.session_state.footdle_started = False
        if "footdle_secret" not in st.session_state:
            st.session_state.footdle_secret = None
        if "footdle_guesses" not in st.session_state:
            st.session_state.footdle_guesses = []
        if "footdle_gave_up_message" not in st.session_state:
            st.session_state.footdle_gave_up_message = False
        if "footdle_win_message" not in st.session_state:
            st.session_state.footdle_win_message = False

      
        if not st.session_state.footdle_started:
            if st.button("Start"):
                player_df = get_players()
                st.session_state.footdle_player_df = player_df
                secret_row = player_df.sample(1).iloc[0]
                st.session_state.footdle_secret = secret_row.to_dict()
                st.session_state.footdle_guesses = []
                st.session_state.footdle_started = True
                st.session_state.footdle_gave_up_message = False
                st.session_state.footdle_win_message = False
                st.rerun()
            st.stop()

        player_df = st.session_state.get("footdle_player_df", get_players())
        player_names = sorted(player_df["Name"].tolist())

        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        with col1:
            guess = st.selectbox(
                "Type or pick a player's name:",
                options=[""] + player_names,
                key="footdle_select"
            )
        with col2:
            st.markdown("<div style='margin-top: 32px;'>", unsafe_allow_html=True)
            if st.button("Guess"):
                # Don't allow guessing after giving up or after win
                if guess and guess not in st.session_state.footdle_guesses and not st.session_state.footdle_gave_up_message and not st.session_state.footdle_win_message and st.session_state.footdle_started:
                    st.session_state.footdle_guesses.append(guess)
                    st.rerun()
        with col3:
            st.markdown("<div style='margin-top: 32px;'>", unsafe_allow_html=True)
            if st.button("Give Up"):
                st.session_state.footdle_gave_up_message = True
                st.rerun()
        with col4:
            st.markdown("<div style='margin-top: 32px;'>", unsafe_allow_html=True)
            if st.button("Restart"):
                st.session_state.footdle_started = False
                st.session_state.footdle_secret = None
                st.session_state.footdle_guesses = []
                st.session_state.footdle_gave_up_message = False
                st.session_state.footdle_win_message = False
                st.rerun()

        secret = st.session_state.footdle_secret

        #message block
        if st.session_state.footdle_gave_up_message:
            answer = secret["Name"] if secret else "unknown"
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; margin-top: 20px;">
                                <div style="max-width: 1400px;
                            width: 100%;
                            background: #253347;
                            color: #fff;
                            font-size: 1.3em;
                            padding: 24px 0;
                            border-radius: 18px;
                            font-weight: bold;
                            text-align: center;
                            letter-spacing: 0.01em;
                            box-shadow: 0 8px 32px rgba(0,0,0,0.13);">
                    😴 You gave up! The answer was: <span style="color:#1be7b7">{answer}</span><br>
                    <span style="font-size:0.85em; color:#b2b8c2; font-weight:normal;">Who is that? Check our player desc!</span>
                </div>
                """,
                unsafe_allow_html=True
            )



    
        headers_html = """
        <div style="display:grid;grid-template-columns:160px repeat(6, 120px);gap:18px;margin-bottom:2px;">
            <div></div>
            <div style="text-align:center;font-weight:bold;">POSITION</div>
            <div style="text-align:center;font-weight:bold;">AGE</div>
            <div style="text-align:center;font-weight:bold;">COUNTRY</div>
            <div style="text-align:center;font-weight:bold;">CLUB</div>
            <div style="text-align:center;font-weight:bold;">LEAGUE</div>
            <div style="text-align:center;font-weight:bold;">VALUE (€ mil.) </div>
        </div>
        """
        st.markdown(f"""<div style='display: flex; justify-content: center;'>{headers_html}</div>""", unsafe_allow_html=True)

        # SVGs for arrows
        arrow_up_svg = """
        <svg width="28" height="28" style="vertical-align:middle;opacity:0.7;" viewBox="0 0 16 16"><path fill="black" d="M8 4l4 8H4z"/></svg>
        """
        arrow_down_svg = """
        <svg width="28" height="28" style="vertical-align:middle;opacity:0.7;transform: rotate(180deg);" viewBox="0 0 16 16"><path fill="black" d="M8 4l4 8H4z"/></svg>
        """

        
        win = False
        for idx, guessed_name in enumerate(reversed(st.session_state.footdle_guesses)):
            guess_row = player_df[player_df["Name"] == guessed_name].iloc[0]
            correct = {
                "Position": guess_row["Position"] == secret["Position"],
                "Age": guess_row["Age"] == secret["Age"],
                "Country": guess_row["Country"] == secret["Country"],
                "Club": guess_row["Club"] == secret["Club"],
                "League": guess_row["League"] == secret["League"],
                "Market Value (€ mil.)": guess_row["Market Value (€ mil.)"] == secret["Market Value (€ mil.)"]
            }
            values = {
                "Position": guess_row["Position"],
                "Age": guess_row["Age"],
                "Country": guess_row["Country"],
                "Club": guess_row["Club"],
                "League": guess_row["League"],
                "Market Value (€ mil.)": guess_row["Market Value (€ mil.)"]
            }
            def get_bg(col):
                return "#3dcc4a" if correct[col] else "#df2222"
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
            html = f"""
            <div style="display:grid;grid-template-columns:160px repeat(6, 120px);gap:18px;align-items:center;margin-bottom:10px;">
                <div style="font-weight:bold;font-size:1.1em;color:b2b8c2;letter-spacing:1px;">{guessed_name}</div>
                <div style="border:6px solid black; background:{get_bg('Position')}; border-radius:7px; height:90px;display:flex;align-items:center;justify-content:center;font-size:2em;">{values['Position']}</div>
                <div style="border:6px solid black; background:{get_bg('Age')}; border-radius:7px; height:90px;display:flex;align-items:center;justify-content:center;font-size:2em;position:relative;">
                    <span>{values['Age']}</span>
                    <span style="margin-left:8px;">{age_arrow}</span>
                </div>
                <div style="border:6px solid black; background:{get_bg('Country')}; border-radius:7px; height:90px;display:flex;align-items:center;justify-content:center;font-size:1.4em;">{values['Country']}</div>
                <div style="border:6px solid black; background:{get_bg('Club')}; border-radius:7px; height:90px;display:flex;align-items:center;justify-content:center;white-space:normal;text-align:center;font-size:1.2em;">{values['Club']}</div>
                <div style="border:6px solid black; background:{get_bg('League')}; border-radius:7px; height:90px;display:flex;align-items:center;justify-content:center;white-space:normal;text-align:center;font-size:1.2em;">{values['League']}</div>
                <div style="border:6px solid black; background:{get_bg('Market Value (€ mil.)')}; border-radius:7px; height:90px;display:flex;align-items:center;justify-content:center;font-size:2em;position:relative;">
                    <span>{values['Market Value (€ mil.)']}</span>
                    <span style="margin-left:8px;">{mv_arrow}</span>
                </div>
            </div>
            """
            st.markdown(f"""<div style='display: flex; justify-content: center;'>{html}</div>""", unsafe_allow_html=True)

            
            if all(correct.values()) and not st.session_state.footdle_gave_up_message and st.session_state.footdle_started:
                st.session_state.footdle_win_message = True
                st.session_state.footdle_started = False
                break

        if st.session_state.get("footdle_win_message"):
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; margin-top: 20px;">
                <div style="max-width: 1400px;
                            width: 100%;
                            background: #18b87a;
                            color: #fff;
                            font-size: 1.3em;
                            padding: 24px 0;
                            border-radius: 18px;
                            font-weight: bold;
                            text-align: center;
                            letter-spacing: 0.01em;
                            box-shadow: 0 8px 32px rgba(0,0,0,0.13);">
                    🎉 YOU WIN! The player was: <span style="color:#fff700">{secret['Name']}</span><br>
                    <span style="font-size:0.85em; color:#eeeeee; font-weight:normal;">
                        Try another round or check the player’s stats!
                    </span>
                </div>
                """,
                unsafe_allow_html=True
        )



    # === COMPUTER MODE ===
    elif st.session_state.footdle_mode == "Computer":

        # difficulty selector
        if not st.session_state.get("footdle_started", False):
            st.markdown("### 🤖 Select Difficulty")

            selected = st.select_slider(
                label="",
                options=["Noob", "Easy", "Medium", "Hard", "Impossible"],
                value=st.session_state.get("footdle_difficulty", "Medium"),
                help="Pick how smart the computer is."
            )

            if st.session_state.get("footdle_difficulty") != selected:
                st.session_state.footdle_difficulty = selected
                st.rerun()

            difficulty_explanations = {
                "Noob": "🟢 Completely random guesses.",
                "Easy": "🟡 Bot has some logic, yet it is really limited",
                "Medium": "🟠 Bot has a logic of an average football fan",
                "Hard": "🔴 Bot has a logic of a football fanatic",
                "Impossible": "⚫ Bot is a machine, it almost never loses"
            }

            st.markdown(f"""
            <div style="margin-top:-10px; font-size: 20px; text-align: center;">
                <strong>{selected}</strong>: {difficulty_explanations[selected]}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("   ")
            st.markdown("   ")

        if "footdle_started" not in st.session_state:
            st.session_state.footdle_started = False
        if "footdle_secret" not in st.session_state:
            st.session_state.footdle_secret = None
        if "footdle_guesses" not in st.session_state:
            st.session_state.footdle_guesses = []
        if "footdle_bot_possible" not in st.session_state:
            st.session_state.footdle_bot_possible = None
        if "footdle_bot_guesses" not in st.session_state:
            st.session_state.footdle_bot_guesses = []
        if "footdle_win_message" not in st.session_state:
            st.session_state.footdle_win_message = None

        if not st.session_state.footdle_started:
            col1, col2, col3 = st.columns([2.2, 1, 2])
            with col2:
                if st.button("Start 1v1"):
                    st.session_state.footdle_win_message = None
                    player_df = get_players()
                    st.session_state.footdle_player_df = player_df
                    secret_row = player_df.sample(1).iloc[0]
                    st.session_state.footdle_secret = secret_row.to_dict()
                    st.session_state.footdle_guesses = []
                    st.session_state.footdle_bot_possible = player_df.copy()
                    st.session_state.footdle_bot_guesses = []
                    st.session_state.footdle_started = True
                    st.rerun()

            st.markdown("---")
            st.markdown("### 🤖 Difficulty Levels Explained")
            st.markdown("""
            Choosing a difficulty determines how accurate the bot's guesses are. Here's how it works:

            - 🟢 **Noob** – **100% random**: The bot guesses completely randomly.  
            - 🟡 **Easy** – **50% noise**: Half of its guesses are wrong, even if it knows better.  
            - 🟠 **Medium** – **25% noise**: Decent logic, but still makes 1 in 4 guesses incorrectly.  
            - 🔴 **Hard** – **10% noise**: Very smart – only 1 in 10 guesses are contaminated.  
            - ⚫ **Impossible** – **0% noise**: Perfect logic. The bot only guesses when it's certain.
            """)
            st.markdown(
                "<sub> *Note:* **Noise** means how often the bot includes misleading players in its guess pool, making it harder for it to win.</sub>",
                unsafe_allow_html=True
            )

            st.stop()


        
        player_df = st.session_state.footdle_player_df
        player_names = sorted(player_df["Name"].tolist())


        col_drop, col_guess,col_restart = st.columns([4, 1, 1])
        with col_drop:
            guess = st.selectbox("Type or pick a player's name:", [""] + player_names, key="footdle_select_computer")


        with col_guess:
            st.markdown("<div style='margin-top: 32px;'>", unsafe_allow_html=True)
            if st.button("Guess"):
                st.session_state.footdle_win_message = None

                if guess and guess not in st.session_state.footdle_guesses and not st.session_state.footdle_win_message and st.session_state.footdle_started:

                    st.session_state.footdle_guesses.append(guess)
                    secret = st.session_state.footdle_secret

                    user_correct = guess == secret["Name"]
                    bot_correct = False
                    bot_guess = None

                    difficulty = st.session_state.get("footdle_difficulty", "Medium")
                    contamination_map = {
                        "Noob": 100,
                        "Easy": 50,
                        "Medium": 25,
                        "Hard": 10,
                        "Impossible": 0
                    }
                    contam_percent = contamination_map.get(difficulty, 25)

                    if difficulty == "Noob":
                        all_unguessed = player_df[~player_df["Name"].isin(st.session_state.footdle_bot_guesses)]
                        if not all_unguessed.empty:
                            bot_guess_row = all_unguessed.sample(1).iloc[0]
                            bot_guess = bot_guess_row["Name"]
                            st.session_state.footdle_bot_guesses.append(bot_guess)
                            bot_correct = bot_guess == secret["Name"]
                    else:
                        if st.session_state.footdle_bot_possible is None or len(st.session_state.footdle_bot_guesses) == 0:
                            bot_possible = player_df.copy()
                        else:
                            bot_possible = st.session_state.footdle_bot_possible.copy()

                        bot_possible = bot_possible[~bot_possible["Name"].isin(st.session_state.footdle_bot_guesses)]

                        if len(st.session_state.footdle_bot_guesses) > 0:
                            last_bot_guess_row = player_df[player_df["Name"] == st.session_state.footdle_bot_guesses[-1]].iloc[0]
                            feedback = {
                                "Position": last_bot_guess_row["Position"] == secret["Position"],
                                "Age": last_bot_guess_row["Age"] == secret["Age"],
                                "Country": last_bot_guess_row["Country"] == secret["Country"],
                                "Club": last_bot_guess_row["Club"] == secret["Club"],
                                "League": last_bot_guess_row["League"] == secret["League"],
                                "Market Value (€ mil.)": last_bot_guess_row["Market Value (€ mil.)"] == secret["Market Value (€ mil.)"]
                            }
                            for col, is_correct in feedback.items():
                                if is_correct:
                                    bot_possible = bot_possible[bot_possible[col] == secret[col]]

                        if contam_percent > 0:
                            n_extra = max(1, int((contam_percent / 100) * len(bot_possible)))
                            all_names = set(player_df["Name"])
                            current_possible_names = set(bot_possible["Name"])
                            already_guessed = set(st.session_state.footdle_bot_guesses)
                            excluded_names = current_possible_names | already_guessed
                            false_positives_df = player_df[~player_df["Name"].isin(excluded_names)]
                            if not false_positives_df.empty:
                                add_df = false_positives_df.sample(n=min(n_extra, len(false_positives_df)))
                                bot_possible = pd.concat([bot_possible, add_df], ignore_index=True)

                        bot_possible = bot_possible.drop_duplicates(subset="Name").reset_index(drop=True)
                        if len(bot_possible) > 0:
                            bot_guess_row = bot_possible.sample(1).iloc[0]
                            bot_guess = bot_guess_row["Name"]
                            st.session_state.footdle_bot_guesses.append(bot_guess)
                            st.session_state.footdle_bot_possible = bot_possible
                            bot_correct = bot_guess == secret["Name"]

                    # === WIN OUTCOME CHECK ===
                    if user_correct and bot_correct:
                        st.session_state.footdle_win_message = "draw"
                    elif user_correct:
                        st.session_state.footdle_win_message = "user"
                    elif bot_correct:
                        st.session_state.footdle_win_message = "bot"

                    if st.session_state.footdle_win_message:
                        st.session_state.footdle_started = False

        with col_restart:
            st.markdown("<div style='margin-top: 32px;'>", unsafe_allow_html=True)
            if st.button("Restart"):
                st.session_state.footdle_started = False
                st.session_state.footdle_secret = None
                st.session_state.footdle_guesses = []
                st.session_state.footdle_bot_guesses = []
                st.session_state.footdle_bot_possible = None
                st.session_state.footdle_win_message = None
                st.rerun()

        # --- win/lose/draw message ---
        if st.session_state.footdle_win_message == "user":
            st.markdown(
                f"""
                <div style="width:100%;
                            margin-top: 10px;
                            background: #18b87a;
                            color: #fff;
                            font-size: 1.3em;
                            padding: 18px 0;
                            border-radius: 12px;
                            font-weight: bold;
                            text-align: center;
                            letter-spacing: 0.01em;
                            box-shadow: 0 8px 32px rgba(0,0,0,0.13);">
                    🎉 YOU WIN! The player was: <span style="color:#fff700">{st.session_state.footdle_secret['Name']}</span><br>
                    <span style="font-size:0.85em; color:#eeeeee; font-weight:normal;">
                        Try another round or check the player’s stats!
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif st.session_state.footdle_win_message == "bot":
            st.markdown(
                f"""
                <div style="width:100%;
                            margin-top: 10px;
                            background: #d53c1c;
                            color: #fff;
                            font-size: 1.3em;
                            padding: 18px 0;
                            border-radius: 12px;
                            font-weight: bold;
                            text-align: center;
                            letter-spacing: 0.01em;
                            box-shadow: 0 8px 32px rgba(0,0,0,0.13);">
                    🤖 THE COMPUTER WINS! The player was: <span style="color:#fff700">{st.session_state.footdle_secret['Name']}</span><br>
                    <span style="font-size:0.85em; color:#eeeeee; font-weight:normal;">
                        Try again or try Solo mode!
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif st.session_state.footdle_win_message == "draw":
            st.markdown(
                f"""
                <div style="width:100%;
                            margin-top: 10px;
                            background: #ff9f1c;
                            color: #fff;
                            font-size: 1.3em;
                            padding: 18px 0;
                            border-radius: 12px;
                            font-weight: bold;
                            text-align: center;
                            letter-spacing: 0.01em;
                            box-shadow: 0 8px 32px rgba(0,0,0,0.13);">
                    🤝 IT'S A DRAW! Both guessed: <span style="color:#fff700">{st.session_state.footdle_secret['Name']}</span><br>
                    <span style="font-size:0.85em; color:#eeeeee; font-weight:normal;">
                        That was intense. Want to go again?
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # --- game progress ---
        coly, colc = st.columns([7, 1])
        with coly:
            st.markdown("**Your Guess**")
        with colc:
            st.markdown("**Bot's Guess**")

        for i in reversed(range(len(st.session_state.footdle_guesses))):
            user_name = st.session_state.footdle_guesses[i]
            user_row = player_df[player_df["Name"] == user_name].iloc[0]
            secret = st.session_state.footdle_secret

            correct = {
                "Position": user_row["Position"] == secret["Position"],
                "Age": user_row["Age"] == secret["Age"],
                "Country": user_row["Country"] == secret["Country"],
                "Club": user_row["Club"] == secret["Club"],
                "League": user_row["League"] == secret["League"],
                "Market Value (€ mil.)": user_row["Market Value (€ mil.)"] == secret["Market Value (€ mil.)"]
            }
            values = {
                "Position": user_row["Position"],
                "Age": user_row["Age"],
                "Country": user_row["Country"],
                "Club": user_row["Club"],
                "League": user_row["League"],
                "Market Value (€ mil.)": user_row["Market Value (€ mil.)"]
            }
            def get_bg(col): return "#3dcc4a" if correct[col] else "#df2222"

            arrow_up_svg = """<svg width="18" height="18" style="vertical-align:middle;opacity:0.7;" viewBox="0 0 16 16"><path fill="black" d="M8 4l4 8H4z"/></svg>"""
            arrow_down_svg = """<svg width="18" height="18" style="vertical-align:middle;opacity:0.7;transform: rotate(180deg);" viewBox="0 0 16 16"><path fill="black" d="M8 4l4 8H4z"/></svg>"""

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

            bot_guess_str = ""
            if i < len(st.session_state.footdle_bot_guesses):
                bot_name = st.session_state.footdle_bot_guesses[i]
                bot_row = player_df[player_df["Name"] == bot_name].iloc[0]
                correct_bot = [
                    bot_row["Position"] == secret["Position"],
                    bot_row["Age"] == secret["Age"],
                    bot_row["Country"] == secret["Country"],
                    bot_row["Club"] == secret["Club"],
                    bot_row["League"] == secret["League"],
                    bot_row["Market Value (€ mil.)"] == secret["Market Value (€ mil.)"]
                ]
                n_correct = sum(correct_bot)
                bot_guess_str = f"<div style='font-weight:bold;color:#0078ff;padding-right:50px;font-size:1.1em;'>{bot_name} ({n_correct}/6)</div>"

            html = f"""
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
            <div style="display:grid;grid-template-columns:120px repeat(6, 95px);gap:8px;align-items:center;">
                <div style="font-weight:bold;font-size:1.1em;padding-right:8px;">{user_name}</div>
                    <div style="border:4px solid black; background:{get_bg('Position')}; border-radius:7px; height:65px; display:flex; align-items:center; justify-content:center;text-align: center; font-size:1.2em;">
                        {values['Position']}
                        </div>
                        <div style="border:4px solid black;background:{get_bg('Age')}; border-radius:7px; height:65px;display:flex;align-items:center;justify-content:center;text-align: center;font-size:1.2em;">
                            <span>{values['Age']}</span>
                            <span style="margin-left:6px;">{arrow_html(values['Age'], secret['Age'], correct['Age'])}</span>
                        </div>
                        <div style="border:4px solid black;background:{get_bg('Country')}; border-radius:7px; height:65px;display:flex;align-items:center;justify-content:center;text-align: center;font-size:1.1em;">{values['Country']}</div>
                        <div style="border:4px solid black;background:{get_bg('Club')}; border-radius:7px; height:65px;display:flex;align-items:center;justify-content:center;text-align: center;font-size:1.1em;">{values['Club']}</div>
                        <div style="border:4px solid black;background:{get_bg('League')}; border-radius:7px; height:65px;display:flex;align-items:center;justify-content:center;text-align: center;font-size:1.1em;">{values['League']}</div>
                        <div style="border:4px solid black;background:{get_bg('Market Value (€ mil.)')}; border-radius:7px; height:65px;display:flex;align-items:center;justify-content:center;text-align: center;font-size:1.2em;">
                        <span>{values['Market Value (€ mil.)']}</span>
                        <span style="margin-left:6px;">{arrow_html(values['Market Value (€ mil.)'], secret['Market Value (€ mil.)'], correct['Market Value (€ mil.)'])}</span>
                    </div>
                    </div>
                <div style="min-width:180px;margin-left:30px;text-align:right;">{bot_guess_str}</div>
            </div>
            """
            st.markdown(f"""<div style='display: flex; justify-content: center;'>{html}</div>""", unsafe_allow_html=True)
