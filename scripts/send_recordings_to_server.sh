#change pathing in the future 

function connectToVpn() {
  sudo wg-quick up peer5 
} 


function sendRecordingsToServer()
{
  #turns file server on
  python /home/av/Projects/auto-studio/scripts/file_server_ctrl.py on 2> /dev/null #to get rid of stderr
  sleep 2m  #it takes time for the server to start
  smbclient \\\\10.0.0.80\\SommersMedia -U='' --password '' -c 'cd Raw\ ; lcd /home/av/Projects/auto-studio/recordings/; prompt; mput *'
  #need to make a check to make sure the above command worked
  #moves all the recordings to the archive so the program doesnt resend the same files
  mv /home/av/Projects/auto-studio/recordings/*  /home/av/Desktop/recordings-archive/
  #turns file server off
  python /home/av/Projects/auto-studio/scripts/file_server_ctrl.py off 2> /dev/null 
}


sendRecordingsToServer 
