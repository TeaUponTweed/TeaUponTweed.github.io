.PHONY: clean compile inline upload freeze install polish

MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

clean:
	rm -f $(MAKEFILE_DIR)/src/derivativeworksblog/static/*.html

compile: clean
	compile-all -p $(MAKEFILE_DIR)/src/derivativeworksblog/posts/ -o $(MAKEFILE_DIR)/src/derivativeworksblog/static/

inline: compile
	@for file in $(MAKEFILE_DIR)/src/derivativeworksblog/static/*.html; do \
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

polish:
	black src
	isort src

serve: inline
	gunicorn -b 0.0.0.0:5556 derivativeworksblog.app:app
