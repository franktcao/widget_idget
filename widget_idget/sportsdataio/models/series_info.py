
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class SeriesInfo(BaseModel):
    away_wins: int = Field(default=0, alias="AwayTeamWins", strict=False)
    home_wins: int = Field(default=0, alias="HomeTeamWins", strict=False)
    game: int = Field(default=1, alias = "GameNumber", strict=False)
    best_of: int = Field(default=7, alias="MaxLength", strict=False) 