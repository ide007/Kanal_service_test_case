FROM python:3.10.7
#LABEL maintainer="idel2309@gmail.com"

RUN apt-get update && apt-get install -y postgresql

WORKDIR ./app

COPY ./ ./


RUN pip install --upgrade pip

RUN pip install -r requirements.txt
COPY wait-for-postgres.sh .
RUN chmod +x wait-for-postgres.sh
CMD ["python", "run.py"]