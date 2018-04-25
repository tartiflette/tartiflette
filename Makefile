
.PHONY: format
format:
	yapf -i -vv -r tartiflette

.PHONY: check-format
check-format:
	yapf -d -vv -r tartiflette

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
	py.test -s tests/unit --junitxml=reports/report_unit_tests.xml --cov . --cov-config .coveragerc --cov-report term-missing --cov-report xml:reports/coverage.xml

.PHONY: test-func
test-func:
	mkdir -p reports
	py.test -s tests/functional --junitxml=reports/report_func_tests.xml --cov . --cov-config .coveragerc --cov-report term-missing --cov-report xml:reports/coverage.xml

.PHONY: tests
tests: test-integ test-unit test-func

.PHONY: quality
quality: style complexity tests
