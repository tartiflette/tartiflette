---
id: use-with-docker
title: Use with Docker
sidebar_label: 14. Use with Docker
---

For those who want to use **Tartiflette** within a docker image, you can find a `Dockerfile` sample below.

Create a `Dockerfile` at the root level of your **Recipes Manager GraphQL API**.

This `Dockerfile` includes:
* pipenv
* **tartiflette** dependencies `cmake`, `bison` and `flex`

```dockerfile
FROM python:3.7.2

RUN apt-get update && apt-get install -y cmake bison flex

RUN pip install --user pipenv

ENV PYTHONPATH=/usr/src/app/
ENV PATH="$PATH:/root/.local/bin"

WORKDIR /usr/src/app

COPY Pipfile /usr/src/app/
COPY Pipfile.lock /usr/src/app/

ARG parameters=install
RUN pipenv "${parameters}"

COPY . /usr/src/app/

EXPOSE 8080

CMD [ "pipenv", "run", "python", "-m", "recipes_manager" ]
```
