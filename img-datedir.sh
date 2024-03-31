#!/bin/sh

for file in $*; do
    exif_datetime=`identify -format "%[EXIF:DateTimeOriginal]" $file`
    out_datetime=`echo $exif_datetime | awk '{ print $1 }' | sed 's/:/-/g; s/ /_/g;'`
    # echo "$exif_datetime | $out_datetime"
    if [ ! -d  $out_datetime ]; then
        mkdir $out_datetime
    fi
    mv -v $file ${out_datetime}/$file
done
