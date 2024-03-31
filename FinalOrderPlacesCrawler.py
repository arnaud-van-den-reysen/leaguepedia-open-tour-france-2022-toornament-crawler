import re
from bs4 import BeautifulSoup
import requests

def getNombrePageDeSwissGroup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    nombrePageDeParticipant = 0
    for a in soup('a',class_="page"):
        nombrePageDeParticipant+=1
    if nombrePageDeParticipant == 0:
        nombrePageDeParticipant = 1
    return nombrePageDeParticipant

def getOrderAndPlaces(url,nbPage):
    """
    return [{'order': 'Elyandra Esport', 'places': '1', 'groupstage': 'VVDVVV'}, {'order': 'Omerix', 'places': '2', 'groupstage': 'VVVVVD'},...]
    if not complete [{'order': 'CICADAS Gaming', 'places': '1', 'groupstage': 'V'}, {'order': 'Voltage', 'places': '1', 'groupstage': 'V'},...]
    """
    orderAndPlaces = []
    order = []
    places = []
    groupstage = []
    for i in range(1,nbPage+1):
        response = requests.get(url+"?page="+str(i))
        soup = BeautifulSoup(response.text, 'html.parser')
        for j in soup.find_all('div',class_="rank large"):
            if j.get_text() != "#":
                places.append(j.get_text())
        for j in soup.find_all('div',class_="name weighted"):
            if j.get_text() != "Nom":
                order.append(j.get_text())
        for j in soup.find_all('div',class_=re.compile("history history-")):#history-<n° de result>
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

def getFinalOrderPlacesLeaguepediaFormat(url):
    leString = getOrderAndPlaces(url,getNombrePageDeSwissGroup(url))
    txt = "|finalorder="
    for i in leString:
        txt = txt + i['order']+','
    txt = txt + "\n"
    txt = txt + "|finalplaces="
    for i in leString:
        txt = txt + i['places']+','
    txt = txt + "\n"
    return txt

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

def getTournamentResultsLeaguepediaFormat(url):
    leString = getOrderAndPlaces(url,getNombrePageDeSwissGroup(url))
    txt = ''
    for i in leString:
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
    for i in leString:
        if(int(i['places']) > 8):
            txt = txt + '|{{TournamentResults/Line|place='+i['places']+'|team='+i['order']+'|groupstage='+i['groupstage']+"}}\n"    
    return txt