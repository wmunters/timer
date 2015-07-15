import Tkinter as tk
import subprocess as sub
import sys
from conference import *

class TimerGui(tk.Tk):
    def __init__(self, conference):

        tk.Tk.__init__(self)
        self.conference = conference

        # Set the window size
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.overrideredirect(1)
        self.geometry("%dx%d+0+0" % (w, h))

        # Define buttons etc.
        toolbar = tk.Frame(self)
        toolbar.pack(side="top", fill="x")
        b1 = tk.Button(self, text="Timer Wednesday", command=self.time_Wed)
        b2 = tk.Button(self, text="Timer Thursday", command=self.time_Thu)
        b3 = tk.Button(self, text="Timer Friday", command=self.time_Fri)
        self.e = tk.Entry(self)
#        self.e.focus_set()
        b4 = tk.Button(self, text='Play session', command=self.selectSession)
        b5 = tk.Button(self, text='Override time', command=self.overRide)
        bpause    = tk.Button(self, text="Pause/Play", command = self.PlayPause)
        self.e2 = tk.Entry(self)
        bnext     = tk.Button(self, text="Next", command = self.Next)
        bquit     = tk.Button(self, text="Quit", command = self.destroy)

        # Place them on the toolbar
        b1.pack(in_=toolbar, side="left")
        b2.pack(in_=toolbar, side="left")
        b3.pack(in_=toolbar, side="left")
        bquit.pack(in_=toolbar, side="right")
        self.e.pack(in_=toolbar, side="right")
        b4.pack(in_=toolbar, side="right")
        bnext.pack(in_ =toolbar, side="right")
        bpause.pack(in_ =toolbar, side="right")
        self.e2.pack(in_=toolbar, side="right")
        b5.pack(in_=toolbar, side="right")



        # Define some text-holding labels
        self.labelheader = tk.Label(self, font="Verdana 30 bold", justify=LEFT, wraplength=w)
        self.labelheader.pack(side="top", fill="both", expand=True)
        self.label = tk.Label(self, font="Verdana 125 bold")
        self.label.pack(side="top", fill="both", expand=True)

        self.Pause = False
        self.Next  = False
        self.Prev  = False
        self.OverRideTime = False

    def overRide(self):
        self.OverRideTime = True
        self.setTime = int(self.e2.get())*60

    # Toggle between play and pause
    def PlayPause(self):
        self.Pause = not self.Pause

    # Skip to the next presentation
    def Next(self):
        self.Next = True

    # Select a session to start with
    def selectSession(self):
        sess_string=self.e.get()
        dummyDay = getSessions(self,sess_string)
        if dummyDay is not 0:
            dummyDay.DayTimer(self, self.labelheader, self.label)

    # Full day timers
    def time_Wed(self):
        day = self.conference.days[0]
        day.DayTimer(self, self.labelheader, self.label)
    def time_Thu(self):
        day = self.conference.days[1]
        day.DayTimer(self, self.labelheader, self.label)
    def time_Fri(self):
        day = self.conference.days[2]
        day.DayTimer(self, self.labelheader, self.label)


gui = TimerGui(conference)
gui.mainloop()

