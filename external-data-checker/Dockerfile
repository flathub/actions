FROM debian:buster
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y bubblewrap git gir1.2-glib-2.0 gir1.2-json-1.0 \
        python3-apt python3-gi python3-github python3-ruamel.yaml \
        python3-tenacity && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN git config --global user.name "flathubbot" && \
    git config --global user.email "sysadmin@flathub.org"

RUN git clone https://github.com/endlessm/flatpak-external-data-checker /opt/flatpak-external-data-checker

ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
