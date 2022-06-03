#if it returns anything other than 0 then not connected to the internet
ping -c 1 -q google.com >&/dev/null; echo $?
