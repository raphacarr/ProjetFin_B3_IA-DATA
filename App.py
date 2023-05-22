import streamlit as st
import pandas as pd
import seaborn as sns
import textwrap
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from DataTeam import get_team_stats, get_all_players
from DataPlayer import get_player_details, get_player_honours
from Data import events_df_copie
from config import collection, collection2
st.set_page_config(page_title="Projet Final Data IA", page_icon="⚽", layout="wide")

##########################################################################################################
#                                                                                                        #
#                                         APPEL MONGO                                                    #
#                                                                                                        #
##########################################################################################################

@st.cache_data
def getMongoData():
    records = collection.find({}, {'_id': 0})
    dfStatsMongo = pd.DataFrame(list(records))
    return dfStatsMongo

@st.cache_data
def getMongoData2():
    records = collection2.find({}, {'_id': 0})
    dfJoueursDecisifsMongo = pd.DataFrame(list(records))
    return dfJoueursDecisifsMongo

##########################################################################################################
#                                                                                                        #
#                                         STREAMLIT                                                      #
#                                                                                                        #
##########################################################################################################

# Sidebar - Navigation
st.sidebar.title("Navigation")
page_selection = st.sidebar.radio("Go to", ["Accueil", "Analyses","Machine Learning Prediction"])

# Fonction pour la page d'accueil
def Accueil():
    st.title("L'excellence du Real Madrid dans le plus prestigieux des championnats")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg", width=200)  
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/fr/e/ef/UEFA_Ligue_des_Champions.svg", width=200)
        
    st.write("## Objectif du projet")
    st.write("""
    L'objectif de ce projet est d'analyser les performances du Real Madrid, une équipe de football de renommée mondiale, 
    dans la Ligue des champions de l'UEFA. Nous utiliserons des données de match et des statistiques de joueurs 
    pour mieux comprendre comment le Real Madrid se compare aux autres équipes dans la ligue. 
    Nous examinerons également les performances individuelles des joueurs du Real Madrid.
    De plus, nous créerons un model prédictif pour essayer de prédire des résultats de match éventuels.
    """)
    
    st.write("## Méthodologie")
    st.write("""
    Notre projet a suivi une méthodologie systématique qui assure une analyse exhaustive des performances du Real Madrid dans la Ligue des champions de l'UEFA. Voici les étapes que nous avons suivies :

    1. **Collecte des données** : Nous avons recueilli des données pertinentes concernant les matchs de la Ligue des champions de l'UEFA et les statistiques des joueurs du Real Madrid à partir de diverses sources de confiance.

    2. **Traitement des données** : Une fois les données collectées, nous les avons préparées pour l'analyse. Cela comprenait le nettoyage des données pour éliminer les erreurs ou les incohérences, ainsi que la transformation des données pour faciliter l'analyse.

    3. **Analyse des données** : Avec des données bien préparées, nous avons effectué une analyse exploratoire pour comprendre les tendances, les modèles et les relations entre différentes variables. 

    4. **Visualisation des données** : Nous avons utilisé divers outils de visualisation pour représenter graphiquement les résultats de notre analyse. Cela a rendu nos conclusions plus accessibles et faciles à comprendre.

    5. **Modélisation prédictive** : À partir de notre analyse, nous avons utilisé une régression linéaire pour construire un modèle prédictif. Ce modèle peut être utilisé pour prévoir des résultats sur des matchs, basées sur les données historiques.

    """)

    
    st.write("## A propos du Real Madrid")
    st.write("""
    Le Real Madrid Club de Fútbol, plus simplement connu sous le nom de Real Madrid, est un club de football professionnel espagnol 
    basé à Madrid. Fondé le 6 mars 1902, le Real Madrid est l'un des clubs les plus célèbres et les plus riches du monde. 
    Il a remporté un nombre record de titres de la Ligue des champions de l'UEFA et a été nommé Club du XXe siècle par la FIFA.
    """)
    
    
    # Ajout des informations sur Karim Benzema
    id_player = 34146309 #id récupéré sur TheSportsDB
    
    player_details = get_player_details(id_player)

    if player_details is not None:
        st.title(player_details['strPlayer'])
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
def Analyses():
    
    # Sidebar - Affichage
    st.sidebar.title("Affichage")
    show_stats_equipe = st.sidebar.checkbox("Afficher les statistiques de l'équipe", value=False)
    show_stats_joueurs_LDC = st.sidebar.checkbox("Afficher les statistiques des joueurs de la ldc 2021-22", value=False)
    show_stats_joueurs_22_23 = st.sidebar.checkbox("Afficher les statistiques des joueurs sur la saison 2022-23", value=False)
    show_joueurs_decisifs = st.sidebar.checkbox("Afficher les joueurs décisifs de la ldc 2021-22", value=False)

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
    
    dfStatsMongo = getMongoData()
    dfJoueursDecisifsMongo = getMongoData2()

    # Créez une liste des noms des joueurs de la Ligue des Champions
    if champions_league_players is not None:
        champions_league_player_names = [player["strPlayer"] for player in champions_league_players]
    else:
        champions_league_player_names = []

    # Créez un nouveau DataFrame contenant uniquement les joueurs qui participent à la Ligue des Champions 21-22
    dfStats = dfStatsMongo[dfStatsMongo["Joueur"].isin(champions_league_player_names)]
    # Compter le nombre de joueurs uniques dans chaque équipe
    player_counts = dfStats.groupby('Équipe')['Joueur'].nunique()

    # Filtrer les équipes qui ont plus d'un joueur
    dfStats = dfStats[dfStats['Équipe'].isin(player_counts[player_counts > 1].index)]

    # Convertir la colonne 'Buts' en un type numérique
    dfStatsMongo['Buts'] = pd.to_numeric(dfStats['Buts'], errors='coerce')
    dfStats['Buts'] = pd.to_numeric(dfStats['Buts'], errors='coerce')
    # Convertir la colonne 'Passes D.' en un type numérique
    dfStatsMongo['P.D.'] = pd.to_numeric(dfStats['P.D.'], errors='coerce')
    dfStats['P.D.'] = pd.to_numeric(dfStats['P.D.'], errors='coerce')
    
    # Préparation des données pour l'affichage
    data = {
        "Équipe": list(win_percentages.keys()),
        "Nombre de matchs joués": list(team_matches.values()),
        "% de victoire": list(win_percentages.values()),
        "Moy de but / matchs": list(average_goals_per_match.values()),
    }
    df = pd.DataFrame(data)
    
    # Charger les données du csv
    data = pd.read_csv('ChampionsLeague22-23.csv', header=None)
    data.drop([0, 2, 7], axis=1, inplace=True)
    data.columns = ['Date', 'Home Team', 'Home Score', 'Away Team', 'Away Score']

