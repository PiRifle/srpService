FROM python:3.9

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt

EXPOSE 6530

CMD [ "python", "app.py" ]