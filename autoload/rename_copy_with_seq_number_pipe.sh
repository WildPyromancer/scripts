declare -r input=$(
	if [ -p /dev/stdin ]; then
		cat -
	else
		echo $@
	fi
)
export __global_counter=0
mkdir ./renamed
declare -r REGEX_FILE_NAME_SUFFIX='\(\.\/\)?\(.*\)\.\(\w+\)'
echo $input | sed -e 's/\.\/\(.*\)\.\(.*\)/cp \1.\2 ".\/renamed\/\1$(printf "%03d\n" "${__global_counter}").\2";__global_counter=$((++__global_counter))/g' | zsh
# echo $input | sed -e 's/\.\/\(.*\)\.\(.*\)/cp \1.\2 ".\/renamed\/\1$(printf "%03d\n" "${__global_counter}").\2";__global_counter=$((++__global_counter))/g' | zsh
unset __global_counter
trap 'unset __global_counter' 1 2 3 15
return 0
