#!/usr/bin/python
# coding: utf-8

import numpy as np
import time
from Tkinter import *

# ms delay (set to 1000 for real-time)
tt = 1000 

# Time of break & keynotes
Twelcome       = 15   # 15 minutes welcome on Wednesday
Tposterflash   = 40   # 40 minutes poster flash presenations
Tcoffee_poster = 50   # 50 minutes poster & coffee session on Wednesday
Tlunchbreak    = 70   # 1h10 minutes lunchbreak everyday
Tcoffee        = 30   # 30 minutes coffeebreak
Tcoffee_fri    = 20   # 20 minutes coffeebreak on Friday 

# Regular presentations
T = 15              # presentation time
Twarn = 3           # 2 minutes warning
Tquest = 4          # 5 minutes questions
Tswitch = 1         # 60 seconds to switch speakers

# Keynote lectures
Tkeynote = 42       # 50 minutes keynotes
Twarnkeynote = 6    # 6 minutes warning during keynotes
Tquestkeynote = 7   # 7 minutes questions during keynotes

class Conference:
    def __init__(self,days):
        self.days = days

    def ConferenceTimer(self):
        for day in self.days:
            day.DayTimer()

class Day:
    def __init__(self, sessions):
        self.sessions = sessions

    def DayTimer(self, guiroot, headerbox, timebox):
        for session in self.sessions:
            guiroot.update_idletasks()
            guiroot.update()
            session.SessionTimer(guiroot,headerbox,timebox)

    def printSchedule(self):
        for session in self.sessions:
            session.printDetails()

class Session:
    def __init__(self, name, day, tstart, tend, presentations,number):
        self.name = name
        self.day = day
        self.presentations = presentations
        self.tstart = tstart
        self.tend   = tend
        self.number = number

    def SessionTimer(self,master,headerlabel, label):
        for pres in self.presentations:
            pres.printDetailsPres(self.name,self.number,headerlabel)

            if 'break' in self.name or 'Break' in self.name:
                bgactivecolor='black'
                textactivecolor='white'
                bgwarncolor='black'
            else:
                bgactivecolor='green'
                textactivecolor='black'
                bgwarncolor='yellow'

            # Time for the presentation itself
            timeLeft = pres.duration*60 # initial time left in seconds
            while timeLeft>=0:
                minutesLeft, secondsLeft = divmod(timeLeft, 60)
                #minutesLeft, secondsLeft = (timeLeft // 60, timeLeft % 60)
                stringtime= "%02d:%02d" % (minutesLeft, secondsLeft)
                if timeLeft<=pres.warn*60:
                    label.config(text=stringtime, bg=bgwarncolor, fg=textactivecolor)
                else:
                    label.config(text=stringtime, bg=bgactivecolor, fg=textactivecolor)
                #master.update_idletasks()
                master.update()
                master.after(tt)
                #master.update()
                if not master.Pause:
                    timeLeft = timeLeft-1
                if master.Next:
                    timeLeft = -1

            # Time for questions
            if not ('Break' in self.name or 'break' in self.name or master.Next):
                timeLeftq = pres.question*60 # question time left in seconds
                if not timeLeftq == 0:
                    while timeLeftq>=0:
                        minutesLeft, secondsLeft = divmod(timeLeftq, 60)
                        #minutesLeft, secondsLeft = (timeLeft // 60, timeLeft % 60)
                        stringtime= "%02d:%02d" % (minutesLeft, secondsLeft)
                        label.config(text=stringtime, bg='red', fg='white')
                        #master.update_idletasks()
                        master.update()
                        master.after(tt)
                        if not master.Pause:
                           timeLeftq = timeLeftq-1
    
                # Time for switching speakers
                timeSwitch = Tswitch*60
                while timeSwitch>=0:
                    minutesLeft, secondsLeft = divmod(timeSwitch, 60)
                    #minutesLeft, secondsLeft = (timeLeft // 60, timeLeft % 60)
                    stringtime= "%02d:%02d" % (minutesLeft, secondsLeft)
                    label.config(text=stringtime, bg='black', fg='white')
                    #master.update_idletasks()
                    master.update()
                    master.after(tt)
                    if not master.Pause:
                       timeSwitch = timeSwitch-1

            # Reset the next toggle to False! 
            master.Next = False

