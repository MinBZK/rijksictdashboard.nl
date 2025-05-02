FROM base_backend AS buildstep

COPY pyproject.toml poetry.lock alembic.ini /backend/
COPY ./app /backend/app/
COPY ./tests /backend/tests/
COPY ./alembic /backend/alembic/
COPY ./common /backend/common/

WORKDIR /backend/

RUN poetry install

FROM ubuntu:22.04

# Install runtime dependencies and remove build dependencies
RUN apt-get update && apt-get install sqlite3 libexpat1 -y && \
    apt-get remove --purge -y build-essential gcc g++ make cmake autoconf automake libtool pkg-config perl python3-dev git bison flex zlib1g-dev libssl-dev curl wget &&\
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install PSQL, needed for tests
RUN apt-get update && apt-get install postgresql-client -y

# Verify PSQL installed successfully
RUN psql --version

# Copy app folder
COPY --from=buildstep /backend /backend

# Copy tooling
COPY --from=buildstep /usr/local/bin /usr/local/bin

# Copy Python binaries
COPY --from=buildstep /usr/local/lib /usr/local/lib
RUN ln -f -s /usr/bin/python3.11 /usr/bin/python3
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python3.11/site-packages"


WORKDIR /backend/
