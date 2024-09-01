FROM python:latest

WORKDIR /data_layer/

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./app.py app.py
COPY ./app/ ./app/
COPY ./config.py config.py
COPY ./__init__.py __init__.py
COPY ./migrations/ ./migrations/
COPY ./populate_gear_table/ ./populate_gear_table/

ENV FLASK_APP=app:app
ENV PYTHONPATH=/data_layer

EXPOSE 5051

CMD ["flask", "run", "--host=0.0.0.0", "--port=5051"]
