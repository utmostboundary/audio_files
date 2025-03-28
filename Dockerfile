FROM python:3.12

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4.0

RUN pip install "setuptools"
RUN pip install "poetry==$POETRY_VERSION"
RUN pip install "typing_extensions"

WORKDIR /audio_files
COPY ../poetry.lock pyproject.toml /audio_files/

RUN poetry config installer.max-workers 10
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY .. /audio_files
RUN chmod -R 0777 /audio_files

RUN adduser --disabled-password docker-admin
USER docker-admin