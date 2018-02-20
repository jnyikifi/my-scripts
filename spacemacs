docker run -ti --name spacemacs \
 -e DISPLAY="unix$DISPLAY" \
 -e UNAME="knyberg" \
 -e UID="1000" \
 -e TZ=Europe/Helsinki \
 -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
 -v /etc/localtime:/etc/localtime:ro \
 -v /etc/machine-id:/etc/machine-id:ro \
 -v /var/run/dbus:/var/run/dbus \
 -v ${HOME}:/mnt/workspace \
 -v ${HOME}/.local/share/spacemacs/home/emacs:/home/emacs \
 -v ${HOME}/.gitconfig:/home/emacs/.gitconfig \
 --rm \
 spacemacs/emacs25:develop
