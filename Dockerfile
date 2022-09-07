FROM python:3.10.6-slim-bullseye

COPY . .


RUN pip3 install -r requirements.txt


CMD [ "python3", "-m" , "waitress", "--listen=0.0.0.0:5000", "main:app"]