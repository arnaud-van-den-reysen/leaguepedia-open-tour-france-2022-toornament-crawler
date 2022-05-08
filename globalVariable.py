import re
from bs4 import BeautifulSoup
import requests

def getParticipantsURLFromInfoURL(url):
    return url+"participants/"

def getRankingURLFromInfoURL(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    t = soup.find_all(href=re.compile("/fr/tournaments/.................../stages/.................../"))
    r2 = requests.get("https://play.toornament.com"+t[0]['href'])
    s2 = BeautifulSoup(r2.text, 'html.parser')
    t2 = s2.find_all(href=re.compile("/fr/tournaments/.................../stages/.................../groups/..................."))
    return "https://play.toornament.com"+t2[0]['href']

#URL du Round
URLROUND = "https://play.toornament.com/fr/tournaments/5301558561649655808/stages/5301560148115054592/groups/5301560148987469957/rounds/5660935038566301696/"
#DATE DU MATCH
DATE = "2022-05-07" 
#HEURE DU MATCH (|timezone=CET |dst=spring)
TIME = "17:00" 
#FALSE si les scores sont tombés, TRUE si pas de scores
SCORE = False