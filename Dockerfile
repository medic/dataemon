FROM ubuntu

RUN apt-get update \
    && apt-get install -y git libpq-dev python-dev python3-pip postgresql-client \
    && apt-get remove -y python-cffi \
    && pip install --upgrade cffi \
    && pip install cryptography~=3.4 \
    && pip install dbt

WORKDIR /dbt/
COPY . .

CMD ["python3", "/dbt/dbt-run.py"]
