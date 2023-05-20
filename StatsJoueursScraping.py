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
import time
from config import collection

 ##########################################################################################################
 #                                                                                                        #
 #                                    BEAUTIFUL SOUP X SELENIUM                                           #
 #                                                                                                        #
 ##########################################################################################################

url = "https://www.footmercato.net/joueur/"

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.get(url)

# Attente de la présence de l'élément HTML contenant la pop-up des cookies
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#didomi-notice-agree-button")))

# Recherche du bouton d'acceptation des cookies et clic dessus
cookie_accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#didomi-notice-agree-button")))
cookie_accept_button.click()

# Attente de la présence du bouton de filtre des meilleurs buteurs
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-parameters='&tableView=stats&order[goals]=DESC']")))

# Recherche du bouton de filtre des meilleurs buteurs et clic dessus
best_scorers_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-parameters='&tableView=stats&order[goals]=DESC']")))
best_scorers_button.click()

# Attente de la présence de l'élément HTML contenant le tableau des joueurs
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#statsTable")))

# Attente de la présence du bouton "Afficher plus"
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.buttonDisplay--primary")))

max_clicks = 70
click_count = 0

while click_count < max_clicks:
    try:
        afficher_plus_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.buttonDisplay--primary")))
        afficher_plus_button.click()
        time.sleep(1)
        click_count += 1
    except:
        break

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

headers = [header.text.strip() for header in soup.select("table#statsTable th")]

rows = soup.select("table#statsTable tr")
data = []

for row in rows[1:]:
    cells = [cell.text.strip() for cell in row.select("td")]
    player_name = row.select_one("span.personCardCell__name")
    if player_name:
        cells[2] = player_name.text.strip()  # Mettre à jour la colonne "Joueurs" avec uniquement le nom des joueurs
    data.append(cells)

df = pd.DataFrame(data, columns=headers)

print(df)

##########################################################################################################
#                                                                                                        #
#                                              MONGO DB                                                  #
#                                                                                                        #
##########################################################################################################
 
# Convertissez le DataFrame en une liste de dictionnaires
player_list = df.to_dict('records')

# Insérez les documents (dictionnaires) dans la collection MongoDB
result = collection.insert_many(player_list)

# Vérifiez si l'insertion a réussi
if result.acknowledged:
    print(f"Documents insérés avec succès.")
else:
    print("Échec de l'insertion des documents.")

# Supprimer les documents où la colonne "Joueur" est nulle
result = collection.delete_many({"Joueur": None})

# Afficher le nombre de documents supprimés
print(f"Nombre de valeurs nulles supprimées : {result.deleted_count}")