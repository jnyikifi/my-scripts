#!/bin/bash

borg delete \
     --stats \
     /media/jny/Linux\ backup/repo

borg init \
     --encryption none \
     /media/jny/Linux\ backup/repo
