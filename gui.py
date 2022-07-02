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
           

GUI_TEXT = {
            'film_options': ['click to start fliming','click to stop fliming', 'camera not detected', 'downloading video from camera'],
            'podcast_options': ['start a solo podcast','audio equipment not detected','click to stop recording auido'],
            'internet_options':['send files to server','not connected to the internet'],
            'update_options': ['check for updates','Updating closes the program. \nreopen the program after it closes']
        }

# END NIMA's ATTEMPT

class Studio:
    
    def __init__(self, master): 
      myFrame = Frame(master) 
      myFrame.pack() 
      self.filmBtn = Button(master, text=GUI_TEXT['film_options'][0],command=self.film) 
      self.filmBtn.pack(pady=20)

      self.audioRecBtn = Button(master, text=GUI_TEXT['podcast_options'][0], command=self.recordAudio) 
      self.audioRecBtn.pack(pady=20)

      self.sendFilesBtn = Button(master, text=GUI_TEXT['internet_options'][0], command=self.sendFilesToServer)  
      self.sendFilesBtn.pack(pady=20)
      
      self.sendFilesLabel = Label(master, text = "", font =("Courier"))
      self.sendFilesLabel.pack()
      
      self.updateBtn = Button(master, text=GUI_TEXT['update_options'][0],command=self.updateCheck) 
      self.updateBtn.pack(pady=50)
      
      self.filmLabel = Label(master, text =GUI_TEXT['update_options'][1], font =("Courier"))
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
          self.filmBtn['text'] = GUI_TEXT['film_options'][1]
          self.filmLabel['text'] = '' 

        else: # camera not detected
          self.filmBtn['text'] = GUI_TEXT['film_options'][2]
          #each change needs a function, using after so you dont need to sleep the program
          self.filmBtn.after(2000, lambda: self.filmBtn.configure(text=GUI_TEXT['film_options'][0]))
      
      else:
        subprocess.run('kill $(pgrep gphoto2)', shell=True)
        sleep(5)
        self.filmBtn['text'] = GUI_TEXT['film_options'][3]
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
          self.audioRecBtn['text'] = GUI_TEXT['podcast_options'][2] 
        else:
          self.audioRecBtn.config(text=GUI_TEXT['podcast_options'][1]) 
          self.audioRecBtn.after(2000, lambda: self.audioRecBtn.configure(text=GUI_TEXT['podcast_options'][0]))

      else:
        subprocess.run('killall parecord', shell=True)
        self.audioRecBtnClicked = False
        self.audioRecBtn['text'] = GUI_TEXT['podcast_options'][0]


    def sendFilesToServer(self): 
      
      if self.internetCheck(): 
         self.sendFilesBtn['text'] = GUI_TEXT['internet_options'][2] 
         self.sendFilesBtn.after(2000, lambda: self.sendFilesBtn.configure(text=GUI_TEXT['internet_options'][0]))
         return 
      
      #rewrite the check, it takes too long to check if it worked 
      #self.sendFilesBtn['text'] = 'checking to see you can connect to server please wait 3 minutes' 
      
     #dont have the oauth key for the bot right now
     ###self.turnFileServerOnAndConnect()##
     #change back to 180
      sleep(30)

      subprocess.run('./scripts/connect_to_vpn.sh', shell=True) 

      if self.fileServerIsOn(): 
        #self.sendFilesBtn.after(1000, lambda: self.sendFilesBtn.configure(text='file server is on uploading files now'))

       # response = messagebox.askokcancel(
       # "send files","Warning Sending files will halt the program until all the files are sent, this could take hours") 
       # if not response: return 
       # self.sendFilesBtn.after(1000, lambda: self.sendFilesBtn.configure(text='server in on!'))

        self.sendFilesLabel['text'] = 'Server is starting...\nplease wait 3 minutes to start file transfer' 
        process = subprocess.run('./scripts/send_recordings_to_server.sh', shell=True, capture_output=True) 
        
        
        #TO DO display the uploading video
    def turnFileServerOnAndConnect(self): 
        subprocess.Popen('./scripts/turn_server_on_and_connect.sh', shell=True)

    def fileServerIsOn(self): 
      process = subprocess.Popen('./scripts/check_if_file_server_is_up.sh', shell=True, stdout=subprocess.PIPE)
      return process.communicate()[0].decode() 


    def updateCheck(self): 
      
      if self.internetCheck(): 
         self.updateBtn['text'] = 'Please Connect to the internet' 
         return 

      if self.updatePresent:
        self.update()
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
  
    #internet check doent work if the program is connected to the vpn
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
