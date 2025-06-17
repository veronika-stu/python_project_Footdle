from packages import st, pd
from scrape import get_players, get_wikipedia_image, POSITION_MAP, convert_market_value, CLUB_TO_LEAGUE
from footdle import footdle_page

# ----------------------------
# Sidebar Navigation
# ----------------------------
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

with st.sidebar:
    st.title("Navigation")
    if st.button("Home"):
        st.session_state.page = 'Home'
        st.rerun()
    if st.button("Player Info"):
        st.session_state.page = 'Player Info'
        st.rerun()
    if st.button('FootDle'):
        st.session_state.page = 'FootDle'
        st.rerun()
    if st.button("Players List"): 
        st.session_state.page = 'Players List'
        st.rerun()

# ----------------------------
# Home Page
# ----------------------------
if st.session_state.page == 'Home':
    st.title("Welcome to the Football App")
    st.markdown("---")
    st.markdown("""
        Welcome to the ultimate hub for football lovers!  
        Explore club stats, player profiles, or play our football-themed guessing game.
        Whether you're a die-hard fan or just curious about the beautiful game, there's something here for everyone.
        Use the navigation bar on the left or choose an option below to get started:
    """)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("View Player Info"):
            st.session_state.page = "Player Info"
            st.rerun()
    with col2:
        if st.button("Explore Players List"):
            st.session_state.page = "Players List"
            st.rerun()
    with col3:
        if st.button("Play FootDle"):
            st.session_state.page = "FootDle"
            st.rerun()

# ----------------------------
# Player Info Page
# ----------------------------
elif st.session_state.page == 'Player Info':
    st.title("Football Player Statistics")
    df = get_players()
    player_names = sorted(df["Name"].tolist())
    player_choice = st.selectbox("Choose a player:", player_names)
    player_row = df[df["Name"] == player_choice].iloc[0]
    REV_POSITION_MAP = {v: k for k, v in POSITION_MAP.items()}
    full_position = REV_POSITION_MAP.get(player_row["Position"], player_row["Position"])
    col1, col2 = st.columns([1, 2])
    with col1:
        img_url = get_wikipedia_image(player_choice)
        if img_url:
            st.image(img_url, width=220)
        else:
            st.write("No photo available.")
    with col2:
        st.markdown(f"**Name:** {player_row['Name']}")
        st.markdown(f"**Age:** {player_row['Age']}")
        st.markdown(f"**Club:** {player_row['Club']}")
        st.markdown(f"**League:** {player_row['League']}")
        st.markdown(f"**Country:** {player_row['Country']}")
        st.markdown(f"**Position:** {full_position}")
        st.markdown(f"**Market Value:** €{player_row['Market Value (€ mil.)']}m")

# ----------------------------
# Footdle Page 
# ----------------------------
elif st.session_state.page == 'FootDle':
    footdle_page()
  

# ----------------------------
# Players Page
# ----------------------------
elif st.session_state.page == 'Players List':
    st.title("Top 100 Most Valuable Players")
    df = get_players()
    st.dataframe(df, hide_index=True)
