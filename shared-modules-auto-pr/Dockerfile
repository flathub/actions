FROM fedora:31

RUN dnf install -y git python3-pyyaml python3-pygit2 python3-pygithub \ 
    json-glib gobject-introspection python3-gobject

RUN git config --global user.name "flathubbot"
RUN git config --global user.email "sysadmin@flathub.org"

ADD entrypoint.py /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]
