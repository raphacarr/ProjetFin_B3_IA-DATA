import requests

api_key = "60130162"

# Obtenez la liste des équipes participantes
def get_participating_teams(league_id):
    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/lookup_all_teams.php?id={league_id}"
    response = requests.get(url)
    teams = response.json()["teams"]
    return teams

# Obtenez les événements (matchs) de la ligue
def get_league_events(league_id):
    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/eventsseason.php?id={league_id}&s=2021-2022"
    response = requests.get(url)
    events = response.json()["events"]
    return events

# Obtenez les résultats des matchs passés
def get_past_match_results(league_id):
    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/eventspastleague.php?id={league_id}"
    response = requests.get(url)
    past_results = response.json()["events"]
    return past_results

# Remplacez cette valeur par l'ID de la ligue des champions
champions_league_id = "4314"

teams = get_participating_teams(champions_league_id)
events = get_league_events(champions_league_id)
past_results = get_past_match_results(champions_league_id)

print("Équipes participantes:")
print(teams)

print("\nÉvénements (matchs):")
print(events)

print("\nRésultats des matchs passés:")
print(past_results)
