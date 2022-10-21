FROM python:3
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD gunicorn -b 0.0.0.0:8080 $PWD/itutor/app.py