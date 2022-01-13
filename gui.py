from tkinter import *
import tkinter.font as font
import subprocess 

# you're going to need to refacter this # 

recordClicked = False 


def startOrStopFilming():  
  global recordClicked 
 
  if not recordClicked:  
    p = subprocess.Popen('./scripts/record_video.sh', shell=True)
    recordClicked = True 
    videoButton['text'] = 'Click To Stop Filming' 
    #resets the uploading text on new action
    li['text'] = '' 
  else:
    subprocess.run('kill $(pgrep gphoto2)', shell=True) 
    recordClicked = False
    videoButton['text'] = 'Click To Start Filming'



# write error handeling

def sendRecordingsToServer(): 
  process = subprocess.run('./scripts/send_recordings_to_server.sh',shell=True,capture_output=True)

  # idk its stderr and not sdtout

  consoleOutput = process.stderr.decode()

  if (consoleOutput[0:10] == 'do_connect'): 
    li['text']='Could not connect to server \n Contact Avery Taylor'
  else: 
    li['text'] = consoleOutput 
    #Assuming its done uploading when it cant output stderr 
    li['text'] = 'Done uploading' 
  

gui = Tk()
gui.geometry("3840x2160")
  
l = Label(gui, text = "Auto Filmer and Podcaster Desgined by Avery :D", font =("Courier", 20))
li =  Label(gui, text ='hey', font =("Courier", 20))


videoButton = Button(gui, text='Click To Start Filming\n\n(make sure the camera switch is set to record)', height=15, width=200, command=startOrStopFilming)
audioButton = Button(gui, text='Record Audio', height=15, width=200) 
sendFilesButton = Button(gui, text='Click Me To Send Files To Server', height=15, width=200, command=sendRecordingsToServer) 


l.pack(pady=30)

videoButton.pack(pady=50)
audioButton.pack(pady=20) 
sendFilesButton.pack(pady=20) 

li.pack(pady=40) 

gui.mainloop()


