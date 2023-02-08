FROM python:3

RUN pip3 install flask

RUN mkdir /datalet

COPY mlparams /datalet/mlparams

COPY app.py /datalet/app.py

WORKDIR /datalet

CMD ["python", "app.py"]