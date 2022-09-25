FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir -U pip setuptools wheel

COPY . .

RUN pip install --no-cache-dir -e .

RUN python ./src/derivativeworksblog/complie_all.py ./src/derivativeworksblog/posts/ ./src/derivativeworksblog/static/

ENV PYTHONUNBUFFERED=.

ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5556", "derivativeworksblog.app:app"]
