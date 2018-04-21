.PHONY: build install dist srpm rpm pypi clean

PYTHON        ?= python3
INSTALL_FLAGS ?=

NAME          := logulife


install:
	$(PYTHON) setup.py install --skip-build $(INSTALL_FLAGS)

dist: clean
	$(PYTHON) setup.py sdist
	mv dist/$(NAME)-*.tar.gz .

clean:
	rm -rf build dist $(NAME)-*.tar.gz $(NAME).egg-info
