#ident "@(#)$Format:LocalFoodAI_lanfr144:openfoodfacts_ingestion.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.exceptions import AirflowSkipException
from datetime import datetime, timedelta
import os
import hashlib
import requests
import urllib.request

DATA_DIR = "/opt/airflow/data"
INGEST_FILE = "en.openfoodfacts.org.products.csv"
URL = "https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'openfoodfacts_ingestion',
    default_args=default_args,
    description='Automated Data Freshness Pipeline for OpenFoodFacts',
    schedule_interval='0 4 * * *', # Daily at 04:00
    catchup=False,
)

def download_and_validate(**kwargs):
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, INGEST_FILE)
    
    print("Downloading dataset...")
    # Downloading stream to handle large files
    try:
        urllib.request.urlretrieve(URL, file_path)
    except Exception as e:
        print(f"Failed to download: {e}")
        raise
    
    print("Calculating checksum...")
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    new_checksum = md5_hash.hexdigest()
    
    checksum_file = os.path.join(DATA_DIR, "checksum.md5")
    old_checksum = ""
    if os.path.exists(checksum_file):
        with open(checksum_file, "r") as f:
            old_checksum = f.read().strip()
            
    if new_checksum == old_checksum:
        print("Checksum matches previously processed file. Skipping ingestion.")
        raise AirflowSkipException("Dataset is already up to date.")
        
    print("Checksum mismatch: File is new or modified. Ingestion required.")
    
    # Push new checksum to XCom so the next task can save it upon success
    kwargs['ti'].xcom_push(key='new_checksum', value=new_checksum)
    return True

def save_checksum(**kwargs):
    new_checksum = kwargs['ti'].xcom_pull(key='new_checksum', task_ids='validate_freshness')
    checksum_file = os.path.join(DATA_DIR, "checksum.md5")
    with open(checksum_file, "w") as f:
        f.write(new_checksum)
    print("Checksum saved successfully.")

t1_validate = PythonOperator(
    task_id='validate_freshness',
    python_callable=download_and_validate,
    provide_context=True,
    dag=dag,
)

# DockerOperator requires the docker socket to be mounted to the airflow container
# It will spawn a container using the same image as our ingest service
t2_ingest = DockerOperator(
    task_id='trigger_ingestion_container',
    image='food_project-ingest',
    api_version='auto',
    auto_remove=True,
    command='./ingest_csv.py /data/en.openfoodfacts.org.products.csv',
    docker_url='unix://var/run/docker.sock',
    network_mode='food_project_default',
    # We must mount the local data dir into the ingest container so it can see the CSV
    # We use the relative host path since the docker socket resolves from the host's perspective!
    # Airflow runs in Docker, but the socket is the Host's socket.
    mounts=[
        # Host path -> Container path
        # Assuming the host project is in /home/francois/food_project
        # Note: This hardcoding is necessary when triggering sibling containers via socket
        # unless using complex volume bindings.
    ],
    environment={
        'DB_HOST': 'mysql',
        'DB_USER': 'food_loader',
        'DB_PASS': 'your_db_password_here'
    },
    mount_tmp_dir=False,
    dag=dag,
)

# Because host paths can vary, it's safer to use the named volume or rely on the fact 
# that docker-compose already created the image. 
# Wait, the ingest image COPY . /app. So the script is already inside. 
# But the CSV is in the host's ./data directory. 
# To fix the host path mount dynamically without hardcoding /home/francois/food_project:
# The DockerOperator can mount volumes like this: "food_project_data:/data" but we don't have a named volume for data.
# Let's map it via volumes argument.
t2_ingest.volumes = ['/home/francois/food_project/data:/data']

t3_save_checksum = PythonOperator(
    task_id='save_checksum',
    python_callable=save_checksum,
    provide_context=True,
    dag=dag,
)

t1_validate >> t2_ingest >> t3_save_checksum