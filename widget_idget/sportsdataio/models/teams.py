from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class Team(BaseModel):
    """
    A class representing a game with teams, date, time, and channel.
    """
    team_id: int = Field(default=None, alias="TeamID", strict=False)
    key: str = Field(default=None, alias="Key", strict=False)
    city: str = Field(default=None, alias="City", strict=False)
    name: str = Field(default=None, alias="Name")
    conference: str = Field(default=None, alias="Conference")
    wiki_log_url: str = Field(default=None, alias="WikipediaLogoUrl")
    sdi_global_team_id: int = Field(default=None, alias="GlobalTeamID")
    nba_team_id: int = Field(default=None, alias="NbaDotComTeamID")
    head_coach: str = Field(default=None, alias="HeadCoach")
    color_primary: str = Field(default=None, alias="PrimaryColor")
    color_secondary: Optional[str] = Field(default=None, alias="SecondaryColor")
    color_tertiary: Optional[str] = Field(default=None, alias="TertiaryColor")
    color_quaternary: Optional[str] = Field(default=None, alias="QuaternaryColor")

    @property
    def colors(self) -> None:
        colors = []
        color_properties = [
            self.color_primary, 
            self.color_secondary, 
            self.color_tertiary, 
            self.color_quaternary
        ]
        for color in color_properties:
            if color is None:
                break
            colors.append(color)
        
        return colors
