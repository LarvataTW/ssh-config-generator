# Using bash
SHELL := /bin/bash

# One worker at the time
MAKEFLAGS = --jobs=1

.PHONY: init
init: ## 初始化運作環境
	mkdir -p output/
	pip3 install -r requirements.txt

.PHONY: update
update: ## 更新 config 檔案
	$(MAKE) init
	python3 generator.py -y vars/your.servers.yaml # 預設產出 SSH config 檔案
	python3 generator.py -y vars/your.servers.yaml -t templaes/ssh.j2 -o path/to/your/ssh/config
	python3 generator.py -y vars/your.servers.yaml -t templates/ansible.j2 -o path/to/your/ansible/inventories/hosts

# Absolutely awesome: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
