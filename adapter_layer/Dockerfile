FROM python:latest

ADD ./requirements.txt /app/requirements.txt

WORKDIR /app/

RUN pip install -r requirements.txt

COPY . /app/

ENV FLASK_APP=app:app
ENV PYTHONPATH=/app

EXPOSE 5050

CMD ["flask", "run", "--host=0.0.0.0", "--port=5050"]
