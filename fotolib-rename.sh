#!/usr/bin/env bash
#
# Sort files from fotolib export into folders

function get_dir() {
    dir=$(echo $1 | sed 's/__.*$//;')
    echo $dir
}

function get_file() {
    file=$(echo $1 | sed 's/^.*__//;')
    echo $file
}

for candidate in *; do
    echo -n "candidate = $candidate"
    if [ -f "$candidate" ]; then
        d=$(get_dir "$candidate")
        f=$(get_file "$candidate")
        echo " result = $d/$f"
        if ! [ -d "$d" ]; then
            mkdir "$d"
        fi
        mv -v "$candidate" "$d/$f"
    else
        echo " not a file"
    fi
done
