FROM fedora:33

RUN dnf install -y flatpak-builder git python3-requests python3-pyyaml \
        python3-pygit2 python3-pygithub && \
    dnf clean all
ADD entrypoint.py /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]
