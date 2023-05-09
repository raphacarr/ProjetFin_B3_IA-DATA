import networkx as nx
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
data = pd.read_csv('ChampionsLeague22-23.csv', header=None)
data.drop([0, 2, 7], axis=1, inplace=True)
data.columns = ['Date', 'Home Team', 'Home Score', 'Away Team', 'Away Score']

past_matches = data.dropna()

# Ajoutez un titre pour le graphique suivant
st.title("Buts par équipe")

# Calculez le nombre de buts marqués par chaque équipe à domicile et à l'extérieur
home_goals = data.groupby('Home Team')['Home Score'].sum().reset_index()
away_goals = data.groupby('Away Team')['Away Score'].sum().reset_index()

# Fusionner les buts à domicile et à l'extérieur et calculer le total
home_goals.columns = ['Team', 'Goals']
away_goals.columns = ['Team', 'Goals']
total_goals = pd.concat([home_goals, away_goals], ignore_index=True)
total_goals = total_goals.groupby('Team')['Goals'].sum().reset_index()

# Trier les équipes par le nombre total de buts marqués
total_goals = total_goals.sort_values(by='Goals', ascending=False)

# Créer un graphique à barres
fig = plt.figure(figsize=(12, 6))
sns.barplot(x='Team', y='Goals', data=total_goals)
plt.xticks(rotation=90)
plt.title("Nombre de buts marqués par équipe")

# Afficher le graphique dans Streamlit
st.pyplot(fig)
