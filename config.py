import os
from datetime import timedelta

BASE_URL = "https://api.football-data.org/v4"
API_TOKEN = os.getenv("FOOTBALL_DATA_TOKEN", "c67e9f5362d54bcdb5042f6f3e2ec0c2")
REQUEST_TIMEOUT = 12
CACHE_TTL = timedelta(minutes=30)

TEAM_IDS = {
    "Manchester City": 65, "Liverpool": 64, "Paris Saint-Germain": 524, "Real Madrid": 86,
    "Chelsea": 61, "Arsenal": 57, "Brentford": 402, "Ipswich Town": 349, "Club Brugge": 851,
    "Nottingham Forest": 351, "Lille": 521, "PSV": 674, "Barcelona": 81, "Atlético Madrid": 78,
    "Inter Milan": 108, "Lazio": 110, "Angers SCO": 556, "Stade de Reims": 547,
    "Brighton & Hove Albion": 397, "Fulham": 63, "AFC Bournemouth": 1044,
    "Wolverhampton Wanderers": 76, "Crystal Palace": 354, "Aston Villa": 58,
    "Southampton": 340, "Bayern Munich": 5, "Benfica": 503, "Manchester United": 66,
    "Tottenham Hotspur": 73, "Juventus": 109, "AC Milan": 98, "Napoli": 113,
    "AS Roma": 100, "Borussia Dortmund": 4, "RB Leipzig": 721, "Porto": 497, "Ajax": 678,
    "Real Sociedad": 92, "Getafe": 82, "Newcastle United": 67, "Club Deportivo Leganés": 745,
    "Leicester City": 338, "Everton": 62, "West Ham United": 563, "Valencia": 95,
    "Sevilla": 559, "Bayer Leverkusen": 3, "Atalanta": 102, "Fiorentina": 99,
    "Sporting CP": 498, "Villarreal": 94
}