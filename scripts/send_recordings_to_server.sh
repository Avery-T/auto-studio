
#saves the files from the camera 
#the camera doesnt save after its recording because its process gets killed to end reocrding

function downloadVideosFromCamera() {
  gphoto2 -P --new --filename "./recordings/%f.mp4"
}


function sendRecordingsToServer()
{
  python turn_on_file_server.py 
  sleep 1m  #it takes time for the server to start
  smbclient \\\\10.0.0.80\\SommersMedia -U='' password=''    
  smbclient //server/share -c 'cd c:/remote/path ; put local-file'
}


downloadVideosFromCamera
sendRecordingsToServer 
