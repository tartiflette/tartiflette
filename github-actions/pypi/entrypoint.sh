#!/bin/bash

if [ -d "./libgraphqlparser" ]; then
	rm -rf ./libgraphqlparser
fi

make init

set_version_if_not_master() {
	cat /github/workflow/event.json | jq -e '. | select(.ref=="refs/heads/master")'
	return_code=$?

	if [ $return_code -ne 0 ]; then
		export TWINE_REPOSITORY_URL="https://test.pypi.org/legacy/"
		make set-version
	fi
} 

check_if_setup_file_exists() {
	if [ ! -f setup.py ]; then
		echo "setup.py must exist in the directory that is being packaged and published."
		exit 1
	fi
}

upload_package() {
	python setup.py sdist
	twine upload dist/*
}

set_version_if_not_master

make get-version

check_if_setup_file_exists
upload_package