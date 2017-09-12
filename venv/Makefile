setup:
	test -d bin || python -m venv .
	bin/pip install -r requirements.txt -r requirements-dev.txt -c constraints.txt

freeze:
	bin/pip freeze | grep -v -F 'git+' > constraints.txt