##########################################################################################################
#                                                                                                        #
#                                              STREAMLIT                                                 #
#                                                                                                        #
##########################################################################################################
        
    # Condition pour afficher les statistiques des équipes
    if show_stats_equipe:
        st.title("Statistiques des équipes de l'UEFA Champions League 2021/22 ")
        st.dataframe(df)

    # Condition pour afficher les statistiques des joueurs
    if show_stats_joueurs_LDC:
        st.write("# Statistiques des joueurs pendant la Ligue des Champions 2021/22")
        st.dataframe(dfStats)
    
    # Affichez les statistiques des joueurs pour la saison 22-23
    if show_stats_joueurs_22_23:
        st.write("# Statistiques des joueurs sur la saison 2022-23")
        st.dataframe(dfStatsMongo) 
        
    # Affichez les joueurs décisifs de la LDC 21-22
    if show_joueurs_decisifs:
        st.write("# Joueurs Décisifs de la League Des Champions 21-22")
        st.dataframe(dfJoueursDecisifsMongo) 

    #Story Telling
    
    st.title("Viualisations des données")
    
    st.subheader("Au football, le nombre de but marqué est l'une des choses les plus importantes, c'est cela que l'on retient à la fin d'un match.")
    st.subheader("Voici le nombre de but marqués pour chaques équipes au cours de la LDC 2021/22: ")
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

    fig = plt.figure(figsize=(12, 6))
    sns.barplot(x='Team', y='Goals', data=total_goals)
    plt.xticks(rotation=90)
    plt.title("Nombre de buts marqués par équipe durant la LDC 2021/22")

    st.pyplot(fig)
    
    st.subheader("Examinons maintenant la distribution des buts par joueur pour chaque équipe.")

    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Équipe', y='Buts', data=dfStats)
    plt.xticks(rotation=90)
    plt.title("Distribution des buts par joueur pour chaque équipe")
    st.pyplot(plt)

    st.title("Le Real Madrid dans la LDC")
    st.subheader("Une équipe des plus importante de la compétition, 14 fois victorieuse du titre et présente chaques années dans cette compétition prestigieuse.")
    
    #Focus sur le Réal
    st.subheader("Le Real, de superbes statistiques en LDC :")
    
    #Graphs %Victoires vs les autres équipes
    # Suppressions des équipes avec 0% de victoires
    df_filtrer = df[df['% de victoire'] > 0]
    # Tri les équipes par pourcentage de victoires
    df_trier = df_filtrer.sort_values(by='% de victoire', ascending=True)
    colors = ['red' if x == 'Real Madrid' else 'blue' for x in df_trier['Équipe']]

    plt.figure(figsize=(10, 10))
    plt.barh(df_trier['Équipe'], df_trier['% de victoire'], color=colors)
    plt.xlabel('% de victoire')
    plt.title('Pourcentage de victoires par équipe')
    st.pyplot(plt)
        
    real_madrid_goals = df[df['Équipe'] == 'Real Madrid']['Moy de but / matchs'].values[0]
    other_teams_goals = df[df['Équipe'] != 'Real Madrid']['Moy de but / matchs']
    #Graphs Buts/équipes
    plt.figure(figsize=(10, 6))
    plt.hist([real_madrid_goals, other_teams_goals], bins=20, alpha=0.5, label=['Real Madrid', 'Other Teams'])
    plt.legend(loc='upper right')
    plt.xlabel('Moy de but / matchs')
    plt.ylabel('Nombre d\'équipes')
    plt.title('Buts moyens par match pour le Real Madrid par rapport aux autres équipes')
    st.pyplot(plt)
    
    
    st.subheader("Le Real possède de grands joueurs avec de belles stats :")
    real_madrid_players = dfStats[dfStats['Équipe'] == 'Real Madrid']
    top_scorers = real_madrid_players.nlargest(5, 'Buts')
    #Graphs buts/Joueurs
    plt.figure(figsize=(10, 6))
    plt.barh(top_scorers['Joueur'], top_scorers['Buts'], color='skyblue')
    plt.xlabel('Nombre de buts')
    plt.ylabel('Joueur')
    plt.title('Top 5 des joueurs du Real Madrid avec le plus de buts')
    plt.gca().invert_yaxis()
    st.pyplot(plt)

    top_assist = real_madrid_players.nlargest(5, 'P.D.')
    #Graphs passesD/Joueurs
    plt.figure(figsize=(10, 6))
    plt.barh(top_assist['Joueur'], top_assist['P.D.'], color='skyblue')
    plt.xlabel('Nombre de passes décisives')
    plt.ylabel('Joueur')
    plt.title('Top 5 des joueurs du Real Madrid avec le plus de passes décisives')
    plt.gca().invert_yaxis()
    st.pyplot(plt)
    
    dfJoueursDecisifsMongo['B+PD'] = pd.to_numeric(dfJoueursDecisifsMongo['B+PD'], errors='coerce')
    top_decisive_players = dfJoueursDecisifsMongo.nlargest(10, 'B+PD') 
    # Top Joueurs buts passes d
    plt.figure(figsize=(10, 6))
    plt.barh(top_decisive_players['Joueur'], top_decisive_players['B+PD'], color='skyblue')
    plt.xlabel('Nombre total de Buts et Passes Décisives')
    plt.ylabel('Joueur')
    plt.title('Top 10 des Joueurs Décisifs de la LDC 21-22')
    plt.gca().invert_yaxis()

    st.pyplot(plt)
    