class Presentation:
    def __init__(self, authors, title, tstart, T, Tq = 0, Tw=Twarn):
        self.authors = authors
        self.title   = title
        self.tstart  = tstart
        self.duration= T
        self.question= Tq
        self.warn    = Tw

    def printDetailsPres(self,sessname, sessnumber,label):
        textstring = ''
        if not sessnumber=='':
            textstring = textstring+ 'Session '+sessnumber+': '+sessname+'\n\n'
        else:
            textstring = textstring+sessname+'\n\n'
        if not self.authors=='':
            textstring = textstring+ self.authors+'\n'
            textstring = textstring+ '"'+self.title+'"'
        label.config(text=textstring,justify=LEFT)

def getSessions(guiroot,sessionString):
    startletter = sessionString[0]
    if startletter == 's':  # regular session    
        if sessionString=='s1': startSession = session1; day = day1
        if sessionString=='s2': startSession = session2; day = day1
        if sessionString=='s3': startSession = session3; day = day1
        if sessionString=='s4': startSession = session4; day = day2
        if sessionString=='s5': startSession = session5; day = day2
        if sessionString=='s6': startSession = session6; day = day2
        if sessionString=='s7': startSession = session7; day = day3
        if sessionString=='s8': startSession = session8; day = day3
        if sessionString=='s9': startSession = session9; day = day3

    elif startletter == 'k': # keynote lecture
        if sessionString=='k1': startSession = keynote1; day = day1 
        if sessionString=='k2': startSession = keynote2; day = day1
        if sessionString=='k3': startSession = keynote3; day = day2
        if sessionString=='k4': startSession = keynote4; day = day2
        if sessionString=='k5': startSession = keynote5; day = day2
        if sessionString=='k6': startSession = keynote6; day = day3 

    elif startletter == 'b': # break
        if sessionString=='bcwm': startSession = coffeebreak_wedmorn; day = day1
        if sessionString=='bctm': startSession = coffeebreak_thumorn; day = day2
        if sessionString=='bcta': startSession = coffeebreak_thuaft;  day = day2
        if sessionString=='bcfm': startSession = coffeebreak_frimorn; day = day3
        if sessionString=='bcfa': startSession = coffeebreak_friaft;  day = day3
        if sessionString=='blw': startSession = lunchbreak_wed; day =day1
        if sessionString=='blt': startSession = lunchbreak_thu; day =day2
        if sessionString=='blf': startSession = lunchbreak_fri; day =day3

    elif startletter == 'p': # poster session
        if sessionString=='pflash': startSession = posterflash; day = day1
        if sessionString=='pcoff': startSession = coffeebreak_poster; day = day1

    try:
        day
    except UnboundLocalError:
        guiroot.labelheader.config(text="Session not recognized")
        return 0

    startindex = day.sessions.index(startSession)
    return Day(day.sessions[startindex:])


#########################################################
#       SESSION DEFINITIONS                             #
#########################################################


#----------------------------
# Welcome
#----------------------------
welcome = Presentation('',
        "Welcome",
        "08:45", Twelcome)
welcome = Session("Welcome", "Wed", "08:45", "09:00", [
    welcome],'')

#----------------------------
# Keynote1
#----------------------------
keynote = Presentation("J. Apt",
        "What the characteristics of wind power mean for integration into power grids",
        "09:00", Tkeynote, Tq=Tquestkeynote, Tw=Twarnkeynote)
keynote1 = Session('Keynote Lecture I', 'Wed', '09:00', '09:50', [keynote],'')

#----------------------------
# Keynote2
#----------------------------
keynote = Presentation("J. Mann", 
        "Lidar measurements in the atmospheric boundary layer and around wind turbines",
        "09:50", Tkeynote, Tq=Tquestkeynote, Tw=Twarnkeynote)
