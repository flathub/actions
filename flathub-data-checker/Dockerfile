FROM debian:buster as unappimage
RUN apt-get update && \
    env DEBIAN_FRONTEND=noninteractive apt-get install -y make gcc git libelf-dev && \
    git clone https://github.com/refi64/unappimage && \
    cd unappimage && make -C squashfs-tools -j$(nproc)

FROM debian:buster
ARG DEBIAN_FRONTEND=noninteractive

COPY --from=unappimage /unappimage/squashfs-tools/unappimage /usr/local/bin/

RUN apt-get update && \
    apt-get install -y bubblewrap git gir1.2-glib-2.0 gir1.2-json-1.0 \
        parallel python3-apt python3-gi python3-github python3-ruamel.yaml \
        python3-tenacity && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN git clone https://github.com/flathub/flatpak-external-data-checker /opt/flatpak-external-data-checker

ADD gh-ls-org /usr/local/bin/gh-ls-org
ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
