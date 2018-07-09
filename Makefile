
.PHONY: format
format:
	black -l 79 --py36 tartiflette setup.py

.PHONY: check-format
check-format:
	black -l 79 --py36 --check tartiflette setup.py

.PHONY: style
style: check-format
	pylint tartiflette --rcfile=pylintrc

.PHONY: complexity
complexity:
	xenon --max-absolute B --max-modules B --max-average A tartiflette

.PHONY: test-integ
test-integ:
	true

.PHONY: test-unit
test-unit:
	mkdir -p reports
	py.test -s tests/unit --junitxml=reports/report_unit_tests.xml --cov . --cov-config .coveragerc --cov-report term-missing --cov-report xml:reports/coverage_func.xml

.PHONY: test-func
test-func:
	mkdir -p reports
	py.test -s tests/functional --junitxml=reports/report_func_tests.xml --cov . --cov-config .coveragerc --cov-report term-missing --cov-report xml:reports/coverage_unit.xml

.PHONY: tests
tests: test-integ test-unit test-func

.PHONY: quality
quality: style complexity tests