keynote2 = Session('Keynote Lecture II', 'Wed', '09:50', '10:40', [keynote],'')

#----------------------------
# Coffee break
#----------------------------
coffee = Presentation('',
        'Coffee Break', 
        '10:40', Tcoffee)
coffeebreak_wedmorn = Session('Coffee Break', 'Wed', '10:40', '11:10', [coffee],'')

#----------------------------
# Session1
#----------------------------
pres1 = Presentation("H. Beck, J.-J. Trujillo, D. Trabucchi, J. Schneemann, M. Kühn", 
        "Full field observation of dynamic wakes by means of long-range LIDAR measurements",
        "11:10", T, Tquest)
pres2 = Presentation("G. Giebel, T. G. Bozkurt, M. R. Skjelmose, J. R. Kristoffersen",
        "Full scale wake experiments at Horns Rev - The case of downregulation",
        "11:30", T, Tquest)
pres3 = Presentation("S. Raach, D. Schlipf, J.-J. Trujillo, P. W. Cheng",
        "Model-based wake tracking using LIDAR measurements for wind farm control",
        "11:50", T, Tquest)
pres4 = Presentation("J.-J. Trujillo, M. Kühn",
        "Application of dynamic time warping in wake tracking analysis",
        "12:10", T, Tquest)
session1 = Session('Wake and ABL interaction I', 'Wed', '11:10', '12:10', [pres1, pres2, pres3, pres4],'I')

#----------------------------
# Lunchbreak
#----------------------------
lunch = Presentation('',
        'Lunch break', 
        '12:30', Tlunchbreak)
lunchbreak_wed= Session('Lunchbreak', 'Wed', '12:30', '13:40', [lunch],'')

#----------------------------
# Session2
#----------------------------
pres1 = Presentation("C. Meneveau, R. J. A. M. Stevens, B. Hobbs, A. Ramos",
        "Coupling fluid dynamic and economic wind farm models to determine optimal wind turbine spacing",
        "13:40", T, Tquest)
pres2 = Presentation("L. Soetran, J. Bartl", 
        "Parameter Variation for Maximizing the Power Production of a Model Wind Farm",
        "14:00", T, Tquest)
pres3 = Presentation("N. Noppe, W. Weijtjens, C. Devriendt",
        "Performance monitoring by tracking estimated power curves on a wind farm level",
        "14:20", T, Tquest)
session2 = Session('Wind-farm optimization', 'Wed', '13:40', '14:20', [pres1, pres2, pres3],'II')

#----------------------------
# Poster flash presentations
#----------------------------
poster = Presentation('',
        'Poster Flash Presentations',
        '14:40', Tposterflash)
posterflash = Session('Poster Flash Presentations', 'Wed', '14:40', '15:20', [poster],'')

#----------------------------
# Coffee break and poster
#----------------------------
coffeeposter = Presentation('',
        'Coffee break & Poster session',
        '15:20', Tcoffee_poster)
coffeebreak_poster = Session('Coffee break & Poster session', 'Wed', '15:20', '16:10', [coffeeposter],'')

#----------------------------
# Session 3
#----------------------------
pres1 = Presentation("P. Gebraad, P. Fleming, A. Wright, J.-W. van Wingerden",
        "Multidisciplinary Research on Wake Control in Wind Power Plants at NREL: Wake Modeling and Control, Systems Engineering, and Field Testing",
        "16:10", T, Tquest)
pres2 = Presentation("J. Meyers, J. P. Goit, W. Munters",
        "Optimal coordinated control of energy extraction in wind farms",
        "16:30", T, Tquest)
pres3 = Presentation("E. Bossanyi, T. Jorge",
        "Practical tools for optimisation of wind plant sector management strategies",
        "16:50", T, Tquest)
pres4 = Presentation("M. Therkildsen, J. Herp, M. Greiner",
        "Wind farm power optimization and control in highly variable multiple wake flows",
        "17:10", T, Tquest)
pres5 = Presentation("C. Shapiro, L. A. Martinez-Tossas, C. Meneveau, D. F. Gayme",
        "Frequency Regulation Controllers for Wind Farms - Preliminary Findings from Large-Eddy Simulations",
        "17:30", T, Tquest)
