from packages import st, pd, px
from scrape import get_players

def show_players_page():
    st.title("Top 100 Most Valuable Players")
    df = get_players()
    st.dataframe(df, hide_index=True)

    st.markdown("### 📊 Player Demographics & Value Insights")

    league_counts = df["League"].value_counts().reset_index()
    league_counts.columns = ["League", "Count"]
    fig_league = px.pie(
        league_counts,
        names="League",
        values="Count",
        title="🏆 League Distribution",
        hole=0.4
    )
    st.plotly_chart(fig_league, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_age = px.histogram(
            df,
            x="Age",
            nbins=10,
            title="Age Distribution",
            color_discrete_sequence=["#1be7b7"]
        )
        st.plotly_chart(fig_age, use_container_width=True)
    with col2:
        fig_value_hist = px.histogram(
            df,
            x="Market Value (€ mil.)",
            nbins=15,
            title="Market Value Distribution",
            color_discrete_sequence=["#ffa600"]
        )
        st.plotly_chart(fig_value_hist, use_container_width=True)

    leagues = sorted(df["League"].unique())
    selected_league_for_pies = st.selectbox("Select a League", ["All"] + leagues, key="pie_league_filter")
    if selected_league_for_pies != "All":
        league_df = df[df["League"] == selected_league_for_pies]
    else:
        league_df = df

    col1, col2 = st.columns([3,2])
    with col1:
        club_counts = league_df["Club"].value_counts().reset_index()
        club_counts.columns = ["Club", "Count"]
        fig_club_pie = px.pie(
            club_counts,
            names="Club",
            values="Count",
            title=f"Club Distribution – {selected_league_for_pies}",
            hole=0.3
        )
        fig_club_pie.update_traces(
        textinfo="percent",
        textposition="inside",
        insidetextorientation="radial",
        pull=[0.05 if count < club_counts["Count"].max() * 0.1 else 0 for count in club_counts["Count"]],
        textfont=dict(size=12)
        )
        st.plotly_chart(fig_club_pie, use_container_width=True)

    with col2:
        position_counts = league_df["Position"].value_counts().reset_index()
        position_counts.columns = ["Position", "Count"]
        fig_position_pie = px.pie(
            position_counts,
            names="Position",
            values="Count",
            title=f"Position Distribution – {selected_league_for_pies}",
            hole=0.3
        )
        fig_position_pie.update_traces(
        textinfo="percent",
        textposition="inside",
        insidetextorientation="radial",
        pull=[0.05 if count < position_counts["Count"].max() * 0.1 else 0 for count in position_counts["Count"]],
        textfont=dict(size=10)
        )
        st.plotly_chart(fig_position_pie, use_container_width=True)




    st.markdown("---")
    st.markdown("### 📌 Position Abbreviations Explained")
    st.markdown("""
    Football positions are shown using standard abbreviations. Here's what each one means:

    - **GK**: Goalkeeper  
    - **LB**: Left-Back  
    - **RB**: Right-Back  
    - **CB**: Centre-Back  
    - **CDM**: Defensive Midfield  
    - **CM**: Central Midfield  
    - **CAM**: Attacking Midfield  
    - **LW**: Left Winger  
    - **RW**: Right Winger  
    - **ST**: Centre-Forward (Striker)  
    - **CF**: Second Striker  
    """)