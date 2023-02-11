#!/usr/bin/env bash

mkdir -p out tiff
for pic in $*; do
    tiffPic="tiff/${pic%.*}.tiff"
    jpgPic="out/${pic%.*}.jpg"
    tiffOut="out/${pic%.*}.tiff"

    echo "Convert $pic to $tiffPic"
    sips -s format tiff $pic --out $tiffPic

    echo "Final conversion $tiffPic to $jpgPic"
    if [ 0 -eq 1 ]; then
        convert $tiffPic \
            -fx '(r+g+b)/3' -colorspace Gray \
            -negate \
            -clahe 25x25%+128+3 \
            -kuwahara 0x0.5 \
            -sharpen 0x1 \
            $jpgPic
    fi
    convert $tiffPic \
        -colorspace Gray \
        -negate \
        $tiffOut
done
