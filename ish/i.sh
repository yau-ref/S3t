#! /bin/sh

cmd="$1"
file="$(basename -- $2)"

user='yauref'
host='localhost'
storagepath='~'
path="$storagepath/$file.gpg"

case "$cmd" in
  'push' ) $(pv "$file" | gpg --batch --no-tty --recipient "$user" -e | ssh "$host" "cat > $path" ) ;;
  'pull' ) $(ssh "$host" "cat $path" | gpg --batch --no-tty --recipient "$user" -d -o "$file.back") ;;
  * ) echo "command '$cmd' is unknown" ;;
esac

exit 0
