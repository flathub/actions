#!/bin/bash

if [[ -z "$GITHUB_WORKSPACE" || -z "$GITHUB_REPOSITORY" ]]; then
    echo "Script is not running in GitHub Actions CI"
    exit 1
fi

cd $GITHUB_WORKSPACE

APP_ID=${GITHUB_REPOSITORY#flathub/}
if [[ -f ${APP_ID}.yml ]]; then
    manifest=${APP_ID}.yml
elif [[ -f ${APP_ID}.yaml ]]; then
    manifest=${APP_ID}.yaml
elif [[ -f ${APP_ID}.json ]]; then
    manifest=${APP_ID}.json
else
    echo "Couldn't find manifest file"
    exit 1
fi

git config user.name "flathubbot" && \
git config user.email "sysadmin@flathub.org"

/opt/flatpak-external-data-checker/flatpak-external-data-checker --update $manifest
