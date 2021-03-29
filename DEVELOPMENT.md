# Development

```shell
cde sdk use python_v3.9
pip3 install configobj distro redis
```

## Test

```shell
python3 test.py
```

## Create package

```shell
python3 setup.py sdist
```

## Create package & deploy to pypi

```shell
python3 setup.py sdist upload -r http://pypi-repo.onet/pypi/
```

## Install package

```shell
pip3 install --no-binary :all: diamond-next-4.0.899.tar.gz
```
