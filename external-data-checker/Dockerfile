FROM ghcr.io/flathub/flatpak-external-data-checker:latest

ADD gh-ls-org /usr/local/bin/gh-ls-org
ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