pres6 = Presentation("J. N. Sakamuri, P. Tielens, D. Van Hertem, N. A. Cutululis",
        "Improved onshore AC Grid Frequency & DC Grid Voltage Control from Offshore Wind Power Plants connected through HVDC using wind speed forecast",
        "17:50", T, Tquest)
session3 = Session('Wind-farm control', 'Wed', '16:10', '18:10', [pres1, pres2, pres3, pres4, pres5, pres6],'III')

######################
# DAY1               #
######################
day1 = Day([welcome, keynote1, keynote2, coffeebreak_wedmorn, session1, lunchbreak_wed, session2, posterflash, coffeebreak_poster, session3])



#################################################################################################################################

#----------------------------
# Keynote III
#----------------------------
keynote = Presentation("C. Bottasso",
        "Wind farm control: strategies and testing",
        "08:40", Tkeynote, Tq=Tquestkeynote, Tw=Twarnkeynote)
keynote3 = Session("Keynote Lecture III", "Thu", "08:40", "09:30", [keynote],'')

#----------------------------
# Keynote IV
#----------------------------
keynote = Presentation("J. D. McCalley",
        "Wind, solar and natural gas: issues for high wind energy penetration in electric power grids",
        "09:30", Tkeynote, Tq=Tquestkeynote , Tw=Twarnkeynote)
keynote4 = Session("Keynote Lecture IV", "Thu", "09:30", "10:20", [keynote],'')

#----------------------------
# Coffee break
#----------------------------
coffee = Presentation('',
        'coffee break', 
        '10:20', Tcoffee)
coffeebreak_thumorn = Session('Coffee Break', 'Thu', '10:20', '10:50', [coffee],'')

#----------------------------
# Session 4
#----------------------------
pres1 = Presentation("B. F. Hobbs, C. Bothwell, R. B. Hytowitz, J. Kazempour, V. Prava, L. Zhao, J. B. Cardell, C. L. Anderson",
        "Integrated Analyses of Demand Response, Wind variability, and Markets",
        "10:50", T, Tquest)
pres2 = Presentation("K. Bruninx, E. Delarue, W. D'Haeseleer",
        "The impact of uncertainty on wind power forecasts on power system balancing: reserve sizing, allocation and activation",
        "11:10", T, Tquest)
pres3 = Presentation("K. Van den Bergh, D. Couckuyt, E. Delarue, W. D'Haeseleer",
        "Redispatching in an interconnected electricity system with high penetration of offshore wind",
        "11:30", T, Tquest)
pres4 = Presentation("K. De Vos, J. Driesen",
        "The Active Participation of Wind Power in Operating Reserves",
        "11:50", T, Tquest)
pres5 = Presentation("I. C. JimÃ©nez GarcÃ­a, M. Davis, F. Doblas-Reyes, V. Torralba-Fernandez, N. Gonzalez-Reviriego",
        "Predicting wind power markets: a new generation of climate risk management tools",
        "12:10", T, Tquest)
session4 = Session("Electricity markets and grid integration", "Thu", "10:50", "12:30", [pres1, pres2, pres3, pres4, pres5],'IV')

#----------------------------
# Lunchbreak
#----------------------------
lunch = Presentation('',
        'Lunch break', 
        '12:30', Tlunchbreak)
lunchbreak_thu = Session('Lunchbreak', 'Thu', '12:30', '13:40', [lunch],'')


#----------------------------
# Keynote V
#----------------------------
keynote = Presentation("D. Gayme",
        "Management of energy resources for flexible and efficient power systems",
        "13:40", Tkeynote, Tq=Tquestkeynote, Tw=Twarnkeynote)
keynote5 = Session("Keynote Lecture V", "Thu", "13:40", "14:30", [keynote],'')

#----------------------------
# Session 5
#----------------------------
pres1 = Presentation("R. J. A. M. Stevens, D. Gayme, C. Meneveau",
        "Testing the coupled wake boundary layer model with LES of turbulent flow in widely spaced wind-farms",
        "14:30", T, Tq=Tquest)
