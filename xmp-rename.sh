scriptdir=$(dirname $0)

for dir in $*; do
    cd $dir
    $scriptdir/xmp-rename.pl *.xmp
    cd ..
done
