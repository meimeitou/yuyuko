FROM hub.dns.360.cn/dns/yuyuko:base

COPY . /workspace
ENV LANG=en_US.UTF-8
ENV PATH=/workspace/.venv/bin:$PATH

CMD ["gunicorn","-c","gunicorn_config.py","yuyuko:app", "--worker-class","gevent", "-w". "1"]
