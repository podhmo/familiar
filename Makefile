gen:
	venv/bin/designer design/main.yaml | bash -x

clean:
	rm -rf gen/*

setup:
	$(MAKE) -C venv setup
	go get -v golang.org/x/tools/cmd/goimports

install:
	go install -v ./cmd/...

run:
	familiar
