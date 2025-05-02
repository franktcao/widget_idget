from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class Game(BaseModel):
    """
    A class representing a game with teams, date, time, and channel.
    """
    game_id: int = Field(default=None, alias="GameID", strict=False)
    away_id: int = Field(default=None, alias="AwayTeamID", strict=False)
    home_id: int = Field(default=None, alias="HomeTeamID", strict=False)
    away: str = Field(default=None, alias="AwayTeam")
    home: str = Field(default=None, alias="HomeTeam")
    game_datetime: Optional[datetime] = Field(default=None, alias="DateTime", strict=False, null=True)
    channel: Optional[str] = Field(default=None, alias="Channel", strict=False, null=True)