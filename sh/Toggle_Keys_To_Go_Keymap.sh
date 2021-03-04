#!/usr/bin/env sh

set -o noclobber
set -o nounset

PROGNAME="${0}"

usage() {
	cat <<EOM
Usage: '${PROGNAME}' [OPTION]...

	-h, --help                Display help.
	    --on
	    --off
	-s  --status              Check to see if the key map has been changed.
EOM
}
# Get what key you type.
# xev | grep --only-matching --regexp='keycode [0-9]*'
# 9     0xff1b (Escape) 0x0000 (NoSymbol) 0xff1b (Escape)
# 147   0x1008ff65 (XF86MenuKB) 0x0000 (NoSymbol) 0x1008ff65 (XF86MenuKB)

grep "Name=\"Keys-To-Go System Control\"" </proc/bus/input/devices >/dev/null || (
	echo "The keyboard is NOT 'Keys-To-Go'."
	exit 1
)

which xmodmap >/dev/null
case "${?}" in
0)
	xmodmap -e 'keycode 147 = Escape NoSymbol Escape'
	;;
*)
	echo "'xmodmap' is not installed." 1>&2
	return 1
	;;
esac

return 0
