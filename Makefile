all: install

.PHONY: install
install:
	pip install -e .

.PHONY: test
test:
	pytest

.PHONY: build
build:
	python setup.py sdist bdist_wheel

.PHONY: deploy
deploy: build
	twine upload dist/*
	rm -rf build dist
