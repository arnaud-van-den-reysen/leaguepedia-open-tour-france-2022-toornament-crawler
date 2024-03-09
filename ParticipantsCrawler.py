import re
from bs4 import BeautifulSoup
import requests

def getNombrePageDeParticipant(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    nombrePageDeParticipant = 0
    for a in soup('a',class_="page"):
        nombrePageDeParticipant+=1
    return nombrePageDeParticipant

def getAllParticipantLink(url,nbPage):
    """
    return ['/fr/tournaments/7536630372811767808/participants/7595279654062268416/', '/fr/tournaments/7536630372811767808/participants/7595278873180643328/',...]
    """
    linkOfParticipant = []
    for i in range(1,nbPage+1):
        response = requests.get(url+"?page="+str(i))
        soup = BeautifulSoup(response.text, 'html.parser')
        for a in soup('a',href=re.compile("/fr/tournaments/.................../participants/.................../")):
            linkOfParticipant.append(a['href'])
    return linkOfParticipant

def getTeamNameAndPlayers(linkP,teams) : 
    listOfRosterTeam = []
    for i in linkP:
        response = requests.get("https://play.toornament.com"+i+"info") 
        soup = BeautifulSoup(response.text, 'html.parser')
        teamName = soup.find_all('h3',text=True)[0].get_text()
        if(teamName in teams):
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

def getParticipantsLeaguepediaFormat(url,teams):
    leString = getTeamNameAndPlayers(getAllParticipantLink(url,getNombrePageDeParticipant(url)),teams)
    txt = "{{Box|start}}\n"
    for team in leString:
        txt = txt+"{{TeamRoster|team="+team['teamName']+"\n"
        txt = txt+"|seed=\n"
        for i in team['players']:
            txt = txt+"|{{TeamRoster/Line|player="+i+"|flag=|role=}}\n"
        txt = txt+"}}\n"
        txt = txt+"{{Box|break}}\n"
    txt = txt+"{{Box|end}}\n"
    return txt