#!/bin/bash

DIR=$(dirname -- "$(readlink -f "${BASH_SOURCE}")")
CPDIR="$DIR/build/CIRCUITPY"
ZIPFILE="$DIR/build/bundle_file.zip"

# default to the project directory
if [[ "$1" != "" ]]; then
	PROJECTDIR = "$1"
else
	PROJECTDIR="project"
fi

# copy files into the build directory
mkdir -p "$CPDIR"/lib
cp boot_out.txt "$CPDIR"/boot_out.txt
cp -r "$PROJECTDIR"/* "$CPDIR"/

# circup --path CIRCUITPY install --auto
for file in `find "$CPDIR" -name "*.py"`
do
	# run circup on every python file
	FILE=`echo $file | sed "s|^$CPDIR\/||"`
	echo circup $FILE
	circup --path "$CPDIR" install --auto --auto-file "$FILE"
done

# cleanup the boot_out.txt
rm "$CPDIR"/boot_out.txt

# erase extended attributes (if you're on mac)
find "$CPDIR" -name '._*' -exec rm -vrf {} \;
# erase DS_Store files (if you're on mac)
find "$CPDIR" -name .DS_Store -exec rm -vrf {} \;

# zip the thing
zip -r "$ZIPFILE" "$CPDIR"
# copy locally
cp -i "$ZIPFILE" ./

# cleanup
rm -rf "$CPDIR"
