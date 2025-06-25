import json
import requests
import boto3
from kafka import KafkaProducer
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# === Cấu hình API & S3 ===
WEATHER_API_KEY = '86df7535febc4e649c3233030251006'
CITY = "Hanoi"
COUNTRY = 'Vietnam'
STATION_ID = 1
QUERY = f"{CITY},{COUNTRY}"
FORMAT = "json"
URL = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
S3_BUCKET = "global-weather-data-v1"
KAFKA_TOPIC = "weather_topic"
KAFKA_BROKER = "localhost:9092"

PARAMS = {
    "key": WEATHER_API_KEY,
    "q": QUERY,
    "format": FORMAT,
    "num_of_days": 1,
    "tp": 3,
    "date": "today"
}

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    dag_id='hanoi_vietnam_station_dag_1',
    default_args=default_args,
    description='Gọi API thời tiết, đẩy lên S3 và Kafka',
    schedule_interval="*/60 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['weather station', 'hanoi', 'vietnam']
)

# === Task 1: Lấy dữ liệu từ API ===
def fetch_weather_data(**kwargs):
    response = requests.get(URL, params=PARAMS)
    data = response.json()
    current_condition = data['data']['current_condition'][0]
    
    record_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    current_condition['station_id'] = STATION_ID
    current_condition['record_time'] = record_time

    kwargs['ti'].xcom_push(key='current_condition', value=current_condition)


# === Task 2: Upload dữ liệu lên S3 ===
def upload_to_s3(**kwargs):
    current_condition = kwargs['ti'].xcom_pull(key='current_condition', task_ids='fetch_weather_data')
    record_time = current_condition['record_time']
    
    session = boto3.Session(profile_name='weather-iam')
    s3 = session.client('s3')

    filename = f"weather_raw/weather_{CITY}_{COUNTRY}_{record_time}.json"
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=filename,
        Body=json.dumps(current_condition),
        ContentType='application/json'
    )

    print(f"Đã lưu dữ liệu lên S3 với key: {filename}")
    kwargs['ti'].xcom_push(key='s3_key', value=filename)


# === Task 3: Gửi dữ liệu vào Kafka ===
def send_to_kafka(**kwargs):
    current_condition = kwargs['ti'].xcom_pull(key='current_condition', task_ids='fetch_weather_data')

    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    producer.send(KAFKA_TOPIC, current_condition)
    producer.flush()
    print("Đã gửi dữ liệu vào Kafka topic:", KAFKA_TOPIC)

# === Định nghĩa các task ===
task_fetch = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=fetch_weather_data,
    provide_context=True,
    dag=dag
)

task_s3 = PythonOperator(
    task_id='upload_to_s3',
    python_callable=upload_to_s3,
    provide_context=True,
    dag=dag
)

task_kafka = PythonOperator(
    task_id='send_to_kafka',
    python_callable=send_to_kafka,
    provide_context=True,
    dag=dag
)

# === Thiết lập thứ tự chạy ===
task_fetch >> [task_s3, task_kafka]
