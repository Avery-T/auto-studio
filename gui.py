#!/usr/bin/env python3
#testing to see if update button works
from tkinter import * 
from tkinter import messagebox
import subprocess
import os 
import time
from time import sleep
root = Tk()
root.title('Auto Filmer')
root.geometry("1080x1080") 


class Studio:
    
    def __init__(self, master):
      myFrame = Frame(master) 
      myFrame.pack() 

      self.filmBtn = Button(master, text="Start Filming",command=self.film) 
      self.filmBtn.pack(pady=5)
      self.filmLabel = Label(master, text = "Make Sure the Camera switch is switched to the film icon\n Camera will not record if its just ON", font =("Courier"))
      self.filmLabel.pack() 

      self.audioRecBtn = Button(master, text="Start a solo podcast", command=self.recordAudio) 
      self.audioRecBtn.pack(pady=20)
      self.audioLabel = Label(master, text = "make sure audio equipment is turned on", font =("Courier"))
      self.audioLabel.pack()

      self.sendFiles = Button(master, text="Send Files To Server", command=self.sendFilesToServer)  
      self.sendFiles.pack(pady=20)
      
      self.sendFilesLabel = Label(master, text = "", font =("Courier"))
      self.sendFilesLabel.pack()
      
      
      self.updateBtn = Button(master, text="check for updates",command=self.updateCheck) 
      self.updateBtn.pack(pady=5)
      
      self.filmLabel = Label(master, text = "check for updates", font =("Courier"))
      self.filmLabel.pack() 

      self.filmBtnClicked = False  
      self.audioRecBtnClicked = False 
      self.sendBtnclicked  = False
      self.updatePresent = False    
     
    #generalize this funciton 

    def film(self): 

      if not self.filmBtnClicked:

        process = subprocess.Popen('./scripts/record_video.sh', shell=True)
        #stdout and stderr are io blocking so this checks if the program is runing blocking io for only 4s not infinitly 
        time.sleep(4) #wait for the start record_video script to run all the functions
        checkForRuningProcess = subprocess.Popen('pgrep gphoto2', shell=True, stdout=subprocess.PIPE) 
        runing = checkForRuningProcess.communicate()[0].decode() 

        if runing:  
          self.filmBtnClicked = True
          self.filmBtn['text'] = 'Click To Stop Filming'
          self.filmLabel['text'] = '' 
        else:
          self.filmLabel['text'] = 'Camera Not Detected'  
        
      else:
        subprocess.run('kill $(pgrep gphoto2)', shell=True)
        time.sleep(5)
        self.filmLabel['text'] = 'Downlaoding video...' 
        subprocess.run('./scripts/download_video.sh', shell=True) 
        #add code to donwload the video 
        self.filmLabel['text'] = '' 
        self.filmBtnClicked = False
        self.filmBtn['text'] = 'Click To Start Filming'

    def recordAudio(self):
      if not self.audioRecBtnClicked:
        process = subprocess.Popen('./scripts/record_audio.sh', shell=True)
        #stdout and stderr are io blocking so this checks if the program is runing blocking io for only 4s not infinitly 
        time.sleep(4) #wait for the start record_video script to run all the functions
        checkForRuningProcess = subprocess.Popen('pgrep parecord', shell=True, stdout=subprocess.PIPE)
        runing = checkForRuningProcess.communicate()[0].decode()

        if runing:
          self.audioRecBtnClicked = True
          self.audioRecBtn['text'] = 'Click To Stop Recording Audio '
          self.audioLabel['text'] = ''
        else:
          self.audioLabel['text'] = 'Audio Equipment not Detected'

      else:
        subprocess.run('killall parecord', shell=True)
        self.audioRecBtnClicked = False
        self.audioRecBtn['text'] = 'Click To Start Recording Audio'
    

    def sendFilesToServer(self): 
    
      response = messagebox.askokcancel("send files",
            "Warning Sending files will halt the program until all the files are sent, this could take hours") 
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

      process = subprocess.Popen('./scripts/checkForUpdate.sh', shell=True, stdout=subprocess.PIPE)

      #casted to a int because i just want to know if the local repo is zero or more commits behind
      consoleOutput = int(process.communicate()[0].decode())
      
      if not (consoleOutput):
        self.updatePresent = True
        self.updateBtn['text'] = 'click again to restart the program and update' 
         
      else:
        self.updateBtn['text'] = 'No updates avaliable' 
      return
    def update(self): 
     root.destroy()
     sleep(2)
     for i in range(4):
        print('hello world')
     process = subprocess.Popen('./scripts/checkForUpdate.sh', shell=True) 
studio = Studio(root) 
root.mainloop()
