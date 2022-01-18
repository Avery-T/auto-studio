#change pathing in the future 

function connectToVpn() { 
  sudo wg-quick up peer5 
} 


function sendRecordingsToServer()
{
  python /home/av/Projects/auto-studio/scripts/file_server_ctrl.py on 2> /dev/null #to get rid of stderr
  sleep 2m  #it takes time for the server to start
  smbclient \\\\10.0.0.80\\SommersMedia -U='' --password '' -c 'cd Raw\ ; lcd /home/av/Projects/auto-studio/recordings/; prompt; mput *'
  python /home/av/Projects/auto-studio/scripts/file_server_ctrl.py off 2> /dev/null 
}


sendRecordingsToServer 
