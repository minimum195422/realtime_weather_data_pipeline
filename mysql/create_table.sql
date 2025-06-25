CREATE TABLE `continents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `continent` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `countries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `continent_id` int NOT NULL,
  `country_name` varchar(255) NOT NULL,
  `iso_code` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `continent_id` (`continent_id`),
  CONSTRAINT `countries_ibfk_1` FOREIGN KEY (`continent_id`) REFERENCES `continents` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `cities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `country_id` int NOT NULL,
  `city_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `country_id` (`country_id`),
  CONSTRAINT `cities_ibfk_1` FOREIGN KEY (`country_id`) REFERENCES `countries` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `weather_stations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `station_name` varchar(255) NOT NULL,
  `city_id` int NOT NULL,
  `station_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `city_id` (`city_id`),
  CONSTRAINT `weather_stations_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `station_operation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `station_id` int NOT NULL,
  `operation_type` varchar(50) NOT NULL,
  `operation_date` date NOT NULL,
  `provider_name` varchar(255) DEFAULT NULL,
  `note` text,
  PRIMARY KEY (`id`),
  KEY `station_id` (`station_id`),
  CONSTRAINT `station_operation_ibfk_1` FOREIGN KEY (`station_id`) REFERENCES `weather_stations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `weather_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `station_id` int NOT NULL,
  `record_time` datetime NOT NULL,
  `temp_c` smallint DEFAULT NULL,
  `temp_f` smallint DEFAULT NULL,
  `windspeed_kmph` float DEFAULT NULL,
  `windspeed_mile` float DEFAULT NULL,
  `winddir_degree` smallint DEFAULT NULL,
  `winddir16point` varchar(5) DEFAULT NULL,
  `precipMM` float DEFAULT NULL,
  `pressure` float DEFAULT NULL,
  `visibility` float DEFAULT NULL,
  `cloud_cover` int DEFAULT NULL,
  `uv_index` int DEFAULT NULL,
  `icon_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `station_id` (`station_id`),
  CONSTRAINT `weather_data_ibfk_1` FOREIGN KEY (`station_id`) REFERENCES `weather_stations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;