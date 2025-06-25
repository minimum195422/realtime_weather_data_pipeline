from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("WeatherStreamingToMySQL") \
    .getOrCreate()

# Schema JSON
weather_schema = StructType([
    StructField("observation_time", StringType()),
    StructField("temp_C", StringType()),
    StructField("temp_F", StringType()),
    StructField("weatherCode", StringType()),
    StructField("weatherIconUrl", ArrayType(
        StructType([StructField("value", StringType())])
    )),
    StructField("weatherDesc", ArrayType(
        StructType([StructField("value", StringType())])
    )),
    StructField("windspeedMiles", StringType()),
    StructField("windspeedKmph", StringType()),
    StructField("winddirDegree", StringType()),
    StructField("winddir16Point", StringType()),
    StructField("precipMM", StringType()),
    StructField("precipInches", StringType()),
    StructField("humidity", StringType()),
    StructField("visibility", StringType()),
    StructField("visibilityMiles", StringType()),
    StructField("pressure", StringType()),
    StructField("pressureInches", StringType()),
    StructField("cloudcover", StringType()),
    StructField("FeelsLikeC", StringType()),
    StructField("FeelsLikeF", StringType()),
    StructField("uvIndex", StringType()),
    StructField("station_id", IntegerType()),
    StructField("record_time", StringType()),  # Đã đúng format '%Y-%m-%d %H:%M:%S'
])

# Đọc stream Kafka
kafka_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "weather_topic") \
    .option("startingOffsets", "latest") \
    .load()

json_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str")

parsed_df = json_df.select(from_json(col("json_str"), weather_schema).alias("data")).select("data.*")

# Chuyển trực tiếp cột record_time sang timestamp (format '%Y-%m-%d %H:%M:%S')
final_df = parsed_df.select(
    col("station_id"),
    to_timestamp(col("record_time"), "yyyy-MM-dd HH:mm:ss").alias("record_time"),
    col("temp_C").cast("smallint").alias("temp_c"),
    col("temp_F").cast("smallint").alias("temp_f"),
    col("windspeedKmph").cast("float").alias("windspeed_kmph"),
    col("windspeedMiles").cast("float").alias("windspeed_mile"),
    col("winddirDegree").cast("smallint").alias("winddir_degree"),
    col("winddir16Point").alias("winddir16point"),
    col("precipMM").cast("float").alias("precipMM"),
    col("pressure").cast("float").alias("pressure"),
    col("visibility").cast("float").alias("visibility"),
    col("cloudcover").cast("int").alias("cloud_cover"),
    col("uvIndex").cast("int").alias("uv_index"),
    col("weatherIconUrl")[0]["value"].alias("icon_url"),
).filter(col("record_time").isNotNull())

def write_to_mysql(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .mode("append") \
        .option("url", "jdbc:mysql://192.168.1.158:3306/weather_schema") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "weather_data") \
        .option("user", "HanoiStation") \
        .option("password", "weatherstation") \
        .save()

query = final_df.writeStream \
    .foreachBatch(write_to_mysql) \
    .outputMode("append") \
    .start()

query.awaitTermination()
