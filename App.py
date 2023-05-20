import streamlit as st
import pandas as pd
import textwrap
import matplotlib.pyplot as plt
from DataTeam import get_team_stats, get_all_players
from DataPlayer import get_player_details, get_player_honours
from config import collection
st.set_page_config(page_title="Projet Final Data IA", page_icon="⚽", layout="wide")

##########################################################################################################
#                                                                                                        #
#                                         APPEL MONGO                                                    #
#                                                                                                        #
##########################################################################################################

@st.cache_data
def get_records_from_mongo():
    records = collection.find({}, {'_id': 0})
    dfStatsMongo = pd.DataFrame(list(records))
    return dfStatsMongo

##########################################################################################################
#                                                                                                        #
#                                         STREAMLIT                                                      #
#                                                                                                        #
##########################################################################################################


# Sidebar - Navigation
st.sidebar.title("Navigation")
page_selection = st.sidebar.radio("Go to", ["Home", "Analysis"])

# Sidebar - Affichage
st.sidebar.title("Affichage")
show_team_stats = st.sidebar.checkbox("Afficher les statistiques de l'équipe", value=False)
show_player_stats = st.sidebar.checkbox("Afficher les statistiques des joueurs de la ldc 2021-22", value=False)
show_player_stats_22_23 = st.sidebar.checkbox("Afficher les statistiques des joueurs sur la saison 2022-23", value=False)

# Fonction pour la page d'accueil
def home():
    st.title("Analyse de la performance du Real Madrid dans la Ligue des Champions UEFA")
    st.image("https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg", width=200)
    st.write("## Objectif du projet")
    st.write("""
    L'objectif de ce projet est d'analyser les performances du Real Madrid, une équipe de football de renommée mondiale, 
    dans la Ligue des champions de l'UEFA. Nous utiliserons des données de match et des statistiques de joueurs 
    pour mieux comprendre comment le Real Madrid se compare aux autres équipes dans la ligue. 
    Nous examinerons également les performances individuelles des joueurs du Real Madrid.
    """)
    
    st.write("## Méthodologie")
    st.write("""
    1. Collecte de données: Nous avons recueilli des données sur les matchs de la Ligue des champions de l'UEFA et les statistiques des joueurs à partir de diverses sources.
    2. Analyse des données: Nous avons analysé ces données pour obtenir des informations sur les performances de l'équipe et des joueurs.
    3. Visualisation des données: Nous avons utilisé divers graphiques pour visualiser nos résultats et faciliter leur compréhension.
    """)
    
    st.write("## A propos du Real Madrid")
    st.write("""
    Le Real Madrid Club de Fútbol, plus simplement connu sous le nom de Real Madrid, est un club de football professionnel espagnol 
    basé à Madrid. Fondé le 6 mars 1902, le Real Madrid est l'un des clubs les plus célèbres et les plus riches du monde. 
    Il a remporté un nombre record de titres de la Ligue des champions de l'UEFA et a été nommé Club du XXe siècle par la FIFA.
    """)
    
    
    # Ajout des informations sur Karim Benzema
    st.title("Karim Benzema")
    player_details = get_player_details("34146309")

    if player_details is not None:
        st.image(player_details['strCutout'], width=200)  # Image du joueur
        st.write("## Biographie")
        st.write(player_details['strDescriptionFR'])  # Biographie du joueur
        
        st.write("## Trophés remportés")
        player_honours = get_player_honours("34146309")
        if player_honours is not None:
            honour_strings = [f"        • {honour['strHonour']} ({honour['strSeason']})" for honour in player_honours]
            combined_honours = '\n'.join(honour_strings)
            wrapped_text = textwrap.fill(combined_honours, 50)
            st.write(wrapped_text)
    else:
        st.write("Désolé, aucune information n'a été trouvée pour ce joueur.")


