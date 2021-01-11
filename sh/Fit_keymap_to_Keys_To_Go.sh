#!/usr/bin/env sh

set -o noclobber
set -o nounset

# Get what key you type.
#
grep "Name=\"Keys-To-Go System Control\"" </proc/bus/input/devices >/dev/null || (
	echo "The keyboard is NOT 'Keys-To-Go'."
	exit 1
)

which xmodmap >/dev/null
case "${?}" in
0)
	xmodmap -e 'keycode 147 = Escape'
	;;
*)
	echo "'xmodmap' is not installed." 1>&2
	return 1
	;;
esac

return 0
