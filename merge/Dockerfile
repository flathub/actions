FROM alpine:edge

LABEL version="1.0.0"
LABEL repository="http://github.com/flathub-actions/merge-app"
LABEL homepage="http://github.com/flathub-actions/merge-app"
LABEL maintainer="Bartłomiej Piotrowski"
LABEL "com.github.actions.name"="Merge new Flathub application"
LABEL "com.github.actions.description"="Imports new application from PR to Flathub"
LABEL "com.github.actions.icon"="git-pull-request"
LABEL "com.github.actions.color"="blue"

RUN apk add --no-cache flatpak-builder git python3 py3-requests py3-pygit2 py3-yaml && \
    python3 -m pip install pygithub
ADD entrypoint.py /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]
