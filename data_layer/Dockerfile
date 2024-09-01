FROM python:latest

ADD ./requirements.txt /app/requirements.txt

WORKDIR /app/

RUN pip install -r requirements.txt

EXPOSE 5051

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run", "--host=0.0.0.0", "--port=5051"]
