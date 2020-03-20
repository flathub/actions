FROM archlinux

RUN pacman -Syu --noconfirm flatpak-builder git python-requests python-yaml \
        python-pygit2 python-pygithub python-pip && \
    pip install cached-property
ADD entrypoint.py /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]
