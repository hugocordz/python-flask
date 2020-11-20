FROM python:alpine3.8
COPY . /app
WORKDIR /app
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip install -r requirements.txt
CMD python ./app.py