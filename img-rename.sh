#!/bin/sh

for file in $*; do
    exif_datetime=`identify -format "%[EXIF:DateTimeOriginal]" $file`
    exif_model=`identify -format "%[EXIF:Model]" $file`
    out_num=`echo $file | perl -pe 's/\D+(\d+)\D+/$1/'`
    out_datetime=`echo $exif_datetime | sed 's/:/-/g; s/ /_/g;'`
    out_model=`echo $exif_model | sed 's/:/-/g; s/ /_/g;'`
    out_ext=`echo $file | perl -pe 's/^.*\.(\w+)$/$1/'`
    echo "mv -v $file ${out_datetime}_${out_model}_${out_num}.${out_ext}"
    `mv -v $file ${out_datetime}_${out_model}_${out_num}.${out_ext}`
done
