ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION} as base

WORKDIR /app

FROM base as builder

WORKDIR /install
COPY . .
RUN pip3 install .

FROM base as runtime

COPY --from=builder /usr/local/ /usr/local
COPY . .

ENV GUNICORN_CMD_ARGS "--bind=0.0.0.0:5000 --workers=2"
CMD [ "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "diceroller:app"]
