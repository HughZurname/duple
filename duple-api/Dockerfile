FROM python:3.7.6-stretch

WORKDIR /app/

COPY . .

RUN pip install .

CMD [ "python", "-m", "duple", "-s" ]
