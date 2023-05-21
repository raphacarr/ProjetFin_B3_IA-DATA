##########################################################################################################
#                                                                                                        #
#                                              IMPORTS                                                   #
#                                                                                                        #
##########################################################################################################

from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import collection2

##########################################################################################################
#                                                                                                        #
#                                    BEAUTIFUL SOUP X SELENIUM                                           #
#                                                                                                        #
##########################################################################################################

url = "https://www.footmercato.net/europe/ligue-des-champions-uefa/2021-2022/decisif"

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.get(url)

# Accepter les cookies
cookie_accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#didomi-notice-agree-button")))
cookie_accept_button.click()

# Attente de la présence de l'élément HTML contenant le tableau des joueurs
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#mostDecisiveStandingsTables")))

# Récupération du tableau
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

headers = [header.text.strip() for header in soup.select("table#mostDecisiveStandingsTables th")]

rows = soup.select("table#mostDecisiveStandingsTables tr")
data = []

for row in rows[1:]:
    cells = [cell.text.strip() for cell in row.select("td")]
    player_name = row.select_one("span.personCardCell__name")
    if player_name:
        cells[1] = player_name.text.strip()
    data.append(cells)

df = pd.DataFrame(data, columns=headers)

print(df)

##########################################################################################################
#                                                                                                        #
#                                              MONGO DB                                                  #
#                                                                                                        #
##########################################################################################################

# Convertir le DataFrame en une liste de dictionnaires
player_list = df.to_dict('records')

# Insérer les documents dans la collection2 (dans le fichier config.py)
result = collection2.insert_many(player_list)

# Vérifiez si l'insertion a réussi
if result.acknowledged:
    print(f"Documents insérés avec succès.")
else:
    print("Échec de l'insertion des documents.")

# Supprimer les documents où la colonne "Joueur" est nulle
result = collection2.delete_many({"Joueur": None})

# Afficher le nombre de documents supprimés ou non
print(f"Nombre de valeurs nulles supprimées : {result.deleted_count}")
