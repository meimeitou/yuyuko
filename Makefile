ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

help:          ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

venv:          ## enter test env.
	@./manager.sh venv

pro-venv:       ## enter product env.
	@./manager.sh pro-venv

base:
	@docker build -t hub.dns.360.cn/dns/yuyuko:base -f Docker-base .

image:
	@docker build -t hub.dns.360.cn/dns/yuyuko:latest .

dev:          ## run flask
	@DEBUG=true python yuyuko.py

pro:
	gunicorn -c gunicorn_config.py yuyuko:app --timeout 90 --log-level debug --worker-class gevent -w 1
