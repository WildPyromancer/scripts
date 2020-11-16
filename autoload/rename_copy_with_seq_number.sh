declare path_of_renamed_dir='./renamed'
declare digit_zerofill=3
declare -i flag_move=0
declare -i flag_initial_name=0

while [ -e "${path_of_renamed_dir}" ]; do
	path_of_renamed_dir+='_'
done

while [ $# -gt 0 ]; do
	case ${1} in

	--debug | -d)
		set -x
		;;
	--move | --mv | -m)
		flag_move=1
		;;
	--name | -n)
		flag_initial_name=1
		shift
		;;
	--zero | --digit | -z)
		if [[ "${2}" =~ "^[2-9]$" ]]; then
			digit_zerofill="${2}"
		else
			die '[ERROR] Invalid digit option [2-9]'
		fi
		shift
		;;
	*)
		echo "[ERROR] Invalid option '${1}'"
		usage
		exit 1
		;;
	esac
	shift
done

if [ flag_move ]; then
	declare CMD='mv -i -v'
else
	declare CMD='cp'
fi
declare -r REGEX_SPLITTER='\.\/\(.*\)\.\(.*\)'
declare -r ARG_INPUT='\1.\2'
if [ flag_initial_name ]; then
	declare -r ARG_OUTPUT="${path_of_renamed_dir}\/${2}\$(printf \"%0${digit_zerofill}d\n\" \"\${__global_counter}\").\2"
else
	# declare -r ARG_OUTPUT='"${path_of_renamed_dir}\/\1$(printf "%03d\n" "${__global_counter}").\2"'
	declare -r ARG_OUTPUT="${path_of_renamed_dir}\/\$(printf \"%0${digit_zerofill}d\n\" \"\${__global_counter}\").\2"
fi
declare -r INCREMENT_GCOUNTER='__global_counter=$((++__global_counter))'
# declare -r REGEX_REPLACER='cp \1.\2 ".\/renamed\/\1$(printf "%03d\n" "${__global_counter}").\2"; __global_counter=$((++__global_counter));'
declare -r REGEX_REPLACER="${CMD} ${ARG_INPUT} ${ARG_OUTPUT}; ${INCREMENT_GCOUNTER};"
declare -r STR_SED="s/${REGEX_SPLITTER}/${REGEX_REPLACER}/g"
if [ -v __global_counter ]; then
	die '[ERROR] Gloval variable "__global_counter" is already been declared.'
else
	export __global_counter=0
fi
mkdir "${path_of_renamed_dir}"
find . -maxdepth 1 -type f | sort | sed -e ${STR_SED} | zsh
unset __global_counter
trap 'unset __global_counter' 1 2 3 15
return 0
