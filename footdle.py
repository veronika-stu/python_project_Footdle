from packages import st, pd
from scrape import get_players

def footdle_page():
    st.title("Footdle - Guess the Player!")
    # Mode selection state
    if "footdle_mode" not in st.session_state:
        st.session_state.footdle_mode = None

    # Mode select page
    if st.session_state.footdle_mode is None:
        st.markdown("""
        Welcome to **Footdle**!  
        - In **Solo** mode, guess the player in as few tries as possible.  
        - In **Against Computer** mode, you and the bot will compete to see who can guess first (coming soon)!  
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
        st.stop()

    # Mode back button
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
        # State setup
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

        # Start button
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
                if guess and guess not in st.session_state.footdle_guesses and not st.session_state.footdle_gave_up_message and st.session_state.footdle_started:
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

        # Give Up message block
        if st.session_state.footdle_gave_up_message:
            answer = secret["Name"] if secret else "unknown"
            st.markdown(
                f"""
                <div style="width:70vw;
                            margin-left: calc(-47vw + 50%);
                            margin-top: 20px;
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

        # Headers row
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

        # Guess grid and win logic
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

            # Win logic (but not after Give Up)
            if all(correct.values()) and not st.session_state.footdle_gave_up_message and st.session_state.footdle_started:
                st.session_state.footdle_win_message = True
                st.session_state.footdle_started = False
                break

        if st.session_state.get("footdle_win_message"):
            st.markdown(
                f"""
                <div style="width:70vw;
                            margin-left: calc(-20vw);
                            margin-top: 20px;
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
            if st.button("Start 1v1"):
                player_df = get_players()
                st.session_state.footdle_player_df = player_df
                secret_row = player_df.sample(1).iloc[0]
                st.session_state.footdle_secret = secret_row.to_dict()
                st.session_state.footdle_guesses = []
                st.session_state.footdle_bot_possible = player_df.copy()
                st.session_state.footdle_bot_guesses = []
                st.session_state.footdle_started = True
                st.rerun()
            st.stop()
        
        player_df = st.session_state.footdle_player_df
        player_names = sorted(player_df["Name"].tolist())

        col1, col2 = st.columns(2)
        user_win = False
        bot_win = False
        with col1:
            st.markdown("### Your turn")
            guess = st.selectbox("Your guess:", [""] + player_names, key="footdle_select_computer")
            if st.session_state.footdle_started:
                if st.button("Guess"):
                    if guess and guess not in st.session_state.footdle_guesses and not st.session_state.footdle_win_message:
                        # --- Add user guess ---
                        st.session_state.footdle_guesses.append(guess)
                        secret = st.session_state.footdle_secret

                        # --- Check if user wins
                        if guess == secret["Name"]:
                            st.session_state.footdle_win_message = "user"
                            st.session_state.footdle_started = False

                        # --- Bot's Turn: Guess using only its own past feedback
                        # 1. On first turn, bot_possible is all players
                        if st.session_state.footdle_bot_possible is None or len(st.session_state.footdle_bot_guesses) == 0:
                            bot_possible = player_df.copy()
                        else:
                            bot_possible = st.session_state.footdle_bot_possible.copy()

                        # 2. Remove already guessed
                        bot_possible = bot_possible[~bot_possible["Name"].isin(st.session_state.footdle_bot_guesses)]

                        # 3. Make a guess if possible, but "contaminate" possible set with 25% random wrong players
                        if len(bot_possible) > 0:
                            # Get feedback for bot's last guess if exists (bot is making next guess based on previous guess)
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
                                # Filter strictly
                                for col, is_correct in feedback.items():
                                    if is_correct:
                                        bot_possible = bot_possible[bot_possible[col] == secret[col]]

                            # Now contaminate the bot's pool
                            n_extra = max(1, int(0.25 * len(bot_possible)))
                            all_possible_names = set(player_df["Name"].tolist())
                            current_possible_names = set(bot_possible["Name"].tolist())
                            already_guessed = set(st.session_state.footdle_bot_guesses)
                            excluded_names = current_possible_names | already_guessed

                            false_positives_df = player_df[~player_df["Name"].isin(excluded_names)]
                            if len(false_positives_df) > 0:
                                add_df = false_positives_df.sample(n=min(n_extra, len(false_positives_df)))
                                bot_possible = pd.concat([bot_possible, add_df], ignore_index=True)

                            # Remove duplicates just in case
                            bot_possible = bot_possible.drop_duplicates(subset="Name").reset_index(drop=True)

                            # --- Pick random guess from contaminated pool
                            bot_guess_row = bot_possible.sample(1).iloc[0]
                            bot_guess = bot_guess_row["Name"]
                            st.session_state.footdle_bot_guesses.append(bot_guess)

                            # Store the contaminated pool for next round
                            st.session_state.footdle_bot_possible = bot_possible

                            # --- Bot win logic
                            if bot_guess == secret["Name"]:
                                st.session_state.footdle_win_message = "bot"
                                st.session_state.footdle_started = False


                # --- Display user guesses grid ---
                st.markdown("#### Your guesses")
                for guessed_name in reversed(st.session_state.footdle_guesses):
                    guess_row = player_df[player_df["Name"] == guessed_name].iloc[0]
                    secret = st.session_state.footdle_secret
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
                    html = f"""
                    <div style="display:grid;grid-template-columns:120px repeat(6, 70px);gap:8px;align-items:center;margin-bottom:4px;">
                        <div style="font-weight:bold;font-size:1.05em;">{guessed_name}</div>
                        <div style="background:{get_bg('Position')}; border-radius:7px; height:35px;display:flex;align-items:center;justify-content:center;">{values['Position']}</div>
                        <div style="background:{get_bg('Age')}; border-radius:7px; height:35px;display:flex;align-items:center;justify-content:center;">{values['Age']}</div>
                        <div style="background:{get_bg('Country')}; border-radius:7px; height:35px;display:flex;align-items:center;justify-content:center;">{values['Country']}</div>
                        <div style="background:{get_bg('Club')}; border-radius:7px; height:35px;display:flex;align-items:center;justify-content:center;">{values['Club']}</div>
                        <div style="background:{get_bg('League')}; border-radius:7px; height:35px;display:flex;align-items:center;justify-content:center;">{values['League']}</div>
                        <div style="background:{get_bg('Market Value (€ mil.)')}; border-radius:7px; height:35px;display:flex;align-items:center;justify-content:center;">{values['Market Value (€ mil.)']}</div>
                    </div>
                    """
                    st.markdown(html, unsafe_allow_html=True)

        with col2:
            st.markdown("### Computer guesses")
            st.markdown("#### Bot guesses")
            for bot_guess in reversed(st.session_state.footdle_bot_guesses):
                guess_row = player_df[player_df["Name"] == bot_guess].iloc[0]
                secret = st.session_state.footdle_secret
                correct = [
                    guess_row["Position"] == secret["Position"],
                    guess_row["Age"] == secret["Age"],
                    guess_row["Country"] == secret["Country"],
                    guess_row["Club"] == secret["Club"],
                    guess_row["League"] == secret["League"],
                    guess_row["Market Value (€ mil.)"] == secret["Market Value (€ mil.)"]
                ]
                n_correct = sum(correct)
                st.markdown(
                    f"<div style='font-weight:bold;font-size:1.1em;margin-bottom:7px;'>{bot_guess} <span style='color:#1be7b7;font-weight:normal;'>({n_correct}/6)</span></div>",
                    unsafe_allow_html=True
                )
        # --- WIN/LOSE MESSAGES ---
        if st.session_state.footdle_win_message == "user":
            st.markdown(
                f"""
                <div style="width:70vw;
                            margin-left: calc(-20vw);
                            margin-top: 20px;
                            background: #18b87a;
                            color: #fff;
                            font-size: 1.3em;
                            padding: 24px 0;
                            border-radius: 18px;
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
                <div style="width:70vw;
                            margin-left: calc(-20vw);
                            margin-top: 20px;
                            background: #d53c1c;
                            color: #fff;
                            font-size: 1.3em;
                            padding: 24px 0;
                            border-radius: 18px;
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