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
            if(i['team1score'] == 'V' or i['team1score'] == 'W'):
                f.write("|team1score=1 |team2score=0 |winner=1")
                if(i['team2score'] == 'F' or i['team2score'] == 'D'):
                    f.write(" |ff=2\n")
                else:
                    f.write("\n")
            if(i['team2score'] == 'V' or i['team2score'] == 'W'):
                f.write("|team1score=0 |team2score=1 |winner=2")
                if(i['team1score'] == 'F' or i['team1score'] == 'D'):
                    f.write(" |ff=1\n")
                else:
                    f.write("\n")
        f.write("}}\n")
        index+=1
    f.close()

def getScheduleLeaguepediaFormat(URLSchedule,score,time,date):
    leString = getMatchScheduleAndResult(URLSchedule,score)
    txt = ''
    index = 1
    for i in leString:
        txt = txt + "{{MatchSchedule|date="+date+" |time="+time+" |timezone=CET |dst=spring\n"
        if (score):
            txt = txt + "|initialorder="+str(index)+"|team1="+i['team1']+" |team2="+i['team2']+'\n'
            txt = txt + "|team1score= |team2score= |winner=\n"
        else:
            txt = txt + "|initialorder="+str(index)+"|team1="+i['team1']+" |team2="+i['team2']+'\n'
            if(i['team1score'] == 'V' or i['team1score'] == 'W'):
                txt = txt + "|team1score=1 |team2score=0 |winner=1"
                if(i['team2score'] == 'F' or i['team2score'] == 'D'):
                    txt = txt + " |ff=2\n"
                else:
                    txt = txt + "\n"
            if(i['team2score'] == 'V' or i['team2score'] == 'W'):
                txt = txt + "|team1score=0 |team2score=1 |winner=2"
                if(i['team1score'] == 'F' or i['team1score'] == 'D'):
                    txt = txt + " |ff=1\n"
                else:
                    txt = txt + "\n"
        txt = txt + "}}\n"
        index+=1
    return txt