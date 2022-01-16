from tkinter import * 
import subprocess

root = Tk()
root.title('Auto Filmer')
root.geometry("400x400") 



class Studio:
    
    def __init__(self, master):
      myFrame = Frame(master) 
      myFrame.pack() 

      self.flmBtn = Button(master, text="click me",command=self.film) 
      self.flmBtn.pack(pady=20)

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
        p = subprocess.Popen('./scripts/record_video.sh', shell=True)
        self.filmBtnClicked = True
        self.filmBtn['text'] = 'Click To Stop Filming'
        
      else:
        subprocess.run('kill $(pgrep gphoto2)', shell=True)
        self.filmBtnClicked = False
        self.filmBtn['text'] = 'Click To Start Filming'

    def recordAudio(self):
      if not self.audioRecBtnClicked:
        p = subprocess.Popen('./scripts/record_audio.sh', shell=True)
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
