import re
from bs4 import BeautifulSoup
import requests

TournamentID = "5228116608680255488" #SEUL VARIABLE à MODIFIER
URL = "https://play.toornament.com/fr/tournaments/"+TournamentID

def getNombrePageDeParticipant(URL):
    response = requests.get(URL+"/participants/")
    soup = BeautifulSoup(response.text, 'html.parser')
    nombrePageDeParticipant = 0
    for a in soup('a',class_="page"):
        nombrePageDeParticipant+=1
    return nombrePageDeParticipant

def getAllParticipantLink(URL,nbPage):
    linkOfParticipant = []
    for i in range(1,nbPage+1):
        response = requests.get(URL+"/participants/?page="+str(i))
        soup = BeautifulSoup(response.text, 'html.parser')
        for a in soup('a',href=re.compile("/fr/tournaments/5228116608680255488/participants/.................../")):
            linkOfParticipant.append(a['href'])
    return linkOfParticipant

def getTeamNameAndPlayers(linkP) : 
    listOfRosterTeam = []
    for i in linkP:
        response = requests.get("https://play.toornament.com"+i+"info") 
        soup = BeautifulSoup(response.text, 'html.parser')
        teamName = soup.find_all('h3',text=True)[0].get_text()
        players = []
        for i in soup.find_all('div','text bold',text=True):
            players.append(re.sub("\n", "",i.get_text()).strip())
        listOfRosterTeam.append(
            {"teamName": teamName,
            "players": players})
    return listOfRosterTeam

def makeFileOfParticipants(data):
    f = open("participants.txt","w",encoding="utf-8")
    f.write("{{Box|start}}\n")
    for team in data:
        f.write("{{TeamRoster|team="+team['teamName']+"\n")
        f.write("|seed=\n")
        for i in team['players']:
            f.write("|{{TeamRoster/Line|player="+i+"|flag=|role=}}\n")
        f.write("}}\n")
        f.write("{{Box|break}}\n")
    f.write("{{Box|end}}\n")
    f.close()

leString = getTeamNameAndPlayers(getAllParticipantLink(URL,getNombrePageDeParticipant(URL)))
print(leString)
makeFileOfParticipants(leString)
