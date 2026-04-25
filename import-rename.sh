#!/bin/bash

set -e

dry_run=false

if [[ "$1" == "--dry-run" ]]; then
    dry_run=true
fi

month_number() {
    case "$1" in
        January)   echo 01 ;;
        February)  echo 02 ;;
        March)     echo 03 ;;
        April)     echo 04 ;;
        May)       echo 05 ;;
        June)      echo 06 ;;
        July)      echo 07 ;;
        August)    echo 08 ;;
        September) echo 09 ;;
        October)   echo 10 ;;
        November)  echo 11 ;;
        December)  echo 12 ;;
        *)         echo "" ;;
    esac
}

for dir in "Imported on "*/; do
    [[ -d "$dir" ]] || continue

    if [[ "$dir" =~ ^"Imported on "([0-9]+)\.[[:space:]]([A-Za-z]+)[[:space:]]([0-9]{4})/ ]]; then
        day="${BASH_REMATCH[1]}"
        month_name="${BASH_REMATCH[2]}"
        year="${BASH_REMATCH[3]}"
        month=$(month_number "$month_name")

        if [[ -z "$month" ]]; then
            echo "Unknown month: $month_name (skipping '$dir')" >&2
            continue
        fi

        new_name=$(printf "%s-%s-%02d" "$year" "$month" "$day")
        dir="${dir%/}"

        if [[ -d "$new_name" ]]; then
            n=1
            while [[ -d "${new_name}.${n}" ]]; do
                (( n++ ))
            done
            new_name="${new_name}.${n}"
        fi

        if [[ "$dry_run" == true ]]; then
            echo "$dir -> $new_name"
        else
            mv -v "$dir" "$new_name"
        fi
    fi
done
