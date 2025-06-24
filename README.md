# Real-time Weather Data Pipeline

## 📌 Overview

This project implements a real-time data pipeline to collect, process, and store weather data. The system uses Apache Airflow to schedule periodic API calls, Kafka to transport messages, Spark Streaming to process data, and MySQL to store the final results.

## 🧱 Architecture

![System Architecture](assets/workflow.png)

## 📦 Technologies Used

- **Apache Airflow** – Orchestrates and schedules hourly DAGs to fetch weather data.
- **Apache Kafka** – Acts as a real-time message queue for streaming data.
- **Apache Spark Streaming** – Processes data from Kafka and transforms it before storage.
- **MySQL** – Stores the final structured weather data for analysis or querying.
- **World Weather Online API** – Provides real-time weather data via RESTful requests.
- **Python** – Main programming language for DAGs, Spark jobs, and data handling.
- **SQL** – Used to define database schema and perform queries on stored data.