#!/bin/bash

go_to_build_dir(){
	if [ ! -z $SUBDIR ]; then
		cd $SUBDIR
	fi
}

check_if_setup_file_exists(){
	if [ ! -f setup.py ]; then
		echo "setup.py must exist in the directory that is being packaged and published."
		exit 1
	fi
}

upload_package(){
	python setup.py sdist
	twine upload dist/*
}

go_to_build_dir
check_if_setup_file_exists
upload_package