pres2 = Presentation("M. Abkar, F. Porté-Agel",
        "On the Influence of Coriolis Forces on the Structure and Evolution of Wind-Turbine Wakes",
        "14:50", T, Tq=Tquest)
pres3 = Presentation("D. Allaerts, J. Meyers",
        "Importance of boundary layer height and Coriolis forces for energy extraction in large wind farms",
        "15:10", T, Tq=Tquest)
pres4 = Presentation("S. J. Andersen, J. N. Sørensen, R. F. Mikkelsen",
        "Large Scale Meandering in Wind Farms",
        "15:30", T, Tq=Tquest)
pres5 = Presentation("M. Wilczek, R. J. A. M. Stevens, C. Meneveau",
        "Wavenumber-frequency spectra in the logarithmic layer of neutral atmospheric boundary layers",
        "15:50", T, Tq=Tquest)
pres6 = Presentation("Y. Ostovan, E. Anik, A. Abdulrahim, O. Uzol",
        "Experimental Investigation of Effects of Tip Injection on the Performance of Two Interacting Wind Turbines",
        "16:10", T, Tq=Tquest)
session5 = Session("Wake and ABL interaction II", "Thu", "14:30", "16:30", [pres1, pres2, pres3, pres4, pres5, pres6],'V')

#----------------------------
# Coffee break
#----------------------------
coffee = Presentation('',
        'coffee break', 
        '16:30', Tcoffee)
coffeebreak_thuaft = Session('Coffee Break', 'Thu', '16:30', '17:00', [coffee],'')


#----------------------------
# Session 6
#----------------------------
pres1 = Presentation("P. J. H. Volker, J. Bagder, A. N. Hahmann, M. Badger, C. B. Hasager",
        "The Simulation of Wind Farm Wakes with Mesoscale Models",
        "17:00", T, Tq=Tquest)
pres2 = Presentation("F. Chatterjee, D. Allaerts, N. Van Lipzig, U. Blahak, J. Meyers",
        "Impact of wind farms on the North Sea climate",
        "17:20", T, Tq=Tquest)
pres3 = Presentation("V. Sharma, M. Calaf, M. B. Parlange, M. Lehning",
        "An LES study of a large wind farm during a realistic (CASES99) diurnal cycle",
        "17:40", T, Tq=Tquest)
pres4 = Presentation("C. Santoni, U. Ciri, S. Leonardi",
        "Effect of topography on wind turbine power fluctuations and blade loads",
        "18:00", T, Tq=Tquest)
pres5 = Presentation("W. Gutierrez, G. Araya, P. Kiliyanpilakkil, A. Ruiz-Columbie, M. Tutkun, L. Castillo",
        "Structural Impact of Different Low Level Jet Types over Wind Turbines in West Texas",
        "18:20", T, Tq=Tquest)
session6 = Session("ABL and meso-scale models", "Thu", "17:00", "18:40", [pres1, pres2, pres3, pres4, pres5],'VI')

######################
# DAY2               #
######################
day2 = Day([keynote3, keynote4, coffeebreak_thumorn, session4, lunchbreak_thu, keynote5, session5, coffeebreak_thuaft, session6])


#################################################################################################################################

#----------------------------
# Keynote VI
#----------------------------
keynote = Presentation("F. Porté-Agel",
        "Interaction between wind farms and the atmospheric boundary layer: simulations and experiments",
        "08:40", Tkeynote, Tq=Tquestkeynote , Tw=Twarnkeynote)
keynote6 = Session("Keynote Lecture VI", "Fri", "08:40", "09:30", [keynote],'')

#----------------------------
# Session 7
#----------------------------
pres1 = Presentation("T. G. Bozkurt, G. Giebel, P. E. Sørensen, P.-E. Réthoré",
        "Available Active Power Estimation for Offshore Wind Power Plants",
        "09:30", T, Tq=Tquest)
