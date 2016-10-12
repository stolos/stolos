#!/bin/bash
set -e

function check_port() {
	local host=${1} && shift
	local port=${1} && shift
	local retries=10
	local wait=2

	until( $(nc -zv ${host} ${port}) ); do
		((retries--))
		if [ $retries -lt 0 ]; then
			echo "Service ${host} didn't become ready in time."
			exit 1
		fi
		sleep "${wait}"
	done
}

tmp=${DATABASE_URL##*@}
check_port "${tmp%%:*}" "5432"
tmp=${REDIS_URL##*//}
check_port "${tmp%%:*}" "6379"

exec "$@"
