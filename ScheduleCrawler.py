from pickle import TRUE
from bs4 import BeautifulSoup
import requests

TournamentID = "5301317149362552832/stages/5301538581880315904/groups/5301538582987612293/rounds/5301538582987612361/" #SEUL VARIABLE à MODIFIER
DATE = "2022-02-26" #DATE DU MATCH
TIME = "13:00" #HEURE DU MATCH (|timezone=CET |dst=no)
SCORE = TRUE #FALSE si les scores sont tombés, TRUE si pas de scores
URL = "https://play.toornament.com/fr/tournaments/"+TournamentID

def getMatchScheduleAndResult(URL,score):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    schedule = []
    for i in soup.find_all('div',class_="record"):
        result = []
        for j in i.stripped_strings:
            result.append(j)
        print(result)
        if(score):
            schedule.append(
                {'team1': result[0],
                'team2': result[1]}
            )
        else:
            schedule.append(
                {'team1': result[0],
                'team1score': result[1],
                'team2': result[2],
                'team2score': result[3]}
            )
    return schedule

def makeFileMatchScheduleAndResult(data,score):
    f = open("schedule.txt","w",encoding="utf-8")
    index = 1
    for i in data:
        f.write("{{MatchSchedule|date="+DATE+" |time="+TIME+" |timezone=CET |dst=no\n")
        if (score):
            f.write("|initialorder="+str(index)+"|team1="+i['team1']+" |team2="+i['team2']+'\n')
            f.write("|team1score= |team2score= |winner=\n")
        else:
            f.write("|initialorder="+str(index)+"|team1="+i['team1']+" |team2="+i['team2']+'\n')
            if(i['team1score'] == 'V'):
                f.write("|team1score=1 |team2score=0 |winner=1")
                if(i['team2score'] == 'F'):
                    f.write(" |ff=2\n")
                else:
                    f.write("\n")
            if(i['team2score'] == 'V'):
                f.write("|team1score=0 |team2score=1 |winner=2")
                if(i['team1score'] == 'F'):
                    f.write(" |ff=1\n")
                else:
                    f.write("\n")
        f.write("}}\n")
        index+=1
    f.close()

leString = getMatchScheduleAndResult(URL,SCORE)
print(leString)
makeFileMatchScheduleAndResult(leString,SCORE)