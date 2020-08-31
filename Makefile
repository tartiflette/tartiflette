SET_ALPHA_VERSION = 0
PKG_VERSION := $(shell cat setup.py | grep "_VERSION =" | egrep -o '[0-9]+\.[0-9]+\.[0-9]+(rc[0-9]+)?')

REF := $(shell cat /github/workflow/event.json | jq ".ref")

ifneq ($(REF),"refs/heads/master")
PKG_VERSION := $(shell echo | awk -v pkg_version="$(PKG_VERSION)" -v build_number="$(shell date +\"%s\")" '{print pkg_version "dev" build_number}')
SET_ALPHA_VERSION = 1
endif

PATH_TO_MAKEFILE := /github/workspace/Makefile
ifneq ("$(wildcard $(PATH_TO_MAKEFILE))","")
IN_GITHUB_ACTION := 1
else
IN_GITHUB_ACTION := 0
endif

.PHONY: init
init:
	git submodule init
	git submodule update

.PHONY: install
install: init
	pip install -e .[test]

.PHONY: format-import
format-import:
	isort tartiflette/. tests/. setup.py

.PHONY: format
format: format-import
	black -l 79 --target-version py36 tartiflette tests setup.py

.PHONY: check-import
check-import:
	isort --check-only tartiflette/. tests/. setup.py

.PHONY: check-format
check-format:
	black -l 79 --target-version py36 --check tartiflette tests setup.py

.PHONY: style
style: check-format check-import
	pylint tartiflette --rcfile=pylintrc
ifeq ($(IN_GITHUB_ACTION),1)
	make clean
endif

.PHONY: test-integration
test-integration: clean
	true

.PHONY: test-unit
test-unit: clean
ifeq ($(IN_GITHUB_ACTION),1)
	make install
endif
	mkdir -p reports
	py.test -s tests/unit --junitxml=reports/report_unit_tests.xml --cov . --cov-config .coveragerc --cov-report term-missing --cov-report xml:reports/coverage_func.xml $(EXTRA_ARGS)
ifeq ($(IN_GITHUB_ACTION),1)
	make clean
endif

.PHONY: test-functional
test-functional: clean
ifeq ($(IN_GITHUB_ACTION),1)
	make install
endif
	mkdir -p reports
	py.test -s tests/functional --junitxml=reports/report_func_tests.xml --cov . --cov-config .coveragerc --cov-report term-missing --cov-report xml:reports/coverage_unit.xml $(EXTRA_ARGS)
ifeq ($(IN_GITHUB_ACTION),1)
	make clean
endif

.PHONY: test
test: test-integration test-unit test-functional

.PHONY: clean
clean:
	find . -name '*.pyc' -exec rm -fv {} +
	find . -name '*.pyo' -exec rm -fv {} +
	find . -name '__pycache__' -exec rm -frv {} +

.PHONY: set-version
set-version:
ifneq ($(SET_ALPHA_VERSION), 0)
	bash -c "sed -i \"s@_VERSION[ ]*=[ ]*[\\\"\'][0-9]\+\\.[0-9]\+\\.[0-9]\+\(rc[0-9]\+\)\?[\\\"\'].*@_VERSION = \\\"$(PKG_VERSION)\\\"@\" setup.py"
endif

.PHONY: run-docs
run-docs:
	docker-compose up docs

.PHONY: get-version
get-version:
	@echo $(PKG_VERSION)

.PHONY: get-last-released-changelog-entry
get-last-released-changelog-entry:
	@cat changelogs/$(PKG_VERSION).md

.PHONY: github-action-version-and-changelog
github-action-version-and-changelog:
	echo $(PKG_VERSION) > $(HOME)/name
	echo $(PKG_VERSION) > $(HOME)/tag
	@cp changelogs/$(PKG_VERSION).md $(HOME)/changelog
