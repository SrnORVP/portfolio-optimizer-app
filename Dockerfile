

ARG PYTHON_VERSION=3.11.9

FROM python:alpine as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY req.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r req.txt

COPY ./py-app py-app
CMD python py-app/flask.py

############################################################

# RUN --mount=type=cache,target=/root/.cache/pip \
#     --mount=type=bind,source=requirements.txt,target=requirements.txt \
#     python -m pip install -r requirements.txt

# EXPOSE 8000
# CMD gunicorn 'myapp.example:app' --bind=0.0.0.0:8000

############################################################
# FROM rust:alpine as base
# RUN cargo build --manifest-path ./rs/src/main.rs
