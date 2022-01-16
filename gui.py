from tkinter import * 
import subprocess
import os 
import time
import asyncio 


root = Tk()
root.title('Auto Filmer')
root.geometry("400x400") 



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

      self.sendFiles = Button(master, text="Send Files To Server", command=self.sendFilesToServer)  
      self.sendFiles.pack(pady=20)
      
      self.sendFilesLabel = Label(master, text = "", font =("Courier", 20))
      self.sendFilesLabel.pack()
       

      self.filmBtnClicked = False  
      self.audioRecBtnClicked = False 
      self.sendBtnclicked  = False
      
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
        self.filmBtnClicked = False
        self.filmBtn['text'] = 'Click To Start Filming'

    def recordAudio(self):
      if not self.audioRecBtnClicked:
        process = subprocess.Popen('./scripts/record_audio.sh', shell=True)
        self.audioRecBtnClicked = True
        self.audioRecBtn['text'] = 'Click To Start Podcasting'
    #resets the uploading text on new action
      else:
        subprocess.run('kill $(pgrep parecord)', shell=True)
        self.audioRecBtnClicked = False
        self.audioRecBtn['text'] = 'Click To Start Podcasting'

    
    def sendFilesToServer(self): 
      process = subprocess.run('./scripts/send_recordings_to_server.sh',shell=True,capture_output=True) 
      consoleOutput = process.stderr.decode() # idk its stderr and not sdtout

      if (consoleOutput[0:10] == 'do_connect'):
        self.sendFilesLabel['text']='Could not connect to server \n Contact Avery Taylor'
      else:
        self.sendFilesLabel['text'] = consoleOutput
        #Assuming its done uploading when it cant output stderr 
        self.sendFilesLabel['text'] = 'Done uploading'



  
studio = Studio(root) 
root.mainloop()
