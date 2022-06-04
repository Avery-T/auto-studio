#!/usr/bin/env python3

from tkinter import * 
from tkinter import messagebox
import subprocess
import os 
import time
from time import sleep
root = Tk()
root.title('Auto Filmer')
root.geometry("1080x1080") 
           
TEXT = [
         ['click to start fliming','click to stop fliming', 
             'camera not detected', 
              'downloading video from camera'],
         ['start a solo podcast','audio equipment not detected','click to stop recording auido'], 
         ['send files to server'], 
         ['check for updates'], 
         ['Updating closes the program. \nreopen the program after it closes'],  
         ['not connected to the internet'] 
       ]

class Studio:
    
    def __init__(self, master): 
      myFrame = Frame(master) 
      myFrame.pack() 
      self.filmBtn = Button(master, text=TEXT[0][0],command=self.film) 
      self.filmBtn.pack(pady=20)

      self.audioRecBtn = Button(master, text=TEXT[1][0], command=self.recordAudio) 
      self.audioRecBtn.pack(pady=20)
      self.audioLabel = Label(master, font =("Courier"))
      self.audioLabel.pack()

      self.sendFiles = Button(master, text=TEXT[2][0], command=self.sendFilesToServer)  
      self.sendFiles.pack(pady=20)
      
      self.sendFilesLabel = Label(master, text = "", font =("Courier"))
      self.sendFilesLabel.pack()
      
      
      self.updateBtn = Button(master, text=TEXT[3][0],command=self.updateCheck) 
      self.updateBtn.pack(pady=50)
      
      self.filmLabel = Label(master, text =TEXT[4][0], font =("Courier"))
      self.filmLabel.pack()

      self.filmBtnClicked = False  
      self.audioRecBtnClicked = False 
      self.sendBtnclicked  = False
      self.updatePresent = False    
     
    #generalize this funciton 

    def film(self): 

      if not self.filmBtnClicked:

        process = subprocess.Popen('./scripts/record_video.sh', shell=True)
        #stdout and stderr are io blocking so this checks if the program is runing blocking 
        sleep(4) #wait for the start record_video script to run all the functions
        checkForRuningProcess = subprocess.Popen('pgrep gphoto2', shell=True, stdout=subprocess.PIPE) 
        runing = checkForRuningProcess.communicate()[0].decode() 

        if runing:  
          self.filmBtnClicked = True
          self.filmBtn['text'] = TEXT[0][1]
          self.filmLabel['text'] = '' 

        else: # camera not detected
          self.filmBtn['text'] = TEXT[0][2]
          #each change needs a function, using after so you dont need to sleep the program
          self.filmBtn.after(2000, lambda: self.filmBtn.configure(text=TEXT[0][0]))
      
      else:
        subprocess.run('kill $(pgrep gphoto2)', shell=True)
        sleep(5)
        self.filmBtn['text'] = TEXT[0][3]
        subprocess.run('./scripts/download_video.sh', shell=True) 
        #add code to donwload the video 
         
        #self.filmLabel['text'] = '' #done  
        self.filmBtnClicked = False
        self.filmBtn.after(2000, lambda: self.filmBtn.configure(text=TEXT[0][0]))
        

    def recordAudio(self):
      if not self.audioRecBtnClicked:
        process = subprocess.Popen('./scripts/record_audio.sh', shell=True)
        #stdout and stderr are io blocking so this checks if the program is runing blocking io for only 4s not infinitly 
        time.sleep(4) #wait for the start record_video script to run all the functions
        checkForRuningProcess = subprocess.Popen('pgrep parecord', shell=True, stdout=subprocess.PIPE)
        runing = checkForRuningProcess.communicate()[0].decode()

        if runing:
          self.audioRecBtnClicked = True
          self.audioRecBtn['text'] = TEXT[1][2] 
          self.audioLabel['text'] = ''
        else:
          self.audioRecBtn.config(text=TEXT[1][1]) 
          #self.audioRecBtn.config(text= TEXT[1][0])

      else:
        subprocess.run('killall parecord', shell=True)
        self.audioRecBtnClicked = False
        self.audioRecBtn['text'] = TEXT[1][0]
    

    def sendFilesToServer(self): 
      
      if self.internetCheck(): 
         self.sendFilesLabel['text'] = TEXT[6][0] 
         return 
    
      response = messagebox.askokcancel(
      "send files","Warning Sending files will halt the program until all the files are sent, this could take hours") 

      if not response: return 

      self.sendFilesLabel['text'] = 'Server is starting...\nplease wait 3 minutes to start file transfer' 
      process = subprocess.run('./scripts/send_recordings_to_server.sh', shell=True, capture_output=True) 
      consoleOutput = process.stdout.decode() 
      self.sendFilesLabel['text'] = consoleOutput
      self.sendFilesLabel['text'] = 'Done uploading' 
     
      
    
    def updateCheck(self): 

      if self.updatePresent:
        self.update()
       
        return 
      

      if self.internetCheck(): 
         self.updateBtn['text'] = 'Please Connect to the internet' 
         return 


      process = subprocess.Popen('./scripts/checkForUpdate.sh', shell=True, stdout=subprocess.PIPE)

      #casted to a int because i just want to know if the local repo is zero or more commits behind
      consoleOutput = int(process.communicate()[0].decode())
      
      if (consoleOutput):
        self.updatePresent = True
        self.updateBtn['text'] = 'click again to restart the program and update' 
         
      else:
        self.updateBtn['text'] = 'No updates avaliable' 
      return
  
    def internetCheck(self): 
     
       process = subprocess.Popen('./scripts/internet_check.sh', shell=True, stdout=subprocess.PIPE)

      #casted to a int because i just want to know if the local repo is zero or more commits behind
       return(int(process.communicate()[0].decode()))

       
    def update(self): 

     root.destroy()
     process = subprocess.Popen('./scripts/update.sh', shell=True) 

     quit() 

studio = Studio(root) 
root.mainloop()
