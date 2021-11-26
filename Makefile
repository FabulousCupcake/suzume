NO_COLOR=\033[0m
OK_COLOR=\033[32;01m
ERROR_COLOR=\033[31;01m
WARN_COLOR=\033[33;01m

.PHONY: all add-analytics append-timestamp build build-json clean

all: clean build
	@echo "$(OK_COLOR)==> Done!$(NOCOLOR)"

build: clean prepare-deps
	@echo "$(OK_COLOR)==> Building zip file $(NO_COLOR)"
	@zip -r func.zip priconne python *.py

prepare-deps:
	@echo "$(OK_COLOR)==> Preparing deps $(NO_COLOR)"
	@pip install -r requirements.txt -t python

clean:
	@echo "$(OK_COLOR)==> Cleaning project… $(NO_COLOR)"
	@rm -rf func.zip
	@rm -rf python
