FROM redhat/ubi8

ARG BUILDREQUIRES='python39-devel gcc libpq-devel libffi-devel openssl-devel rust cargo'
RUN dnf -y install \
    gettext \
    glibc-langpack-en \
    make \
    openssh-clients \
    python39 \
    $BUILDREQUIRES &&\
    dnf clean all
RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:${PATH}"

# RUN pip install --upgrade pip

WORKDIR /app
COPY requirements.txt .
#RUN python3 -m setuptools
RUN pip install --require-hashes --no-binary :all: -r requirements.txt

# Create /etc/ssl/qpc
RUN mkdir -p /etc/ssl/qpc/
COPY deploy/ssl/* /etc/ssl/qpc/

# Create /deploy
RUN mkdir -p /deploy
COPY deploy/gunicorn.conf.py  /deploy
COPY deploy/docker_run.sh  /deploy
COPY deploy/server_run.sh  /deploy
COPY deploy/setup_user.py  /deploy

# Create log directories
RUN mkdir -p /var/log/supervisor/
VOLUME /var/log

# Create /var/data
RUN mkdir -p /var/data
VOLUME /var/data

# Create /etc/ansible/roles/
RUN mkdir -p /etc/ansible/roles/
COPY quipucords/scanner/network/runner/roles/ /etc/ansible/roles/
VOLUME /etc/ansible/roles/

# Copy server code
COPY . .
RUN pip install .

# Set production environment
ARG BUILD_COMMIT=master
ENV QUIPUCORDS_COMMIT=$BUILD_COMMIT
ENV PRODUCTION=True
ENV DJANGO_SECRET_PATH=/var/data/secret.txt
ENV DJANGO_DB_PATH=/var/data/
ENV DJANGO_DEBUG=False
ENV DJANGO_LOG_LEVEL=INFO
ENV DJANGO_LOG_FORMATTER=verbose
ENV DJANGO_LOG_HANDLERS=console,file
ENV DJANGO_LOG_FILE=/var/log/app.log
ENV QUIPUCORDS_LOGGING_LEVEL=INFO
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV PYTHONPATH=/app/quipucords

# Initialize database & Collect static files
RUN make server-static
RUN ls -lta /var/data

WORKDIR /var/log

EXPOSE 443
CMD ["/bin/bash", "/deploy/docker_run.sh"]