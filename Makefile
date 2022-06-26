.PHONY: compile upload

compile:
	python_venv/bin/python complie_all.py

upload: compile
	rsync -arvz ~/code/TeaUponTweed.github.io/ --exclude python_venv --exclude .git --exclude __pycache__/ mbm:mbmblog/
