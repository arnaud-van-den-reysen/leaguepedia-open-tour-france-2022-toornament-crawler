import tkinter as tk
import globalVariable as gv
import ParticipantsCrawler as pc
import FinalOrderPlacesCrawler as fop

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

root = tk.Tk()

root.title('Leaguepedia Toornament Parser')

titrePrincipal = tk.Label(root,text='Leaguepedia Toornament Parser',font=("Helvetica",24)).pack()

labelURLPrincipal = tk.Label(root,text='Toornament URL').pack()

URLinfo = tk.StringVar()
textbox = tk.Entry(root,textvariable=URLinfo).pack()

labelParticipantsSection = tk.Label(root,text='Participants',font=("Helvetica",16)).pack()
tk.Button(root,text='Participants Parse',command=lambda: participantsSectionManager(URLinfo.get())).pack()

labelSchedulesSection = tk.Label(root,text='Schedule',font=("Helvetica",16)).pack()

labelFinalOrderPlacesSection = tk.Label(root,text='FinalOrderPlaces',font=("Helvetica",16)).pack()
tk.Button(root,text='FinalOrderPlaces Parse',command=lambda: finalOrderPlacesSectionManager(URLinfo.get())).pack()

labelTournamentResultsSection = tk.Label(root,text='TournamentResults',font=("Helvetica",16)).pack()
tk.Button(root,text='TournamentResults Parse',command=lambda: tournamentResultsSectionManager(URLinfo.get())).pack()

labelParsingResultSection = tk.Label(root,text='Parsing Result',font=("Helvetica",16)).pack()

text = tk.Text(root, height=8)
text.pack()

root.mainloop()