-- Adminer 4.8.1 MySQL 8.0.29 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `demo`;
CREATE DATABASE `demo` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `demo`;

DROP TABLE IF EXISTS `test`;
CREATE TABLE `test` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sometext` varchar(255) NOT NULL,
  `time` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `test` (`id`, `sometext`, `time`) VALUES
(1,	'A',	'2022-06-27 11:48:22'),
(2,	'b',	'2022-06-27 11:48:28'),
(3,	'c',	'2022-06-27 11:48:34');

-- 2022-06-27 11:48:43
