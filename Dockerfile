FROM archlinux/base

LABEL version="1.0.0"
LABEL repository="http://github.com/flathub-actions/merge-app"
LABEL homepage="http://github.com/flathub-actions/merge-app"
LABEL maintainer="Bartłomiej Piotrowski"
LABEL "com.github.actions.name"="Merge new Flathub application"
LABEL "com.github.actions.description"="Imports new application from PR to Flathub"
LABEL "com.github.actions.icon"="git-pull-request"
LABEL "com.github.actions.color"="blue"

RUN pacman -Syu --noconfirm flatpak-builder git python python-pygithub python-requests python-pygit2
ADD entrypoint.py /entrypoint.py
ENTRYPOINT ['/entrypoint.py']
