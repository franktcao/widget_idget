import os 
import requests

from dotenv import load_dotenv
from urllib.parse import urlencode
from yarl import URL

load_dotenv()

import pydantic
from pydantic.dataclasses import dataclass

@dataclass
class SportsDataIoEndPoint:
    games = "Games"
    teams = "AllTeams"


def get_teams() -> dict:
    url = build_url(SportsDataIoEndPoint.teams)
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.text}; {url}")
    
    return response.json()


def get_games(year: int = 2025, postseason: bool = False) -> dict:
    season = str(year) + ("POST" if postseason else "")
    print(SportsDataIoEndPoint.games)
    url = build_url(SportsDataIoEndPoint.games, additional_params=season)
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.text}; {url}")
    
    return response.json()


def build_url(endpoint: str, *, additional_params: str = None) -> str:
    base_url = "https://api.sportsdata.io/v3/"
    league = "nba"
    dataset = "scores"
    format = "json"
    url = URL(base_url) / league / dataset / format / endpoint

    if additional_params:
        url /= additional_params

    params = {
        "key": os.getenv("SPORTSDATAIO_API_KEY")
    }

    return f"{url}?{urlencode(params)}"