# yuyuko

- 二维码读取
- 二维码生成
- 二维码传数据

## develop

auto open browser:
```shell
# mac
brew install --cask chromedriver
# ubuntu
sudo apt install chromium-chromedriver
```

```shell
# enter env
make venv
# run
make dev
```

## ref

https://github.com/greyli/bootstrap-flask
https://bootstrap-flask.readthedocs.io/en/stable/

## problems

- 无法打开“chromedriver”，因为无法验证开发者

```shell
cd /usr/local/bin/
xattr -d com.apple.quarantine chromedriver
```
