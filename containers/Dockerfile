FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir -U pip setuptools wheel

COPY . .

RUN pip install --no-cache-dir -e .

RUN cd ./src/derivativeworksblog && compile-all -p posts/ -o static/ && cd -

ENV PYTHONUNBUFFERED=.

ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5556", "derivativeworksblog.app:app"]
