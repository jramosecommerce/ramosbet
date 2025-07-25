import requests
from bs4 import BeautifulSoup

FAVORITE_LEAGUES = [
    "BRASILEIRÃO", "SÉRIE B", "LIBERTADORES", "SUL-AMERICANA",
    "LIGA DOS CAMPEÕES", "LIGA EUROPA", "LA LIGA", "SERIE A",
    "LIGUE 1", "EUROCOPA", "COPA AMÉRICA", "COPA DO BRASIL",
    "COPA DA ITÁLIA", "COPA DO MUNDO", "ELIMINATÓRIAS", "BUNDESLIGA", "TORNEIO BETANO"
]

def get_games_today(strategy="all"):
    url = "https://www.flashscore.com.br/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    games = []

    for match_div in soup.find_all("div", class_="event__match"):
        league = match_div.find_previous("div", class_="event__title--name")
        if not league:
            continue

        league_name = league.text.strip().upper()
        if strategy == "favorites" and league_name not in FAVORITE_LEAGUES:
            continue
        elif strategy == "mixed" and len(games) >= 15 and league_name not in FAVORITE_LEAGUES:
            continue

        home = match_div.find("div", class_="event__participant--home")
        away = match_div.find("div", class_="event__participant--away")
        time = match_div.find("div", class_="event__time")

        if home and away and time:
            games.append({
                "league": league_name.title(),
                "home": home.text.strip(),
                "away": away.text.strip(),
                "time": time.text.strip()
            })

    return games