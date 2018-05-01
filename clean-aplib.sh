find . -name "AP.Thumbnails" -print0 | xargs -0 du -ch
find . -name "AP.Minis" -print0 | xargs -0 du -ch
find . -name "AP.Tinies" -print0 | xargs -0 du -ch

if [ "$1" = "delete" ]; then
    echo "Delete"
    find . -name "AP.Thumbnails" -delete
    find . -name "AP.Minis" -delete
    find . -name "AP.Tinies" -delete
fi
