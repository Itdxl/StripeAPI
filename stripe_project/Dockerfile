FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app 
RUN pip3 install -r /app/requirements.txt --no-cache-dir


COPY . /app/

CMD ["gunicorn", "stripe_project.wsgi:application", "--bind", "0:8000"]
