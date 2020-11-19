(
	declare -r REGEX="(\d{3,4})x(\d{3,4})"
	find '.' -maxdepth 1 -type f | grep -e "\.jpg|\.png" | while read -r FILE; do
		if [[ $(identify "${FILE}") =~ ${REGEX} ]]; then
			echo -n "${match}[1] x ${match}[2]"
			if [ "${match}[1]" = "${match}[2]" ]; then
				echo "square"
				convert -size 256x256 "${FILE}" "${FILE}"
			else
				echo "not square"
				convert -size 256x256! "${FILE}" "${FILE}"
			fi
			convert -type grayscale "${FILE}" "${FILE}"
		else
			echo "[${FILE}] may be not image FILE."
		fi
	done
)
return 0
