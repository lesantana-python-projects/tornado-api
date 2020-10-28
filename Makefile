clean:
	@echo "Execute cleaning ..."
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
	rm -f coverage.xml

pep8:
	@find . -type f -not -name "*manager.py*" -not -path "*./.venv/*" -name "*.py"|xargs flake8 --max-line-length=130 --ignore=E402 --max-complexity=6

tests: clean pep8
	py.test tests

test-coverage:clean pep8
	py.test --cov=weather --cov-report=xml tests/unit

test-sonar: test-coverage
	sonar-scanner -Dsonar.sources=.
