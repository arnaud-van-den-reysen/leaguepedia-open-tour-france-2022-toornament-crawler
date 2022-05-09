from operator import contains
import tkinter as tk
from typing import Container
import globalVariable as gv
import ParticipantsCrawler as pc
import FinalOrderPlacesCrawler as fop
import ScheduleCrawler as sc

RESULT = ''

def participantsSectionManager(url):
    URLParticipants = gv.getParticipantsURLFromInfoURL(url)
    RESULT = pc.getParticipantsLeaguepediaFormat(URLParticipants)
    text.delete("1.0","end")
    text.insert('1.0',RESULT)

def finalOrderPlacesSectionManager(url):
    URLFinalOrderPlaces = gv.getRankingURLFromInfoURL(url)
    RESULT = fop.getFinalOrderPlacesLeaguepediaFormat(URLFinalOrderPlaces)
    text.delete("1.0","end")
    text.insert("1.0",RESULT)

def tournamentResultsSectionManager(url):
    URLTournamentResults = gv.getRankingURLFromInfoURL(url)
    RESULT = fop.getTournamentResultsLeaguepediaFormat(URLTournamentResults)
    text.delete("1.0","end")
    text.insert("1.0",RESULT)

def scheduleSectionManager(url,score,time,date):
    URLSchedule = gv.getScheduleURLFromInfoURL(url)
    RESULT = sc.getScheduleLeaguepediaFormat(URLSchedule,score,time,date)
    text.delete("1.0","end")
    text.insert("1.0",RESULT)

root = tk.Tk()

root.title('Leaguepedia Toornament Parser')

titrePrincipal = tk.Label(root,text='Leaguepedia Toornament Parser',font=("Helvetica",24)).pack()

labelURLPrincipal = tk.Label(root,text='Toornament URL :').pack()

URLinfo = tk.StringVar()
textbox = tk.Entry(root,textvariable=URLinfo).pack(fill='x')

labelParticipantsSection = tk.Label(root,text='Participants',font=("Helvetica",16)).pack()
tk.Button(root,text='Participants Parse',command=lambda: participantsSectionManager(URLinfo.get())).pack()

labelSchedulesSection = tk.Label(root,text='Schedule',font=("Helvetica",16)).pack()
SCORE = tk.BooleanVar()
DATE = tk.StringVar()
TIME = tk.StringVar()
labelDate = tk.Label(root,text='Date :').pack()
textbox = tk.Entry(root,textvariable=DATE).pack()
labelTime = tk.Label(root,text='Time :').pack()
textbox = tk.Entry(root,textvariable=TIME).pack()
r1 = tk.Radiobutton(root,text='Round Over',value=False,variable=SCORE).pack()
r2 = tk.Radiobutton(root,text='Round Not Started',value=True,variable=SCORE).pack()
tk.Button(root,text='Schedule Parse',command=lambda: scheduleSectionManager(URLinfo.get(),SCORE.get(),TIME.get(),DATE.get())).pack()

labelFinalOrderPlacesSection = tk.Label(root,text='FinalOrderPlaces',font=("Helvetica",16)).pack()
tk.Button(root,text='FinalOrderPlaces Parse',command=lambda: finalOrderPlacesSectionManager(URLinfo.get())).pack()

labelTournamentResultsSection = tk.Label(root,text='TournamentResults',font=("Helvetica",16)).pack()
tk.Button(root,text='TournamentResults Parse',command=lambda: tournamentResultsSectionManager(URLinfo.get())).pack()

labelParsingResultSection = tk.Label(root,text='Parsing Result',font=("Helvetica",16)).pack()

text = tk.Text(root, height=8)
text.pack()

root.mainloop()