# Fonction pour la page de prédiction Machine Learning
def machine_learning():
    st.title("Prédiction Machine Learning")
    
    prediction = pd.DataFrame(events_df_copie)

    #Todo: Premiere partie sur les prediction 2021-2023
    # Liste des équipes à afficher
    equipes_a_afficher = ['Paris SG', 'Sporting CP', 'Inter', 'Bayern Munich', 'Chelsea', 'Lille', 'Juventus', 'Benfica', 'Ajax', 'Ath Madrid', 'Man United', 'SV Salzburg', 'Man City', 'Liverpool', 'Real Madrid', 'Villarreal']

    # Filtrer le dataframe pour inclure uniquement les rencontres des équipes spécifiées
    filtered_data_pred = prediction[prediction['Home Team'].isin(equipes_a_afficher) | prediction['Away Team'].isin(equipes_a_afficher)]

    # Création de l'application Streamlit
    st.subheader("Prédictions de but des équipes sélectionnées")

    # Filtre pour chaque rencontre
    rencontres = filtered_data_pred['Event Name'].unique()
    selected_rencontre = st.selectbox("Sélectionnez une rencontre", rencontres)

    # Filtrer le dataframe en fonction de la rencontre sélectionnée
    filtered_rencontre_data = filtered_data_pred[filtered_data_pred['Event Name'] == selected_rencontre]

    # Création du diagramme à partir des prédictions de score à domicile et à l'extérieur pour la rencontre sélectionnée
    fig, ax = plt.subplots(figsize=(8, 6))
    bar1 = ax.bar(['Home'], [filtered_rencontre_data['Predicted Home Score'].values[0]], label='Prédiction équipe domicile', color='blue')
    bar2 = ax.bar(['Away'], [filtered_rencontre_data['Predicted Away Score'].values[0]], label='Prédiction équipe extérieur', color='red')

    # Affichage des valeurs exactes à côté de chaque barre
    for rect in bar1:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')
    for rect in bar2:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')

    ax.set_xlabel('Type de score')
    ax.set_ylabel('Score prédit')
    ax.set_title('Prédictions du score pour la rencontre')
    ax.legend()
    st.pyplot(fig)

    # Données du tableau

    statEquipe = pd.DataFrame(columns=['Equipe', 'Moyenne but marque', 'Moyenne but concede'])
    statEquipe.loc[0] = [equipes_a_afficher[0], 1.87, 1.37]
    statEquipe.loc[1] = [equipes_a_afficher[1], 0.67, 1.67]
    statEquipe.loc[2] = [equipes_a_afficher[2], 1.13, 0.87]
    statEquipe.loc[3] = [equipes_a_afficher[3], 3, 0.7]
    statEquipe.loc[4] = [equipes_a_afficher[4], 2.03, 0.97]
    statEquipe.loc[5] = [equipes_a_afficher[5], 1, 1]
    statEquipe.loc[6] = [equipes_a_afficher[6], 1.37, 1.13]
    statEquipe.loc[7] = [equipes_a_afficher[7], 1.3, 1.6]
    statEquipe.loc[8] = [equipes_a_afficher[8], 2.62, 0.87]
    statEquipe.loc[9] = [equipes_a_afficher[9], 0.9, 1]
    statEquipe.loc[10] = [equipes_a_afficher[10], 1.5, 1.2]
    statEquipe.loc[11] = [equipes_a_afficher[11], 1.25, 1.75]
    statEquipe.loc[12] = [equipes_a_afficher[12], 2.27, 1.22]
    statEquipe.loc[13] = [equipes_a_afficher[13], 2.15, 1.08]
    statEquipe.loc[14] = [equipes_a_afficher[14], 2.05, 1.02]
    statEquipe.loc[15] = [equipes_a_afficher[15], 1.67, 1.25]

    # Création du dataframe
    df = pd.DataFrame(statEquipe)

    # Séparation des variables indépendantes (X) et de la variable cible (y)
    X = df[['Moyenne but marque', 'Moyenne but concede']]
    y = df['Equipe']

    # Création du modèle de régression logistique
    model = LogisticRegression()
    model.fit(X, y)

    # Interface Streamlit
    st.title("Prédiction du résultat du match")
    st.write("Sélectionnez les équipes pour comparer le résultat du match")

    # Sélection des équipes à comparer
    equipe1 = st.selectbox("Equipe 1", df['Equipe'])
    equipe2 = st.selectbox("Equipe 2", df['Equipe'])

    # Obtention des moyennes des buts marqués et concédés pour chaque équipe sélectionnée
    moyenne_but_marque_equipe1 = df[df['Equipe'] == equipe1]['Moyenne but marque'].values[0]
    moyenne_but_concede_equipe1 = df[df['Equipe'] == equipe1]['Moyenne but concede'].values[0]

    moyenne_but_marque_equipe2 = df[df['Equipe'] == equipe2]['Moyenne but marque'].values[0]
    moyenne_but_concede_equipe2 = df[df['Equipe'] == equipe2]['Moyenne but concede'].values[0]

    # Prédiction du résultat du match entre les deux équipes
    equipe1_pred = model.predict([[moyenne_but_marque_equipe1, moyenne_but_concede_equipe1]])
    equipe2_pred = model.predict([[moyenne_but_marque_equipe2, moyenne_but_concede_equipe2]])

    # Affichage du résultat
    st.write("Résultat du match :")
    if equipe1_pred[0] == equipe2_pred[0]:
        st.write("Match nul")
    else:
        if equipe1_pred[0] == equipe1:
            st.write(f"{equipe1} gagne contre {equipe2}")
        else:
            st.write(f"{equipe2} gagne contre {equipe1}")
        

if page_selection == "Accueil":
    Accueil()
elif page_selection == "Analyses":
    Analyses()
elif page_selection == "Machine Learning Prediction":
    machine_learning()
