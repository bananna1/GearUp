FROM python:latest

WORKDIR /adapter_layer/

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./app.py app.py
COPY ./consts.py consts.py
COPY ./__init__.py __init__.py
COPY ./views/ ./views/

ENV FLASK_APP=app:app
ENV PYTHONPATH=/adapter_layer

EXPOSE 5050

CMD ["flask", "run", "--host=0.0.0.0", "--port=5050"]
