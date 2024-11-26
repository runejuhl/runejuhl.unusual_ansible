version = $(shell yq .version < galaxy.yml)
target = build/runejuhl-unusual_ansible-$(version).tar.gz

build: $(target)

$(target): $(wildcard *.md *.py *.yml requirements.txt)
	ansible-galaxy collection build --force --output-path build/
