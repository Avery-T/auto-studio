
#pacmd list-sources | egrep '^\s+name: .*alsa_input' # <-- this command is used to find the microphone alias 

#assuming where going to use Scarlett 2i2 forever 
microphone=alsa_input.usb-Focusrite_Scarlett_2i2_USB-00.analog-stereo

parecord --channels=1 -d $microphone /home/av/Desktop/codeStuffs/projects/auto-studio/scripts/new.wave

#make path not static later





