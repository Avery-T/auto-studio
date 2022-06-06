#change pathing in the future 

function connectToVpn() {
  sudo wg-quick up peer5 
} 

#somthing is wrong but i can fix it on the main computer 

function sendRecordingsToServer()
{


  smbclient \\\\10.0.0.80\\SommersMedia -U='' --password '' -c 'cd Raw\ ; lcd ~/Projects/auto-studio/recordings/ ; prompt; mput *'

  #need to make a check to make sure the above command worked
  #moves all the recordings to the archive so the program doesnt resend the same files

  mv ~/Projects/auto-studio/recordings/*  ~/Desktop/recordings-archive/
 
  #turns file server off
  python ~/Projects/auto-studio/scripts/file_server_ctrl.py off 2> /dev/null 
}


sendRecordingsToServer 
