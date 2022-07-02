
function sendRecordingsToServer()
{
  #have to do full path for lcd
  smbclient \\\\10.0.0.80\\SommersMedia -U='' --password '' -c 'cd Raw\ ; lcd /home/av/Projects/auto-studio/recordings/ ; prompt; mput *'

  #need to make a check to make sure the above command worked
  #moves all the recordings to the archive so the program doesnt resend the same files

  mv ~/Projects/auto-studio/recordings/*  ~/Desktop/recordings-archive/
 
  #turns file server off
  #python ~/Projects/auto-studio/scripts/file_server_ctrl.py off 2> /dev/nullmb
}


sendRecordingsToServer

