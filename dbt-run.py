import psycopg2
import os
import time
import json
import subprocess

from urllib.parse import urlparse


for attempt in range(5):
    time.sleep(3)
    try:
        conn = psycopg2.connect(
            f"dbname={os.getenv('POSTGRES_DB')} "
            f"user={os.getenv('POSTGRES_USER')} "
            f"password={os.getenv('POSTGRES_PASSWORD')} "
            f"host=postgres port=5432"
        )
    except psycopg2.OperationalError as e:
        print('Unable to connect!\n{0}').format(e)
        conn = None
    else:
        break

if conn is None:
    exit(1)

cur = conn.cursor()

cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {os.getenv('POSTGRES_SCHEMA')}._dataemon (
        inserted_on TIMESTAMP DEFAULT NOW(),
        packages jsonb
    )
""")

init_package = urlparse(os.getenv("DATAEMON_INITAL_PACKAGE"))
if init_package.scheme in ["http", "https"]:
    cur.execute(
        f"INSERT INTO {os.getenv('POSTGRES_SCHEMA')}._dataemon "
        "(packages) VALUES (%s)",
        [json.dumps({
            "packages": [
                {
                    "git": init_package._replace(fragment='').geturl(),
                    "revision": init_package.fragment
                }
            ]
        })]
    )
    conn.commit()


while True:
    cur.execute(f"""
        SELECT packages
        FROM {os.getenv('POSTGRES_SCHEMA')}._dataemon
        ORDER BY inserted_on DESC
    """)

    with open("/dbt/packages.yml", "w") as f:
        f.write(json.dumps(cur.fetchone()[0]))

    subprocess.run(["dbt", "deps", "--profiles-dir", ".dbt"])
    subprocess.run(["dbt", "run",  "--profiles-dir", ".dbt"])
    time.sleep(5)
