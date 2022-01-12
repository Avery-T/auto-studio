from tkinter import *
import tkinter.font as font
import subprocess 




recordClicked = False 
recordPID = ''

p = 0

def startFilming():  
  global recordClicked 
  global recordPID
  global p 

  if recordClicked==False: 
    p = subprocess.Popen('./scripts/record_video.sh', shell=True) 
    recordClicked = True 
 
  else:
    subprocess.run('kill $(pgrep gphoto2)', shell=True) 

#def startPodcast(): 

def main(): 
  gui = Tk()
  gui.geometry("1920x1080")

  l = Label(gui, text = "Auto Filmer and Podcaster Desgined by Avery :D")
  l.config(font =("Courier", 14))
  # create button
  videoButton = Button(gui, text='recordVideo', height=15, width=200, command=startFilming )
  audioButton = Button(gui, text='Record Audio', height=15, width=200) 
  sendFilesButton = Button(gui, text='Click Me To Send Files To Server', height=15, width=200) 
  l.pack()

  videoButton.pack(pady=50)

  audioButton.pack(pady=20) 

  sendFilesButton.pack(pady=20) 

  gui.mainloop()

main() 
