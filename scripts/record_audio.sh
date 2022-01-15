pacmd list-sources | egrep '^\s+name: .*alsa_input'


parecord --channels=1 -d alsa_input.usb-Focusrite_Scarlett_2i2_USB-00.analog-stereo new.wave






