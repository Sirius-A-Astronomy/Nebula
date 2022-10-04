FROM python:3.9.10

#RUN mkdir ./app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY database-setup ./database-setup

RUN pip install -e .

RUN python database-setup/init_db.py
RUN python database-setup/database_test_data.py

ENV FLASK_APP=nebula
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000


CMD ["flask", "run"]