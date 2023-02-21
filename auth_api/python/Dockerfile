FROM python:3-alpine

LABEL maintainer="oliveros.carlos.ro@gmail.com"

RUN mkdir /home/SRE-Bootcamp-Q12023

COPY . /home/SRE-Bootcamp-Q12023

WORKDIR /home/SRE-Bootcamp-Q12023

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "api.py"]