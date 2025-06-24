import datetime as dt
from typing import Optional
import pandas as pd
from pydantic import BaseModel

from widget_idget.sportsdataio.models.series_info import SeriesInfo

from .sportsdataio.models.games import Game as SdiGame


class Team(BaseModel):
    city: str
    name: str
    display_city: str
    display_name: str
    conference: Optional[str]
    standing: Optional[int] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    score: Optional[int] = None
    ties: Optional[int] = 0
    logo_url: Optional[str] = None
    division: Optional[str]= None
    sdi_team_id: Optional[int] = None

    @property
    def win_ratio(self) -> float: 
        wins = self.wins
        losses = self.losses
        ties = self.ties

        total_games = (wins + losses + ties)
        return wins / total_games if total_games > 0 else 0.0
    
    @classmethod
    def from_sportsdataio(cls, sr: pd.Series, is_away: bool = False) -> "Team":
        schema = SdiGame(**sr)
        # Set the default values for the team
        city = schema.home
        name = schema.home
        display_city = schema.home
        display_name = schema.home
        sdi_team_id = schema.home_id
        
        # Change values if the team is away
        if is_away:
            city = schema.away
            name = schema.away
            display_city = schema.away
            display_name = schema.away
            sdi_team_id = schema.away_id
        
        # TODO: Figure out where to get these fields
        conference = None
        standing = None
        wins = None
        losses = None
        score = None
        ties = None
        logo_url = None

        return cls(
            city = city,
            name = name,
            display_city = display_city,
            display_name = display_name,
            conference = conference,
            standing = standing,
            wins = wins,
            losses = losses,
            score = score,
            ties = ties,
            logo_url = logo_url,
            sdi_team_id = sdi_team_id,
        )

class Card(BaseModel):
    away: Team
    home: Team
    date: Optional[dt.date]
    time: Optional[dt.time]
    channel: Optional[str]
    series_info: Optional[SeriesInfo]


    @classmethod
    def from_sportsdataio(cls, sr: pd.Series) -> "Card":
        schema = SdiGame(**sr)
        away = Team.from_sportsdataio(sr, is_away = True)
        home = Team.from_sportsdataio(sr, is_away = False)
        series_info = SeriesInfo(**sr["SeriesInfo"])
        game_datetime = schema.game_datetime

        return cls(
            away = away,
            home = home,
            date = None if game_datetime is None else game_datetime.date(),
            time = None if game_datetime is None else game_datetime.time(),
            channel = schema.channel,
            series_info=series_info
        )