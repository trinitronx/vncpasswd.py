FROM python:2.7-alpine
COPY . /src/vncpasswd.py
WORKDIR /src/vncpasswd.py
ENTRYPOINT ["/src/vncpasswd.py/vncpasswd.py"]
