from Tkinter import *
from datetime import datetime
from datetime import timedelta
from datetime import time
import json
import os.path

class PowerConvert(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)        
        self.grid()
        self.createWidgets()

    def createWidgets(self):        
        self.current = Label(self)
        self.current.config(font=('console', 14, 'normal'))
        self.current["text"] = "Current Power :"
        self.current.grid(row=0, column=0)

        self.currentText = Entry(self)
        self.currentText.config(font=('console', 14, 'normal'))
        self.currentText["width"] = 50
        self.currentText.grid(row=0, column=1, columnspan=6)
         
        self.goal = Label(self)
        self.goal.config(font=('console', 14, 'normal'))
        self.goal["text"] = "Goal Power :"
        self.goal.grid(row=1, column=0)

        var = StringVar()
        self.goalText = Entry(self, textvariable=var)
        self.goalText.config(font=('console', 14, 'normal'))
        self.goalText["width"] = 50
        self.goalText.grid(row=1, column=1, columnspan=6)

        if os.path.isfile('goalValue.json'):
            loadFile = open('goalValue.json', 'r')
            line = loadFile.readline()
            context = json.loads(line)
            var.set(context["goalValue"])
        
        self.checkVar = IntVar()
        self.futureCheckBox = Checkbutton(self, variable = self.checkVar, onvalue = 1, offvalue = 0)
        self.futureCheckBox.grid(row=3, column=0, columnspan=1)
        self.futureCheckBox["command"] = self.SwitchInputTime
        
        self.hourTime = Entry(self, state = DISABLED)
        self.hourTime.config(font=('console', 14, 'normal'))
        self.hourTime["width"] = 10
        self.hourTime.grid(row=3, column=1, columnspan=1)

        self.minTime = Entry(self, state = DISABLED)
        self.minTime.config(font=('console', 14, 'normal'))
        self.minTime["width"] = 10
        self.minTime.grid(row=3, column=2, columnspan=1)
        
        self.clear = Button(self)
        self.clear.config(font=('console', 14, 'normal'))
        self.clear["text"] = "Clear"
        self.clear["command"] = self.Clear
        self.clear.grid(row=3, column=3, columnspan=2)

        self.count = Button(self)
        self.count.config(font=('console', 14, 'normal'))
        self.count["text"] = "Count Time"
        self.count["command"] = self.ConvertCount
        self.count.grid(row=3, column=5, columnspan=2)

        self.DistanceTime = Label(self)
        self.DistanceTime.config(font=('console', 18, 'normal'))
        self.DistanceTime["text"] = "Distance Time :"
        self.DistanceTime.grid(row=4, column=0, columnspan=6)
        
        self.CurrentTime = Label(self)
        self.CurrentTime.config(font=('console', 18, 'normal'))
        self.CurrentTime["text"] = "Current Time :"
        self.CurrentTime.grid(row=5, column=0, columnspan=6)
        
        self.EstimatedTime = Label(self)
        self.EstimatedTime.config(font=('console', 18, 'normal'))
        self.EstimatedTime["text"] = "Estimated Time :"
        self.EstimatedTime.grid(row=6, column=0, columnspan=6)
        
    def PowerAndPowerConvertTime(self):
        if int(self.goalText.get()) > int(self.currentText.get()):
            min = (int(self.goalText.get()) - int(self.currentText.get())) * 8
            self.DistanceTime["text"] = "Distance Time", min, "Min"
            
            nowTime = datetime.now()
            self.CurrentTime["text"] = "Current Time", nowTime.strftime('%m/%d %H:%M')

            allMin = timedelta(minutes = min)
            after = nowTime + allMin

            self.EstimatedTime["text"] = "Estimated Time", after.strftime('%m/%d %H:%M')            
            self.SaveLog();
        else:
            print "Error Value"

    def ConvertCount(self):
        '''
            cover count.
        '''
        if self.checkVar.get():
            self.PowerAndTimeConvertTime() 
        else:
            self.PowerAndPowerConvertTime()

    def PowerAndTimeConvertTime(self):
        '''
            SourcePower and goal time , cover to time
        '''
        nowTime = datetime.now()
        h = int(self.hourTime.get())
        m = int(self.minTime.get())
        isRightFormat = (h < 24)&(m < 60)
        if isRightFormat:
            print h, m
            print nowTime.time()
            afterTime = nowTime.replace(hour = h, minute = m)
            time = afterTime - nowTime
            print time
        else:
            print "input wrong."

    def SaveLog(self):        
        data = int(self.goalText.get())
        with open('goalValue.json', 'w') as outfile:
            json.dump({"goalValue":data}, outfile)

    def Clear(self):
        self.currentText.delete(0, END)
        self.goalText.delete(0, END)
        self.hourTime.delete(0, END)
        self.minTime.delete(0, END)

    def SwitchInputTime(self):
        '''
        NORMAL and DISABLED
        '''
        if self.checkVar.get():
            self.hourTime["state"] = NORMAL
            self.minTime["state"] = NORMAL
            self.goalText["state"] = DISABLED
        else:
            self.hourTime["state"] = DISABLED
            self.minTime["state"] = DISABLED
            self.goalText["state"] = NORMAL
            
root = Tk()
app = PowerConvert(master=root)
app.mainloop()