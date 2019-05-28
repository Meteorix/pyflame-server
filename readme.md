pyflame-server
==============

A webservice to facilate the use of [pyflame](https://github.com/Meteorix/pyflame)

[Pyflame解析和扩展](https://github.com/Meteorix/meteorix-blog/blob/master/_posts/pyflame.md)

# Installation

```shell
pip install -r requirements.txt
python wsgi.py
```

visit http://172.22.22.230:5000/

> change '172.22.22.230' to your server ip

# Usage

1 get pyflame for py2.6 py2.7 py3.4 py3.5 py3.6 py3.7
``` shell
curl -o pyflame http://172.22.22.230:5000/pyflame ; chmod +x pyflame
```

2.1 start python to profile
```shell
./pyflame -t python3.6 -c "print(sum(i for i in range(1000000)))" > profile.txt
```

2.2 or attach python pid to profile, -s seconds -p pid, reference
```shell
sudo ./pyflame -s 5 -p 28947 > profile.txt
```

3 upload to pyflame-server
```shell
curl -F "file=@profile.txt" http://172.22.22.230:5000/upload
```

4 visit the url printed by curl, samples here

# My fork of Pyflame

Since the author of [uber/pyflame](https://github.com/uber/pyflame) no longer works at uber, the official repo is not well maintained. I forked to [Meteorix/pyflame](https://github.com/Meteorix/pyflame) and did the following things:

1. Merge PR of py3.7 support
1. Merge PR of anaconda fix
1. Fix py2.7 build script
1. Add Dockerfile to build pyflame which enables py2.6/py2.7/py3.4/py3.5/py3.6/py3.7 support
1. Add c/c++ stack profile
