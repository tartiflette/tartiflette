#!/bin/sh

set -e

_PATH_TAG="${HOME}/tag"
_PATH_USERNAME="${HOME}/username"
_PATH_REPOSITORY="${HOME}/repository"
_PATH_CHANGELOG="${HOME}/changelog"
_PATH_NAME="${HOME}/name"

if [ -f $_PATH_TAG ]; then
    TAG=$(cat $_PATH_TAG)
fi

if [ -f $_PATH_USERNAME ]; then
    USERNAME=$(cat $_PATH_USERNAME)
fi

if [ -f $_PATH_REPOSITORY ]; then
    REPOSITORY=$(cat $_PATH_REPOSITORY)
fi

if [ -f $_PATH_NAME ]; then
    NAME=$(cat $_PATH_NAME)
fi

echo "---------------------------"
echo "TAG: $TAG"
echo "REPOSITORY: $REPOSITORY"
echo "USERNAME: $USERNAME"
echo "NAME: $NAME"
echo "---------------------------"

if [ -f $_PATH_CHANGELOG ]; then
    echo "Release with changelog"
    desc=$(cat _PATH_CHANGELOG)
    github-release release \
        --user $USERNAME \
        --repo $REPOSITORY \
        --tag $TAG \
        --name $NAME \
        --description "${desc}"
else
    echo "Release without changelog"
    github-release release \
        --user $USERNAME \
        --repo $REPOSITORY \
        --tag $TAG \
        --name $NAME
fi