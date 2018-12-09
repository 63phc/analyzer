FROM python:3.7-alpine
WORKDIR /app
RUN apk add --no-cache bash git
ADD requirements.txt /app
RUN pip install -r requirements.txt
ADD app.py /app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
