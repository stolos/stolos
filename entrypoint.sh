#!/bin/bash
set -e

function check_port() {
	local host=${1} && shift
	local port=${1} && shift
	local retries=5
	local wait=1

	until( $(nc -zv ${host} ${port}) ); do
		((retries--))
		if [ $retries -lt 0 ]; then
			echo "Service ${host} didn't become ready in time."
			exit 1
		fi
		sleep "${wait}"
	done
}

a=${DATABASE_URL##*//}
check_port "${a%%:*}" "5432"
a=${REDIS_URL##*//}
check_port "${a%%:*}" "6379"

exec "$@"
