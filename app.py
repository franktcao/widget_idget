import datetime as dt
import streamlit as st
import pandas as pd
import pandera as pa

from widget_idget.sportsdataio.models.teams import Team
from widget_idget.sportsdataio.response import get_games, get_teams
from widget_idget.ui import Card

class SportsDataIO(pa.DataFrameModel):
    Day: pa.typing.Series[dt.datetime] = pa.Field(  
        coerce=True,
        # checks=pa.Check.str_length(10, 10),
        description="Date of the game in YYYY-MM-DD format",
    )

@st.cache_data
def get_data(today: dt.datetime) -> pd.DataFrame:
    year = today.year
    schema = SportsDataIO 
    # TODO: Improve how to determine season year and if it's the postseason
    records = get_games(int(year), postseason=False)
    last_game = pd.DataFrame.from_records(records)[schema.Day].astype("datetime64[ns]").max()
    if pd.to_datetime(today) > last_game:
        records = get_games(year, postseason=True)

    df = (
        pd.DataFrame.from_records(records)
        .sort_values(by=schema.Day, ascending=False)
    )

    return df


@st.cache_data
def get_teams_data() -> pd.DataFrame:
    records = get_teams()

    df = (
        pd.DataFrame.from_records(records)
        .set_index("TeamID")
    )

    return df

def get_games_by_date(df: pd.DataFrame, date: dt.date = None) -> pd.DataFrame:
    if date is None:
        date = dt.date.today()

    schema = SportsDataIO
    return df.pipe(
        lambda x: x[x[schema.Day].astype("datetime64[s]").dt.date == date]
    )

def display_card(card: Card) -> None:
    cols = st.columns(
        [col_width_pct, remaining_width_pct, col_width_pct], 
        vertical_alignment="bottom",
        border=True
    )
    display_card_side(card, cols)
    display_card_separator(card, cols)
    display_card_side(card, cols, is_away=False)

def display_card_side(card: Card, cols: list[st.delta_generator], is_away: bool = True) -> None:
    i_col = 0 if is_away else 2
    side = card.away if is_away else card.home
    team_id = side.sdi_team_id
    team_info = teams.loc[team_id]
    team_fmt = Team(**team_info)
    team_name = side.name
    nba_id = team_fmt.nba_team_id
    # img_url = team_fmt.wiki_log_url
    img_url = f"https://cdn.nba.com/logos/nba/{nba_id}/primary/L/logo.svg"
    series_record = (
        f"{card.series_info.away_wins}-{card.series_info.home_wins}"
        if is_away 
        else f"{card.series_info.home_wins}-{card.series_info.away_wins}"
    )
    caption = f"""{team_name}\n\n{series_record}"""
    with cols[i_col]:
        st.image(img_url, caption=caption, width=100, use_container_width=True)

def display_card_separator(card: Card, cols: list[st.delta_generator]) -> None:
    today = dt.date.today()
    day_name = today.strftime("%A")
    date = card.date
    date = f"Today, {day_name}" if date == today else f"{date.strftime('%A %b %d')}"
    channel = card.channel if card.channel else "*(TBD...)*"
    time_zone = "ET"
    with cols[1]:
        st.write("### @")
        st.write(f'**{date}** \n\non **{channel}** At **{card.time.strftime("%I:%M %p")} {time_zone}**')
        st.write(f'Best of **{card.series_info.best_of}**')

# Remove top margin
st.markdown("""
<style>
header.stAppHeader {
    background-color: transparent;
}
section.stMain .block-container {
    padding-top: 0rem;
    z-index: 1;
}
</style>""", unsafe_allow_html=True)
st.title("NBA Games")
today = dt.date.today()
all_games = get_data(today)

teams = get_teams_data()

todays_games = get_games_by_date(all_games)

# st.write(todays_games)
scheduled_games = (
    todays_games
    .pipe(lambda x: x[x["Status"] == "Scheduled"])
    .sort_values("DateTime")
    # .merge(teams, left_on="AwayTeamID", right_on="TeamID", how="left", suffixes=["", "_away"])
    # .merge(teams, left_on="HomeTeamID", right_on="TeamID", how="left", suffixes=["", "_home"])
)

# st.write(active_games)

# TODO: Merge `teams` onto `games`

st.write("# Today's Games")
col_width_pct = 35
remaining_width_pct = 100 - 2 * col_width_pct
cards = [Card.from_sportsdataio(game) for _, game in scheduled_games.iterrows()]
day_name = today.strftime("%A %B %d")
st.write(f"#### {day_name}")
for card in cards:
    display_card(card)

st.divider()

st.write("# Upcoming Games")
for i_day in range(1, 3):
    date = (dt.datetime.now() + dt.timedelta(days=i_day)).date()
    # st.write(f"## {date.weekday()}, {date}")
    day_name = date.strftime("%A")
    # st.write(f"#### {day_name} {date}")
    day_name = date.strftime("%A %B %d")
    st.write(f"#### {day_name}")
    games = (
        get_games_by_date(all_games, date=date)
        .pipe(lambda x: x[x["Status"] != "NotNecessary"])
        .sort_values("DateTime")
    )
    
    cards = [Card.from_sportsdataio(game) for _, game in games.iterrows()]
    for card in cards:
        display_card(card)

