# Real-time Weather Data Pipeline

## 📌 Overview

This project implements a real-time data pipeline to collect, process, and store weather data. The system uses Apache Airflow to schedule periodic API calls, Kafka to transport messages, Spark Streaming to process data, and MySQL to store the final results.

## 🧱 Architecture

![System Architecture](assets/workflow.png)

The system is designed as a real-time data pipeline with the following components:

- **WorldWeatherOnline API** is used as the external weather data source.
- **Apache Airflow** runs multiple DAGs every hour to fetch weather data and push messages to **Kafka**.
- **Apache Kafka** acts as the message broker, buffering weather data streams.
- **Apache Spark Streaming** reads from Kafka, processes and transforms the data in real time.
- **MySQL** stores the structured and cleaned data for further analysis or dashboarding.