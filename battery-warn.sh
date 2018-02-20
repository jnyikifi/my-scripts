#!/bin/bash

warn=$1
current=$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep percentage| awk '{ print $2 }' | sed 's/%//')

while true; do
    if [ "$current" -le "$warn" ]; then
        i3-nagbar -t warning -m "Battery low ($current/$warn %), recharge!" -f pango:"Noto 18"
    fi
    sleep 60
done
