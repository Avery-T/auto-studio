#!/bin/bash

#remeber to change this ip 

smbServerIP=10.0.0.80

ping -c1 -W1 $smbServerIP >/dev/null && echo 1 || echo 0
