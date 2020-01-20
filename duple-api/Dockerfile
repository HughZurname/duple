FROM python:3.7.6-stretch

WORKDIR /app/

COPY . .

RUN pip install .

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

CMD [ "python", "-m", "duple" ]
