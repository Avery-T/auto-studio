from tkinter import *
import tkinter.font as font
import subprocess 

def startFilming():  
   subprocess.run('./recordAndSave.sh') 

def startPodcast(): 

def main(): 
  gui = Tk()
  gui.geometry("1920x1080")

  l = Label(gui, text = "Click Me To Film")
  l.config(font =("Courier", 14))
  # create button

  videoButton = Button(gui, text='recordVideo', height=15, width=200, command=startFilming)
  audioButton = Button(gui, text='Record Audio', height=15, width=200) 

  l.pack()

  videoButton.pack()
  audioButton.pack(pady=20) 

  gui.mainloop()

main() 