# Fonction pour la page d'analyse
def analysis():


    ##########################################################################################################
    #                                                                                                        #
    #                                          DATAFRAME                                                     #
    #                                                                                                        #
    ##########################################################################################################

    #Statistiques de l'équipe importer via DataTeam
    champions_league_id = "4480" #id sur l'API de SportDB
    team_matches, win_percentages, average_goals_per_match = get_team_stats(champions_league_id)

    # Obtenez la liste de tous les joueurs de la Ligue des Champions
    champions_league_players = get_all_players(champions_league_id)
    
    dfStatsMongo = get_records_from_mongo()

    # Créez une liste des noms des joueurs de la Ligue des Champions
    if champions_league_players is not None:
        champions_league_player_names = [player["strPlayer"] for player in champions_league_players]
    else:
        champions_league_player_names = []

    # Créez un nouveau DataFrame contenant uniquement les joueurs qui participent à la Ligue des Champions 21-22
    dfStats = dfStatsMongo[dfStatsMongo["Joueur"].isin(champions_league_player_names)]

    # Convertir la colonne 'Buts' en un type numérique
    dfStatsMongo['Buts'] = pd.to_numeric(dfStats['Buts'], errors='coerce')
    dfStats['Buts'] = pd.to_numeric(dfStats['Buts'], errors='coerce')
    # Convertir la colonne 'Passes D.' en un type numérique
    dfStatsMongo['P.D.'] = pd.to_numeric(dfStats['P.D.'], errors='coerce')
    dfStats['P.D.'] = pd.to_numeric(dfStats['P.D.'], errors='coerce')
    
        # Préparez les données pour Streamlit
    data = {
        "Équipe": list(win_percentages.keys()),
        "Nombre de matchs joués": list(team_matches.values()),
        "% de victoire": list(win_percentages.values()),
        "Moy de but / matchs": list(average_goals_per_match.values()),
    }
    df = pd.DataFrame(data)

    ##########################################################################################################
    #                                                                                                        #
    #                                              STREAMLIT                                                 #
    #                                                                                                        #
    ##########################################################################################################
        
        # Condition pour afficher les statistiques de l'équipe
    if show_team_stats:
        st.title("UEFA Champions League 2021/2022 Statistics")
        st.dataframe(df)

    # Condition pour afficher les statistiques des joueurs
    if show_player_stats:
        st.write("# Statistiques des joueurs de la Ligue des Champions")
        st.dataframe(dfStats)
    
    # Affichez les statistiques des joueurs pour la saison 22-23
    if show_player_stats_22_23:
        st.write("# Statistiques des joueurs pour la saison 22-23")
        st.dataframe(dfStatsMongo) 

    #Story Telling

    real_madrid_wins = df[df['Équipe'] == 'Real Madrid']['% de victoire'].values[0]
    other_teams_wins = df[df['Équipe'] != 'Real Madrid']['% de victoire']

    plt.figure(figsize=(10, 6))
    plt.hist([real_madrid_wins, other_teams_wins], bins=20, alpha=0.5, label=['Real Madrid', 'Other Teams'])
    plt.legend(loc='upper right')
    plt.xlabel('% de victoire')
    plt.ylabel('Nombre d\'équipes')
    plt.title('Distribution des victoires du Real Madrid par rapport aux autres équipes')
    st.pyplot(plt)

    real_madrid_goals = df[df['Équipe'] == 'Real Madrid']['Moy de but / matchs'].values[0]
    other_teams_goals = df[df['Équipe'] != 'Real Madrid']['Moy de but / matchs']

    plt.figure(figsize=(10, 6))
    plt.hist([real_madrid_goals, other_teams_goals], bins=20, alpha=0.5, label=['Real Madrid', 'Other Teams'])
    plt.legend(loc='upper right')
    plt.xlabel('Moy de but / matchs')
    plt.ylabel('Nombre d\'équipes')
    plt.title('Buts moyens par match pour le Real Madrid par rapport aux autres équipes')
    st.pyplot(plt)

    real_madrid_players = dfStats[dfStats['Équipe'] == 'Real Madrid']
    top_scorers = real_madrid_players.nlargest(5, 'Buts')

    plt.figure(figsize=(10, 6))
    plt.barh(top_scorers['Joueur'], top_scorers['Buts'], color='skyblue')
    plt.xlabel('Nombre de buts')
    plt.ylabel('Joueur')
    plt.title('Top 5 des joueurs du Real Madrid avec le plus de buts')
    plt.gca().invert_yaxis()
    st.pyplot(plt)

    top_assist = real_madrid_players.nlargest(5, 'P.D.')

    plt.figure(figsize=(10, 6))
    plt.barh(top_assist['Joueur'], top_assist['P.D.'], color='skyblue')
    plt.xlabel('Nombre de passes décisives')
    plt.ylabel('Joueur')
    plt.title('Top 5 des joueurs du Real Madrid avec le plus de passes décisives')
    plt.gca().invert_yaxis()
    st.pyplot(plt)

    # Create color map
    colors = {True: 'blue', False: 'gray'}
    df['IsRealMadrid'] = df['Équipe'] == 'Real Madrid'

    fig, ax = plt.subplots(figsize=(14,8))

    # Create a scatter plot with varying bubble sizes. Use the 'Nombre de matchs joués' for the size of the bubbles.
    bubble = ax.scatter(df['Moy de but / matchs'], df['% de victoire'], s=df['Nombre de matchs joués']*10, 
                        c=df['IsRealMadrid'].apply(lambda x: colors[x]), alpha=0.6, edgecolors="w", linewidth=2)

    # Add labels to the bubbles
    for i, txt in enumerate(df['Équipe']):
        ax.annotate(txt, (df['Moy de but / matchs'].iat[i],df['% de victoire'].iat[i]))

    ax.set_xlabel("Moyenne de buts par match")
    ax.set_ylabel("Pourcentage de victoires")
    ax.set_title("Bulle représentant le nombre de matchs joués, le pourcentage de victoires et la moyenne de buts par match")

    # Show the plot
    plt.show()

# Choisissez la page en fonction de la sélection de la barre latérale
if page_selection == "Home":
    home()
elif page_selection == "Analysis":
    analysis()
