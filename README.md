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

## 🧾 API Input Structure

The weather data is fetched from the [World Weather Online API](https://www.worldweatheronline.com/).

Example JSON snippet:

```json
{
  "data": {
    "current_condition": [{
      "temp_C": "33",
      "windspeedKmph": "12",
      "pressure": "1010",
      "humidity": "62",
      "observation_time": "07:00 AM"
    }]
  }
}