FROM python:3.7.2

LABEL "name"="python"
LABEL "maintainer"="Stan Chollet <stanislas.chollet@gmail.com>"
LABEL "version"="1.0.0"

LABEL "com.github.actions.name"="Python container"
LABEL "com.github.actions.description"="Execute python code into a docker image."
LABEL "com.github.actions.icon"="sunset"
LABEL "com.github.actions.color"="purple"

RUN apt-get update && apt-get install -y cmake bison flex git

ENV PYTHONPATH=/github/workspace/

WORKDIR /github/workspace
