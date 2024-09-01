FROM python:3.10-slim

WORKDIR /

COPY . /

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run", "--port=5002"]