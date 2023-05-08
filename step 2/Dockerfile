FROM python:3.8-slim

ENV SERVER_PORT=12345
ENV EXPIRE_MINS=5
ENV ENDPOINT_NAME="shortner"
ENV APILAYER_API="8N9yCSt5abnlzXuz1hLKJheipuK2tdrt"
ENV APILAYER_URL="https://api.apilayer.com/short_url/hash"

WORKDIR /code
COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "app.py" ]