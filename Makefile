SET_ALPHA_VERSION = 0
PKG_VERSION := $(shell cat setup.py | grep "_VERSION =" | egrep -o "([0-9]+\\.[0-9]+\\.[0-9]+)")
ifneq ($(and $(TRAVIS_BRANCH),$(TRAVIS_BUILD_NUMBER)),)
ifneq ($(TRAVIS_BRANCH), master)
PKG_VERSION := $(shell echo | awk -v pkg_version="$(PKG_VERSION)" -v travis_build_number="$(TRAVIS_BUILD_NUMBER)" '{print pkg_version "a" travis_build_number}')
SET_ALPHA_VERSION = 1
endif
endif

.PHONY: init
init:
	git submodule init
	git submodule update

.PHONY: format-import
format-import:
	isort -rc tartiflette/. tests/. setup.py

.PHONY: format
format: format-import
	black -l 79 --py36 tartiflette tests setup.py

.PHONY: check-import
check-import:
	isort --check-only -rc tartiflette/. tests/. setup.py

.PHONY: check-format
check-format:
	black -l 79 --py36 --check tartiflette tests setup.py

.PHONY: style
style: check-format check-import
	pylint tartiflette --rcfile=pylintrc

.PHONY: complexity
complexity:
	xenon --max-absolute B --max-modules B --max-average A tartiflette

.PHONY: test-integration
test-integration: clean
	true

.PHONY: test-unit
test-unit: clean
	mkdir -p reports
	py.test -s tests/unit --junitxml=reports/report_unit_tests.xml --cov . --cov-config .coveragerc --cov-report term-missing --cov-report xml:reports/coverage_func.xml $(EXTRA_ARGS)

.PHONY: test-functional
test-functional: clean
	mkdir -p reports
	py.test -s tests/functional --junitxml=reports/report_func_tests.xml --cov . --cov-config .coveragerc --cov-report term-missing --cov-report xml:reports/coverage_unit.xml $(EXTRA_ARGS)

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
	bash -c "sed -i \"s@_VERSION[ ]*=[ ]*[\\\"\'][0-9]\+\\.[0-9]\+\\.[0-9]\+[\\\"\'].*@_VERSION = \\\"$(PKG_VERSION)\\\"@\" setup.py"
endif

.PHONY: run-docs
run-docs:
	docker-compose up docs

.PHONY: git-tag
git-tag:
ifeq ($(TRAVIS_BRANCH), master)
	git config --local user.name "dm-tartiflette-release-travis"
	git config --local user.email "dm-tartiflette-release-travis@dailymotion.com"
	git tag $(PKG_VERSION)
	@git push -q https://dm-tartiflette-release-travis:$(GITHUBTOKEN)@github.com/dailymotion/tartiflette.git $(PKG_VERSION)
endif

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

.PHONY: build-artifact
build-artifact: init
	pip install -e .[test]
