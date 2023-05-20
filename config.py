#IMPORT
from pymongo import MongoClient

# se connecter à la base de données MongoDB
url = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.2"
client = MongoClient(url)
db = client['Projet_Fin']
collection = db['StatsJoueurs']