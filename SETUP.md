# 🛠️ System Setup

## 📦 1. Installing Airflow on Ubuntu (Python 3.10)

This section guides you through installing Apache Airflow on Ubuntu using Python 3.10 and a virtual environment (`venv`).

### ✅ Install Python 3.10 and essential tools

```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-dev
```

### ✅ Create and activate a virtual environment

```bash
python3.10 -m venv airflow_env
source airflow_env/bin/activate
```

### ✅ Install Apache Airflow

```bash
export AIRFLOW_VERSION=2.9.1
export PYTHON_VERSION="3.10"
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install --upgrade pip setuptools wheel
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

### ✅ Initialize the Airflow Project Folder and Database

```bash
mkdir -p ~/airflow
cd ~/airflow
airflow db init
```

### ✅ Create an Admin User

```bash
airflow users create \
  --username admin \
  --firstname Duong \
  --lastname Minh \
  --role Admin \
  --email admin@example.com \
  --password admin
```

### ✅ Start Airflow Services

Start the webserver:

```bash
airflow webserver --port 8080
```

In a separate terminal, start the scheduler:

```bash
airflow scheduler
```

### 📌 Notes

- Airflow scans the `~/airflow/dags/` directory for DAG definition files. You should place your custom DAG Python scripts inside this folder so that they are automatically detected and scheduled. For example, you can copy a DAG file from your GitHub repository by downloading or cloning it, then placing the DAG code into the `dags` directory.
  
  ➡️ [View full DAG code](./airflow/hanoi_weather_station_n1_dag.py)

- By default, Airflow uses SQLite as the metadata database, which is not suitable for production. For production use, update the `sql_alchemy_conn` parameter in `airflow.cfg` to use MySQL or PostgreSQL.

## 🧪 2. Kafka Setup

### ✅ Install Java 17

```bash
sudo apt update
sudo apt install -y openjdk-17-jdk
java -version
```

### ✅ Download and Extract Kafka

```bash
wget https://downloads.apache.org/kafka/4.0.0/kafka_2.13-4.0.0.tgz
tar -xvzf kafka_2.13-4.0.0.tgz
mv kafka_2.13-4.0.0 kafka
cd kafka
mkdir tmp
```

### ✅ Edit Configuration File

Open the Kafka server configuration:

```bash
nano config/server.properties
```

Find the line:

```bash
log.dirs=...
```

Replace it with:

```bash
log.dirs=/home/minimum/kafka/tmp/kraft-combined-logs
```

### ✅ Generate UUID for Kafka KRaft Mode

```bash
bin/kafka-storage.sh random-uuid
```

Once the UUID is generated (e.g. `e29c4fae-xxxx-xxxx-xxxx-xxxxxxxxxxxx`), run the following command to format the storage in standalone mode:

```bash
bin/kafka-storage.sh format -t [uuid] -c config/server.properties --standalone
```

🔁 If you see an error due to an existing UUID or prior data, remove the old cache with:

```bash
rm -rf /tmp/kraft-combined-logs
```

Then re-run the format command above.

### ✅ Start Kafka Server

```bash
bin/kafka-server-start.sh config/server.properties
```

### ✅ Create a Kafka Topic

```bash
bin/kafka-topics.sh --create --topic [your-topic-name] --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### ✅ Start Kafka Producer (Terminal 1)

```bash
bin/kafka-console-producer.sh --topic [your-topic-name] --bootstrap-server localhost:9092
```

### ✅ Start Kafka Consumer (Terminal 2)

```bash
bin/kafka-console-consumer.sh --topic [your-topic-name] --bootstrap-server localhost:9092 --from-beginning
```

### ✅ List All Topics

```bash
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

## ⚡ 3. Spark setup

### ✅ Download and Extract Spark

```bash
wget https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
tar -xvzf spark-3.5.1-bin-hadoop3.tgz
mv spark-3.5.1-bin-hadoop3 spark
cd spark
```

### ✅ Configure Environment Variables

Open the `.bashrc` file:

```bash
nano ~/.bashrc
```

Scroll to the bottom and add the following lines:

```bash
export SPARK_HOME=~/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
```

Save and close the file, then reload your shell configuration:

```bash
source ~/.bashrc
```

Apache Spark is now ready to use. You can verify the installation with:

```bash
spark-shell
```

### ✅ Streaming Data with Apache Spark

Create a folder for your streaming project, for example:

```bash
mkdir ~/weather_project
cd ~/weather_project
```

Place your Spark streaming script in this directory. For example, ➡️ [View full Spark streaming code](./spark/spark_streaming.py)

### ✅ Add MySQL Connector

Download the MySQL JDBC connector (`mysql-connector-jdbc.jar`) and place it in the project directory (e.g., `/home/minimum/weather_project/mysql-connector-jdbc.jar`).  
You can download it from the official MySQL site or use the following link (adjust version as needed):

```bash
wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.33/mysql-connector-java-8.0.33.jar -O mysql-connector-jdbc.jar
```

### ✅ Run Spark Streaming Job

Use the following `spark-submit` command to run your Spark streaming application with Kafka and MySQL support:

```bash
spark-submit --master local[*] \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
  --jars /home/minimum/weather_project/mysql-connector-jdbc.jar \
  spark_streaming.py
```

This command:

- Uses all available local cores (`local[*]`)

- Loads the Kafka Spark SQL integration package

- Loads the MySQL connector for JDBC output

- Executes your `spark_streaming.py` script

## ☁️ Installing AWS CLI and Required Python Libraries

## ✅ Install AWS CLI (v2)

Download and install the AWS Command Line Interface:

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

### ✅ Set Up an AWS Profile

To create a new named profile for AWS credentials:

```bash
aws configure --profile [your-profile-name]
```

Replace `[your-profile-name]` with your custom profile name (e.g., `weather-stream`), then provide your Access Key ID, Secret Access Key, region, and output format when prompted.

### ✅ View Configured Profiles

List all configured profiles:

```bash
aws configure list-profiles
```

To view details of a specific profile:

```bash
aws configure list --profile [your-profile-name]
```

### ✅ Install Required Python Libraries

Make sure the following Python libraries are installed for your streaming and cloud integration:

```bash
pip install kafka-python boto3
```

- `kafka-python`: Used to interact with Kafka producers and consumers in Python.

- `boto3`: AWS SDK for Python, required for working with AWS services such as S3, SQS, or DynamoDB.
