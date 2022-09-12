FROM python:3.10.1
#LABEL maintainer="idel2309@gmail.com"

COPY .. ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
CMD ["python", "run.py"]
