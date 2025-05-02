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
    schema = SportsDataIO 
    # TODO: Improve how to determine season year and if it's the postseason
    # st.write(year, type(year))
    records = get_teams()

    df = (
        pd.DataFrame.from_records(records)
    )

    return df

def get_games_by_date(df: pd.DataFrame, date: dt.date = None) -> pd.DataFrame:
    if date is None:
        date = dt.date.today()

    schema = SportsDataIO
    return df.pipe(
        lambda x: x[x[schema.Day].astype("datetime64[s]").dt.date == date]
    )

st.title("NBA Games")
today = dt.date.today()
all_games = get_data(today)

teams = get_teams_data()
# st.write(teams)

todays_games = get_games_by_date(all_games)

# st.write(todays_games)
active_games = todays_games.pipe(lambda x: x[x["Status"] == "Scheduled"])

# st.write(active_games)

# TODO: Get SeriesInfo for series wins/losses
# TODO: Scrape NBA logos from : https://www.nba.com/teams
# TODO: Look at SDI's Team Profile for team names and logos
#   Download all logos locally OR download them in cache
# TODO: Use team info from Teams table

col_width_pct = 35
remaining_width_pct = 100 - 2 * col_width_pct
cards = [Card.from_sportsdataio(game) for _, game in active_games.iterrows()]
for card in cards:
    cols = st.columns(
        [col_width_pct, remaining_width_pct, col_width_pct], 
        vertical_alignment="center",
        border=True
    )
    with cols[0]:
        team_id = card.away.sdi_team_id
        team_info = teams.pipe(lambda x: x[x["TeamID"] == team_id]).iloc[0]
        team_fmt = Team(**team_info)
        st.image(team_fmt.wiki_log_url)
        st.write(f"### {card.away.name}")
    with cols[1]:
        st.write("### @")
        st.write(f'On **{card.channel}** At **{card.time.strftime("%I:%M %p")}**')
    with cols[2]:
        team_id = card.home.sdi_team_id
        team_info = teams.pipe(lambda x: x[x["TeamID"] == team_id]).iloc[0]
        team_fmt = Team(**team_info)
        st.image(team_fmt.wiki_log_url)
        st.write(f"### {card.home.name}")

