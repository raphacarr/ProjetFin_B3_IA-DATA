import requests
import pandas as pd
from collections import defaultdict
#? Import pour le ML
from sklearn.preprocessing import OrdinalEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

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

# print("Équipes participantes:")
# print(teams_df)

# print("\nÉvénements (matchs):")
# print(events_df)

# print("\nRésultats des matchs passés:")
# print(past_results_df)

teams = get_participating_teams(champions_league_id)
events = get_league_events(champions_league_id)

team_matches = defaultdict(int)
team_wins = defaultdict(int)
team_goals = defaultdict(int)

for event in events:
    home_team = event["strHomeTeam"]
    away_team = event["strAwayTeam"]
    home_goals = int(event["intHomeScore"])
    away_goals = int(event["intAwayScore"])

    team_matches[home_team] += 1
    team_matches[away_team] += 1
    team_goals[home_team] += home_goals
    team_goals[away_team] += away_goals

    if home_goals > away_goals:
        team_wins[home_team] += 1
    elif home_goals < away_goals:
        team_wins[away_team] += 1

win_percentages = {team: (team_wins[team] / team_matches[team]) * 100 for team in team_matches}
average_goals_per_match = {team: team_goals[team] / team_matches[team] for team in team_matches}

# print("Pourcentage de victoires par équipe:")
# for team, win_percentage in win_percentages.items():
#     print(f"{team}: {win_percentage:.2f}%")

# print("\nNombre moyen de buts par match par équipe:")
# for team, avg_goals in average_goals_per_match.items():
#     print(f"{team}: {avg_goals:.2f}")
    
def process_events(events, past_results):
    team_matches = {}
    team_wins = {}
    team_goals = {}

    for event in events + past_results:
        home_team = event["strHomeTeam"]
        away_team = event["strAwayTeam"]
        home_goals = int(event["intHomeScore"]) if event["intHomeScore"] else 0
        away_goals = int(event["intAwayScore"]) if event["intAwayScore"] else 0

        # Mise à jour du nombre de matchs pour chaque équipe
        team_matches[home_team] = team_matches.get(home_team, 0) + 1
        team_matches[away_team] = team_matches.get(away_team, 0) + 1

        # Mise à jour du nombre de victoires pour chaque équipe
        if home_goals > away_goals:
            team_wins[home_team] = team_wins.get(home_team, 0) + 1
        elif home_goals < away_goals:
            team_wins[away_team] = team_wins.get(away_team, 0) + 1

        # Mise à jour du nombre de buts pour chaque équipe
        team_goals[home_team] = team_goals.get(home_team, 0) + home_goals
        team_goals[away_team] = team_goals.get(away_team, 0) + away_goals

    return team_matches, team_wins, team_goals

    
def get_team_stats(league_id):
    teams = get_participating_teams(league_id)
    events = get_league_events(league_id)
    past_results = get_past_match_results(league_id)
    
    team_matches, team_wins, team_goals = process_events(events, past_results)

    win_percentages = {team: (team_wins[team] / team_matches[team]) * 100 for team in team_matches}
    average_goals_per_match = {team: team_goals[team] / team_matches[team] for team in team_matches}

    return win_percentages, average_goals_per_match



#? Fonction qui permet de séparer un event team 
def separate_teams(event_name):
    foot = event_name.split(" vs ")
    if len(foot) == 2:
        home_team = foot[0]
        away_team = foot[1]
    else:
        home_team = ""
        away_team = ""
    return home_team, away_team

match_data = []
listTeam =[]
test = []

# Conversion des colonnes ID en int de base celle-ci sont de type object
teams_df['Team ID'] = teams_df['Team ID'].astype('int')
events_df['Home Team ID'] = events_df['Home Team ID'].astype('int')
events_df['Away Team ID'] = events_df['Away Team ID'].astype('int')

counter = 0
listEquipe = []

for index, row in events_df.iterrows():
    event_id = row["Event ID"]
    event_name = row["Event Name"]
    event_date = row["Event Date"]
    home_team_id = row["Home Team ID"]
    away_team_id = row["Away Team ID"]
    home_score = row["Home Score"]
    away_score = row["Away Score"]
    
    listEquipe.append(event_name)

# Créer une nouvelle colonne "Home Team" et "Away Team" dans le dataframe events_df
events_df['Home Team'] = [separate_teams(event_name)[0] for event_name in events_df['Event Name']]
events_df['Away Team'] = [separate_teams(event_name)[1] for event_name in events_df['Event Name']]

#! test machine learning
# Créer une copie du DataFrame
df_encoded = events_df.copy()

# Encoder les colonnes "Home Team" et "Away Team"
encoder = OrdinalEncoder()
df_encoded[["Home Team ID", "Away Team ID"]] = encoder.fit_transform(events_df[["Home Team", "Away Team"]])

# Sélectionner les caractéristiques et la cible
X = df_encoded[["Home Team ID", "Away Team ID"]]
y_home = df_encoded["Home Score"]
y_away = df_encoded["Away Score"]

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_home_train, y_home_test, y_away_train, y_away_test = train_test_split(X, y_home, y_away, test_size=0.2, random_state=42)

# Créer un modèle de régression linéaire pour Home Team
model_home = LinearRegression()
model_home.fit(X_train, y_home_train)

# Faire des prédictions sur les données de test pour Home Team
predictions_home = model_home.predict(X_test)

# Calculer l'erreur quadratique moyenne (RMSE) pour Home Team
rmse_home = mean_squared_error(y_home_test, predictions_home, squared=False)
#!print("RMSE for Home Team:", rmse_home)

# Créer un modèle de régression linéaire pour Away Team
model_away = LinearRegression()
model_away.fit(X_train, y_away_train)

# Faire des prédictions sur les données de test pour Away Team
predictions_away = model_away.predict(X_test)

# Calculer l'erreur quadratique moyenne (RMSE) pour Away Team
rmse_away = mean_squared_error(y_away_test, predictions_away, squared=False)
#!print("RMSE for Away Team:", rmse_away)

events_df_copie = events_df
event_df_encoded = events_df_copie.copy()
event_df_encoded[["Home Team ID", "Away Team ID"]] = encoder.transform(events_df_copie[["Home Team", "Away Team"]])
predictions_home = model_home.predict(event_df_encoded[["Home Team ID", "Away Team ID"]])
predictions_away = model_away.predict(event_df_encoded[["Home Team ID", "Away Team ID"]])

events_df_copie["Predicted Home Score"] = predictions_home
events_df_copie["Predicted Away Score"] = predictions_away


#!print(events_df_copy)