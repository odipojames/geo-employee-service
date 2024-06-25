FROM python:3.9.0

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 8001

ENTRYPOINT [ "/app/build.sh" ]