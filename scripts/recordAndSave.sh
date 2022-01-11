#!/bin/bash

#idk why the camera makes you do the command twice to work

function setupCamera() {
  gphoto2 \
     --set-config viewfinder=1 \
     --set-config capturetarget='Memory card' \
     --set-config movierecordtarget=Card \
     --wait-event 10s \
     --set-config movierecordtarget=None \
     --wait-event-and-download 2s \
     --set-config viewfinder=0
 } 


 function recordAndSave(){
  gphoto2 \
     --set-config viewfinder=1 \
     --set-config capturetarget='Memory card' \
     --set-config movierecordtarget=Card \
     --wait-event $1s  \
     --set-config movierecordtarget=None \
     --wait-event-and-download 2s \
     --set-config viewfinder=0
 } 

 function main() 
 {
    setupCamera 
    recordAndSave 5 
 }

main
