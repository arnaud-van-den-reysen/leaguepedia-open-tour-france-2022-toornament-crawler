from pickle import TRUE
from bs4 import BeautifulSoup
import requests
from globalVariable import URLROUND,SCORE,TIME,DATE

def getMatchScheduleAndResult(url,score):
    response = requests.get(url)
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

def makeFileMatchScheduleAndResult(data,score,time,date):
    f = open("schedule.txt","w",encoding="utf-8")
    index = 1
    for i in data:
        f.write("{{MatchSchedule|date="+date+" |time="+time+" |timezone=CET |dst=spring\n")
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

leString = getMatchScheduleAndResult(URLROUND,SCORE)
print(leString)
makeFileMatchScheduleAndResult(leString,SCORE,TIME,DATE)