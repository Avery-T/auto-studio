function downloadRecordings() 
{
  gphoto2 -P --new
}


function sendRecordingsToServer()
{
  smbclient \\\\10.0.0.80\\SommersMedia -U='' password=''    
  smbclient //server/share -c 'cd c:/remote/path ; put local-file'
}


downloadRecordings
