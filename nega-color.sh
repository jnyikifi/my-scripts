#!/usr/bin/env bash

mkdir -p out tiff
for pic in $*; do
    tiffPic="tiff/${pic%.*}.tiff"
    tiffOut="out/${pic%.*}.tiff"
    jpgPic="out/${pic%.*}.jpg"

    echo "Convert $pic to $tiffPic"
    sips -s format tiff $pic --out $tiffPic

    echo "Negative conversion $tiffPic to $tiffOut"
    ${HOME}/Src/negative2positive/negative2positive -a s -cb a $tiffPic $tiffOut
    echo "Create B&W $jpgPic"
    convert $tiffOut \
        -fx '(r+g+b)/3' -colorspace Gray \
        -clahe 25x25%+128+3 \
        -kuwahara 0x0.5 \
        -sharpen 0x0.5 \
        $jpgPic
done
