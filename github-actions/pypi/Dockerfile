FROM python:3.7

LABEL "name"="pypi"
LABEL "maintainer"="Stan Chollet <stanislas.chollet@gmail.com>"
LABEL "version"="1.0.0"

LABEL "com.github.actions.name"="Pypi Release"
LABEL "com.github.actions.description"="Push package to pypi server."
LABEL "com.github.actions.icon"="upload"
LABEL "com.github.actions.color"="green"

RUN apt-get update && apt-get install -y cmake bison flex git jq

ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

RUN pyenv install $PYTHON_VERSION
RUN pyenv global $PYTHON_VERSION
RUN pip install --upgrade setuptools wheel twine

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]