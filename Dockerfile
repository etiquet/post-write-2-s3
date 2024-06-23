FROM python:3.8-slim

WORKDIR /app

COPY app.py /app

RUN pip install flask boto3

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

