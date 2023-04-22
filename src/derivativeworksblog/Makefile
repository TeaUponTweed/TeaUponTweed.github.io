.PHONY: clean compile inline upload install

MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

clean:
	rm -f $(MAKEFILE_DIR)/static/*.html

compile: clean
	compile-all -p $(MAKEFILE_DIR)/posts/ -o $(MAKEFILE_DIR)/static/

inline: compile
	@for file in $(MAKEFILE_DIR)/static/*.html; do \
		echo "Inlining $$file..."; \
		inliner -i $$file > $${file%.html}.min.html; \
		mv $${file%.html}.min.html $$file; \
	done

upload: inline
	rsync -arvz ~/code/TeaUponTweed.github.io/ --exclude python_venv --exclude .git --exclude __pycache__/ mbm:mbmblog/

freeze:
	pip install -U pip-tools
	pip-compile --resolver=backtracking

install:
	pip install -U pip setuptools wheel
	pip install -U -r dev-requirements.txt
	pip install -r requirements.txt
	pip install -e .
