.PHONY: test coverage clean build publish

test:
	python -m pytest tests/

coverage:
	python -m pytest tests/ --cov=rison --cov-report=term-missing

clean:
	rm -rf dist/ build/ *.egg-info

build: clean
	python -m build

publish: build
	twine upload dist/*
