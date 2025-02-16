#!/bin/sh

# Will require sudo, also your user need to be in video group

# Make light changable via video group

# Add light file to video group 
sudo chown root:video /sys/class/backlight/intel_backlight/brightness 

# Make light writable for current (video) group
chmod g+w /sys/class/backlight/intel_backlight/brightness 
