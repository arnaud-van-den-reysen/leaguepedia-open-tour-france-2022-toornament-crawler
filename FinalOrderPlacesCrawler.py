from bs4 import BeautifulSoup
import requests

TournamentID = "5228116608680255488/stages/5228123532906905600/groups/5228123533913538693/" #SEUL VARIABLE à MODIFIER
URL = "https://play.toornament.com/fr/tournaments/"+TournamentID

def getNombrePageDeSwissGroup(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    nombrePageDeParticipant = 0
    for a in soup('a',class_="page"):
        nombrePageDeParticipant+=1
    return nombrePageDeParticipant

def getOrderAndPlaces(URL,nbPage):
    orderAndPlaces = []
    order = []
    places = []
    groupstage = []
    for i in range(1,nbPage+1):
        response = requests.get(URL+"?page="+str(i))
        soup = BeautifulSoup(response.text, 'html.parser')
        for j in soup.find_all('div',class_="rank large"):
            if j.get_text() != "#":
                places.append(j.get_text())
        for j in soup.find_all('div',class_="name weighted"):
            if j.get_text() != "Nom":
                order.append(j.get_text())
        for j in soup.find_all('div',class_="history history-6"):
            if j.get_text() != "Historique    ":
                groupstage.append(j.get_text())
    for i,j,k in zip(order,places,groupstage):
        orderAndPlaces.append(
            {'order': i,
            'places': j,
            'groupstage': k
            }
        )
    return orderAndPlaces

def makeFileOfFinalOrderPlaces(data):
    f = open("finalOrderPlaces.txt","w",encoding="utf-8")
    f.write("|finalorder=")
    for i in data:
        f.write(i['order']+',')
    f.write("\n")
    f.write("|finalplaces=")
    for i in data:
        f.write(i['places']+',')
    f.write("\n")
    f.close()

def makeFileTournamentResults(data):
    f = open("tournamentResults.txt","w",encoding="utf-8")
    for i in data:
        win = 0
        lose = 0
        for j in i['groupstage']:
            if(j == 'V'):
                win+=1
            if(j == 'D'):
                lose+=1
            if(j == 'F'):
                lose+=1
        i['groupstage'] = str(win)+" - "+str(lose)
    for i in data:
        if(int(i['places']) > 8):
            f.write('|{{TournamentResults/Line|place='+i['places']+'|team='+i['order']+'|groupstage='+i['groupstage']+"}}")
        f.write("\n")
    f.close()

leString = getOrderAndPlaces(URL,getNombrePageDeSwissGroup(URL))
print(leString)
makeFileOfFinalOrderPlaces(leString)
makeFileTournamentResults(leString)