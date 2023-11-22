FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /megano

RUN pip install --upgrade pip "poetry==1.7.1"

RUN poetry config virtualenvs.create false --local

COPY pyproject.toml poetry.lock ./

# RUN poetry install
RUN poetry install --only main

COPY . /megano/

CMD [ "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000" ]