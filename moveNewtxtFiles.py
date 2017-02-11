import wx
import wx.lib.agw.multidirdialog as MDD
import os
from os import path
import datetime as dt
import time
import shutil
import sqlite3


class MyForm(wx.Frame):
    
            
    def __init__(self):
       
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "File Browser GUI")

        panel = wx.Panel(self, wx.ID_ANY)
        self.currentDirectory = os.getcwd()

        self.txt3 = wx.TextCtrl(panel, size = (400, 125), style = wx.TAB_TRAVERSAL|wx.TE_MULTILINE|wx.TE_LINEWRAP)
        self.txt4 = wx.TextCtrl(panel, size = (400, 55), style = wx.TAB_TRAVERSAL|wx.TE_MULTILINE|wx.TE_LINEWRAP)
        self.txt5 = wx.TextCtrl(panel, size = (400, 55), style = wx.TAB_TRAVERSAL|wx.TE_MULTILINE|wx.TE_LINEWRAP)
        self.txt6 = wx.TextCtrl(panel, size = (400, 55), style = wx.TAB_TRAVERSAL|wx.TE_MULTILINE|wx.TE_LINEWRAP)
        fileCheckBtn = wx.Button(panel, label = "Run File Check")
        fileCheckBtn.Bind(wx.EVT_BUTTON, self.mainFunc)

        self.txt1 = wx.TextCtrl(panel, size = (200, 25))
        dirDiaBtn = wx.Button(panel, label = "Select Folder to Check for Updates")
        dirDiaBtn.Bind(wx.EVT_BUTTON, self.onOpen)

        self.txt2 = wx.TextCtrl(panel, size=(200, 25))
        dirDiaBtn2 = wx.Button(panel, label = "Select Folder to Receive Changes ")
        dirDiaBtn2.Bind(wx.EVT_BUTTON, self.onDir)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(dirDiaBtn, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.txt1, 0, wx.ALL|wx.CENTER,5)
        sizer.Add(dirDiaBtn2, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.txt2, 0, wx.ALL|wx.CENTER,5)
        sizer.Add(fileCheckBtn, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.txt3, 5, wx.ALL|wx.CENTER,5)
        sizer.Add(self.txt4, 0, wx.ALL|wx.CENTER,5)
        sizer.Add(self.txt5, 0, wx.ALL|wx.CENTER,5)
        sizer.Add(self.txt6, 0, wx.ALL|wx.CENTER,5)
        panel.SetSizer(sizer)
        
    #I added the text boxes in 2 seperate functions    
    def onOpen(self, event):
        panel = wx.Panel(self, wx.ID_ANY)
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           )
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetPath()

            self.txt1.write(self.filename)
            
                
    def onDir(self, event):
        panel = wx.Panel(self, wx.ID_ANY)
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           )
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetPath()
            self.txt2.write(self.filename)  
        dlg.Destroy()

    def mainFunc(self,event):
        
       
                

        
        hold = self.txt1.GetValue()
        receive = self.txt2.GetValue()
        for files in os.listdir(hold):
            self.txt3.write("files: {}".format(files))
            if files.endswith(".txt"):
                source = (os.path.join(hold, files))
                destination = (os.path.join(receive, files))
                mtime = (os.path.getmtime(source))
                timeDiff = time.time() - mtime 
                _24hrsAgo = time.time() - (24 *60 *60) 
                last24hrs = time.time() - _24hrsAgo 
                if timeDiff < last24hrs: 
                    self.txt4.write('Updated File(s) detected: {}'.format(files))
                    self.txt5.write('Updated File(s) moved to: {}'.format(destination))
                    try:
                        shutil.copy(source,destination) 
                    except IOError as e:
                        return ('could not open the file: %s ') % e

        conn = sqlite3.connect('record.db')

        c = conn.cursor()
        conn.execute("CREATE TABLE if not exists File_Check( ids INTEGER, date_stamp TIMESTAMP);")
        paths = self.txt1.GetValue()
        idfordb = 1
        date = str(dt.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
        c.execute("INSERT INTO File_Check( ids, date_stamp) VALUES(?,?)", (idfordb, date))
        
        conn.commit()

        with conn:
            c.execute("SELECT date_stamp FROM File_Check ORDER BY date_stamp DESC LIMIT 1")
            returnVal = c.fetchall()[0] #Need this to select data from the tuple and get it out of unicode
            for date in returnVal:
                    self.txt6.SetValue("Last File Check DB entry: {}".format(date))
        conn.close()
          
 
if __name__=="__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()
