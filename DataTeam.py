import requests
import pandas as pd
from collections import defaultdict

api_key = "60130162"

# Obtenez la liste des équipes participantes
def get_participating_teams(league_id):
    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/lookup_all_teams.php?id={league_id}"
    response = requests.get(url)
    response_json = response.json()
    if response_json is None:
        return []
    teams = response_json.get("teams", [])
    return teams

# Obtenez les événements (matchs) de la ligue
def get_league_events(league_id):
    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/eventsseason.php?id={league_id}&s=2021-2022"
    response = requests.get(url)
    events = response.json()["events"]
    return events if events is not None else []

# Obtenez les résultats des matchs passés
def get_past_match_results(league_id):
    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/eventspastleague.php?id={league_id}"
    response = requests.get(url)
    past_results = response.json()["events"]
    return past_results if past_results is not None else []

champions_league_id = "4480"

teams = get_participating_teams(champions_league_id)
events = get_league_events(champions_league_id)
past_results = get_past_match_results(champions_league_id)

teams_df = pd.DataFrame(teams)
events_df = pd.DataFrame(events)
past_results_df = pd.DataFrame(past_results)

# Nettoyer les données des équipes
teams_df = teams_df[["idTeam", "strTeam", "strTeamBadge"]]
teams_df.columns = ["Team ID", "Team Name", "Team Badge"]

# Nettoyer les données des événements (matchs)
events_df = events_df[["idEvent", "strEvent", "dateEvent", "idHomeTeam", "idAwayTeam", "intHomeScore", "intAwayScore"]]
events_df.columns = ["Event ID", "Event Name", "Event Date", "Home Team ID", "Away Team ID", "Home Score", "Away Score"]

# Nettoyer les données des résultats des matchs passés
past_results_df = past_results_df[["idEvent", "strEvent", "dateEvent", "idHomeTeam", "idAwayTeam", "intHomeScore", "intAwayScore"]]
past_results_df.columns = ["Event ID", "Event Name", "Event Date", "Home Team ID", "Away Team ID", "Home Score", "Away Score"]

def process_events(events, past_results):
    team_matches = defaultdict(int)
    team_wins = defaultdict(int)
    team_goals = defaultdict(int)

    for event in events + past_results:
        home_team = event["strHomeTeam"]
        away_team = event["strAwayTeam"]
        home_goals = int(event["intHomeScore"]) if event["intHomeScore"] else 0
        away_goals = int(event["intAwayScore"]) if event["intAwayScore"] else 0

        # Mise à jour du nombre de matchs pour chaque équipe
        team_matches[home_team] += 1
        team_matches[away_team] += 1

        # Mise à jour du nombre de victoires pour chaque équipe
        if home_goals > away_goals:
            team_wins[home_team] += 1
        elif home_goals < away_goals:
            team_wins[away_team] += 1

        # Mise à jour du nombre de buts pour chaque équipe
        team_goals[home_team] += home_goals
        team_goals[away_team] += away_goals

    return team_matches, team_wins, team_goals

def get_team_stats(league_id):
    teams = get_participating_teams(league_id)
    events = get_league_events(league_id)
    past_results = get_past_match_results(league_id)
    
    team_matches, team_wins, team_goals = process_events(events, past_results)

    win_percentages = {team: (team_wins[team] / team_matches[team]) * 100 for team in team_matches}
    average_goals_per_match = {team: team_goals[team] / team_matches[team] for team in team_matches}

    return team_matches, win_percentages, average_goals_per_match

def get_team_players(team_id):
    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/lookup_all_players.php?id={team_id}"
    response = requests.get(url)
    players = response.json().get("player")
    return [] if players is None else players

def get_all_players(league_id):
    teams = get_participating_teams(league_id)
    all_players = []
    
    for team in teams:
        team_id = team["idTeam"]
        players = get_team_players(team_id)
        
        # Ajouter l'information de l'équipe à chaque joueur pour garder une trace de leur équipe
        for player in players:
            player["team"] = team["strTeam"]
        
        all_players.extend(players)
    
    return all_players
