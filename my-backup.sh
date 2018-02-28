#!/bin/bash
# Run from the home directory

dpkg-query -l > Documents/pkg.list

borg create \
     --verbose \
     --stats \
     --compression zlib,6 \
     --exclude-caches \
     --exclude '.cache/*' \
     --exclude 'tmp/*' \
     --exclude 'Downloads/*' \
     --exclude 'Dropbox/*' \
     /media/jny/Linux\ backup/repo::'{now}' \
     .
