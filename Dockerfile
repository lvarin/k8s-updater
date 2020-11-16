FROM python:3.6-slim-stretch

WORKDIR /app
COPY ./ /app/
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "api.py"]
