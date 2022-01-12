#!/bin/bash

# idk why the camera makes you do the command twice to work

# this script will record forever, The gui "kills" this script to get the camera to stop recording
# no option in Gphoto2 to record until interupted 


function setupCamera(){
  gphoto2 \
     --set-config viewfinder=1 \
     --set-config capturetarget='Memory card' \
     --set-config movierecordtarget=Card \
     --wait-event 2s \
     --set-config movierecordtarget=None \
     --wait-event-and-download 2s \
     --set-config viewfinder=0
 } 

# record never ends itself
#the gui will kill the script and thats how the recording ends

 function record(){
  gphoto2 \
     --set-config viewfinder=1 \
     --set-config capturetarget='Memory card' \
     --set-config movierecordtarget=Card \
     --wait-event 1200s \
     --set-config movierecordtarget=None \
     --set-config viewfinder=0
 } 

 function main(){
    setupCamera 
    record
 }

main