pres2 = Presentation("V. Thomas, C. VerHulst, C. Meneveau, D. Gayme",
        "Dynamic mode decomposition applied to large-eddy simulations of wind farms",
        "09:50", T, Tq=Tquest)
pres3 = Presentation("G. V. Iungo, C. Santoni, S. Leonardi",
        "Data-driven Reduced Order Model for prediction of wind turbine wakes",
        "10:10", T, Tq=Tquest)
pres4 = Presentation("A. Staid, C. VerHulst, S. D. Guikema",
        "Statistical Modeling of Wind Farm Power Production: A Study of Predictive Accuracy for Multiple Wind Farms",
        "10:30", T, Tq=Tquest)
session7 = Session("Data-driven wind-farm models", "Fri", "09:30", "10:50", [pres1, pres2, pres3, pres4], 'VII')

#----------------------------
# Coffee break
#----------------------------
coffee = Presentation('',
        'coffee break', 
        '10:50', Tcoffee_fri)
coffeebreak_frimorn = Session('Coffee Break', 'Fri', '10:50', '11:10', [coffee], '')

#----------------------------
# Session 8
#----------------------------
pres1 = Presentation("W. Munters, C. Meneveau, J. Meyers",
        "Turbulent inflow precursor method with time-varying direction for large-eddy simulations and applications to wind farms",
        "11:10", T, Tq=Tquest)
pres2 = Presentation("S. Shamsoddin, F. Porté-Agel",
        "Large-eddy Simulation of Atmospheric Boundary-Layer Flow through a Wind Farm Sited on Complex Terrain",
        "11:30", T, Tq=Tquest)
pres3 = Presentation("E. Ploumakis, D. Mehta, L. Lignarolo, W. Bierbooms",
        "Enhanced kinetic energy entrainment in wind farm wakes: LES study of a wind turbine array with tethered kites",
        "11:50", T, Tq=Tquest)
pres4 = Presentation("P. Bauweraerts, J. Meyers",
        "Large-eddy simulation of wind-farm boundary-layer transients",
        "12:10", T, Tq=Tquest)
pres5 = Presentation("G. Cortina, V. Sharma, M. Calaf",
        "Turbulence analysis upstream of a wind turbine: a LES approach to improve wind LIDAR technology",
        "12:30", T, Tq=Tquest)
session8 = Session("Wake and ABL interaction III", "Fri", "11:10", "12:50", [pres1, pres2, pres3, pres4, pres5], 'VIII')

#----------------------------
# Lunchbreak
#----------------------------
lunch = Presentation('',
        'Lunch break', 
        '12:50', Tlunchbreak)
lunchbreak_fri = Session('Lunchbreak', 'Fri', '12:50', '14:00', [lunch],'')

#----------------------------
# Session 9
#----------------------------
pres1 = Presentation("J. U. Bretheim, C. Meneveau, D. F. Gayme",
        "Developing a large eddy simulation variant of the restricted nonlinear model for wall-bounded turbulent flow",
        "14:00", T, Tq=Tquest)
pres2 = Presentation("M. Calaf,  G. Cortina,  Y. Dinkar, V. Sharma",
        "Wind Turbine Box, the flow around a characteristic wind turbine",
        "14:20", T, Tq=Tquest)
pres3 = Presentation("L. A. Martinez, A. E. Yilmaz, M. J. Churchfield, J. Meyers, C. Meneveau",
        "Comparison of an Actuator Line Model implementation in three different Large-Eddy Simulation Codes",
        "14:40", T, Tq=Tquest)
pres4 = Presentation("S. Sarmast, S. Ivanell",
        "Comparison of wind turbine wake properties using actuator line and disc approaches",
        "15:00", T, Tq=Tquest)
session9 = Session("Wind-farm large-eddy simulations - technical aspects", "Fri", "14:00", "15:20", [pres1, pres2, pres3, pres4], 'IX')

######################
# DAY3               #
######################
day3 = Day([keynote6, session7, coffeebreak_frimorn, session8, lunchbreak_fri, session9])


#day1.DayTimer()
#day2.DayTimer()
#day3.DayTimer()

conference = Conference([day1, day2, day3])

