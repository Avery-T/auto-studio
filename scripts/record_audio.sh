#pacmd list-sources | egrep '^\s+name: .*alsa_input' # <-- this command is used to find the microphone alias 

#assuming where going to use Scarlett 2i2 forever 
#parecord --channels=1 -D alsa_input.usb-Focusrite_Scarlett_2i2_USB-00.analog-stereo /home/av/Desktop/codeStuffs/projects/auto-studio/new.wave

#make path not static later





parecord --channels=1 -d alsa_input.usb-Focusrite_Scarlett_2i2_USB-00.analog-stereo /home/av/Projects/auto-studio/recordings/$(date +%Y%m%dT%H%M%S).wav




