gen:
	venv/bin/designer design/main.yaml | bash -x

setup:
	$(MAKE) -C venv setup
