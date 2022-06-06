#change pathing in the future 
# use this function if you need to use a vpn to access file server
function connectToVpn() {
  sudo wg-quick up peer5 
} 


python ./file_server_ctrl.py on 2> /dev/null #to get rid of stderr




