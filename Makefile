.PHONY: init
init:
	git submodule update --init

.PHONY: install
install: init
	pip install -e .[test]

.PHONY: format-import
format-import:
	isort tartiflette/. tests/. setup.py

.PHONY: format
format: format-import
	black tartiflette tests setup.py

.PHONY: check-import
check-import:
	isort --check-only tartiflette/. tests/. setup.py

.PHONY: check-format
check-format:
	black --check tartiflette tests setup.py

.PHONY: style
style: check-format check-import
	pylint tartiflette --rcfile=pylintrc

.PHONY: test-unit
test-unit: clean
	mkdir -p reports
	pytest -s tests/unit --junitxml=reports/report_unit_tests.xml --cov . --cov-config .coveragerc --cov-report term-missing --cov-report xml:reports/coverage_func.xml $(EXTRA_ARGS)

.PHONY: test-functional
test-functional: clean
	mkdir -p reports
	pytest -s tests/functional --junitxml=reports/report_func_tests.xml --cov . --cov-config .coveragerc --cov-report term-missing --cov-report xml:reports/coverage_unit.xml $(EXTRA_ARGS)

.PHONY: test
test: test-unit test-functional

.PHONY: clean
clean:
	find . -name '*.pyc' -exec rm -fv {} +
	find . -name '__pycache__' -exec rm -frv {} +

.PHONY: set-dev-version
set-dev-version:
	bash -c "sed -i -e 's!^\(\s*_VERSION = \).*!\1\"$(shell $(MAKE) get-version).dev$(shell date +\"%s\")\"!' setup.py"

.PHONY: run-docs
run-docs:
	docker-compose up docs

.PHONY: get-version
get-version:
	@echo $(shell cat setup.py | grep "_VERSION =" | egrep -o '[0-9]+\.[0-9]+\.[0-9]+(rc[0-9]+)?')
