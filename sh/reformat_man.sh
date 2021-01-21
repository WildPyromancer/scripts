#!/usr/bin/env sh

set -o errexit
set -o noclobber
set -o nounset

PROGNAME="${0}"

usage() {
	cat <<EOM
Usage: man 'command' | '${PROGNAME}' [OPTION]...

	-h, --help                Display help.
	-s, --spaces=             Number of spaces. -> tab size
EOM
}

check_three_or_four() {
	case "${1}" in
	3 | 4)
		return 0
		;;
	*)
		echo "${PROGNAME}: spaces are 3 or 4. not ${1}." 1>&2
		return 1
		;;
	esac
}

for OPT in "${@}"; do
	case "${OPT}" in
	-h | --help)
		usage
		exit 0
		;;
	--spaces=*)
		SPACES=$(echo "${1}" | sed -E --expression='s/^--.+=(.+)$/\1/')
		check_three_or_four "${SPACES}" || exit 1
		;;
	-s | --spaces)
		if [ -n "${2}" ] || [ "$(expr "${2}" : "^-")" = 0 ]; then
			check_three_or_four "${2}" || exit 1
		else
			# 引数必須の場合
			echo "${PROGNAME}: ${1} option requires an argument." 1>&2
			return 1
		fi
		;;
	-*)
		echo "${PROGNAME}: Invalid option -- '$(echo "${1}" | sed 's/^-*//')'" 1>&2
		echo "Try '${PROGNAME} --help' for more information." 1>&2
		exit 1
		;;
	*)
		# do something
		shift 1
		;;
	esac
done

EXP="s_(\n\t+[^\n]+)\n\t+_\1 _g"
DOTRETURN="s_(\n\t+)([^\n]+)\. +_\1\2\.\1_g"
cat - | sed -z -E --expression="s/‐\n\s+//g" --expression="s/ {2}/ /g" --expression="s/\n {4}/\n\t/g" --expression="s/\t {3}/\t\t/g" --expression="${EXP}" --expression="${EXP}" --expression="${EXP}" --expression="${DOTRETURN}" --expression="${DOTRETURN}" --expression="${DOTRETURN}" --expression="${DOTRETURN}" || exit 1
exit 0
