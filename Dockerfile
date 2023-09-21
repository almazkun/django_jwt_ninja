FROM python:3.11-slim

LABEL org.opencontainers.image.source=https://github.com/almazkun/django_jwt_ninja

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY ./Pipfile ./Pipfile.lock ./

RUN pip3 install pipenv && pipenv install --system

COPY apps ./apps
COPY api ./api
COPY settings ./settings
COPY manage.py ./

ENTRYPOINT [ "python3" ]

CMD [ "manage.py", "runserver", "0.0.0.0:8000" ]