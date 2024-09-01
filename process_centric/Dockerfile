FROM python:3.10

WORKDIR /process_centric/

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./app.py app.py
COPY ./consts.py consts.py
COPY ./client_secret.json client_secret.json
COPY ./CONFIG.json CONFIG.json
COPY ./__init__.py __init__.py
COPY ./views/ ./views/
COPY ./static/ ./static/
COPY ./templates/ ./templates

ENV FLASK_APP=app:app
ENV PYTHONPATH=/process_centric

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

