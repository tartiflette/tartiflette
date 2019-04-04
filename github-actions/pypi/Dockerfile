FROM python:3.7.2

LABEL "name"="pypi"
LABEL "maintainer"="Stan Chollet <stanislas.chollet@gmail.com>"
LABEL "version"="1.0.0"

LABEL "com.github.actions.name"="Pypi Release"
LABEL "com.github.actions.description"="Push package to pypi server."
LABEL "com.github.actions.icon"="upload"
LABEL "com.github.actions.color"="green"

RUN apt-get update && apt-get install -y cmake bison flex git jq

RUN pip install --upgrade setuptools wheel twine

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

WORKDIR /github/workspace

ENTRYPOINT ["/entrypoint.sh"]