#!/usr/bin/env bash

mkdir -p heic jpg
for file in *.heic *.HEIC; do
    base="${file%.*}"
    echo "Converting $file to jpg/$base.jpg"
    convert "$file" -quality 95 "jpg/$base.jpg"
    mv -v "$file" heic/
done
