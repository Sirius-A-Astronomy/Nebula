FROM python:3.9.10

#RUN mkdir ./app
WORKDIR ./app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python database-setup/init_db.py
RUN python database-setup/test_database.py

ENV FLASK_APP=nebula
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000


CMD ["flask", "run"]