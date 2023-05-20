import requests

def get_player_details(player_id):
    url = f"https://www.thesportsdb.com/api/v1/json/3/lookupplayer.php?id={player_id}"
    response = requests.get(url)
    data = response.json()
    return data['players'][0] if 'players' in data and data['players'] is not None else None

def get_player_honours(player_id):
    url = f"https://www.thesportsdb.com/api/v1/json/3/lookuphonours.php?id={player_id}"
    response = requests.get(url)
    data = response.json()
    return data['honours'] if 'honours' in data and data['honours'] is not None else None
