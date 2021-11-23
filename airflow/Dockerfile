FROM apache/airflow:latest-python3.9

COPY requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

RUN mkdir -p /opt/airflow/db