#!/bin/bash
echo "This script install a syntax highlight complement for gedit"
dir_scope=/usr/share/gtksourceview-3.0/language-specs/
echo "file copied"
sudo \cp gcode.lang $dir_scope
sudo \cp gcode.lang /usr/share/gtksourceview-4/language-specs/
sudo \cp gcode.lang /usr/share/gtksourceview-5/language-specs/
for dir in /home/*/; do
    # strip trailing slash
    homedir="${dir%/}"
    # strip all chars up to and including the last slash
    username="${homedir##*/}"

    case $username in
    *.*) continue ;; # skip name with a dot in it
    esac
    sudo chown -R "$username" "$dir_scope"
done
echo "Finished without problems. Thanks for use and share it!"
exit 0

