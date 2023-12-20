FROM python:3.11

RUN mkdir '/video-hosting_app'

WORKDIR /video-hosting_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


#WORKDIR src

#CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000