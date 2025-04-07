-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: ztudy
-- ------------------------------------------------------
-- Server version	9.0.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailaddress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_emailaddress_user_id_email_987c8728_uniq` (`user_id`,`email`),
  KEY `account_emailaddress_email_03be32b2` (`email`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
INSERT INTO `account_emailaddress` VALUES (1,'user1@gmail.com',0,1,2);
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `email_address_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailconfirmation`
--

LOCK TABLES `account_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `account_emailconfirmation` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add site',6,'add_site'),(22,'Can change site',6,'change_site'),(23,'Can delete site',6,'delete_site'),(24,'Can view site',6,'view_site'),(25,'Can add background video type',7,'add_backgroundvideotype'),(26,'Can change background video type',7,'change_backgroundvideotype'),(27,'Can delete background video type',7,'delete_backgroundvideotype'),(28,'Can view background video type',7,'view_backgroundvideotype'),(29,'Can add motivational quote',8,'add_motivationalquote'),(30,'Can change motivational quote',8,'change_motivationalquote'),(31,'Can delete motivational quote',8,'delete_motivationalquote'),(32,'Can view motivational quote',8,'view_motivationalquote'),(33,'Can add room category',9,'add_roomcategory'),(34,'Can change room category',9,'change_roomcategory'),(35,'Can delete room category',9,'delete_roomcategory'),(36,'Can view room category',9,'view_roomcategory'),(37,'Can add sound',10,'add_sound'),(38,'Can change sound',10,'change_sound'),(39,'Can delete sound',10,'delete_sound'),(40,'Can view sound',10,'view_sound'),(41,'Can add user',11,'add_user'),(42,'Can change user',11,'change_user'),(43,'Can delete user',11,'delete_user'),(44,'Can view user',11,'view_user'),(45,'Can add background video',12,'add_backgroundvideo'),(46,'Can change background video',12,'change_backgroundvideo'),(47,'Can delete background video',12,'delete_backgroundvideo'),(48,'Can view background video',12,'view_backgroundvideo'),(49,'Can add room',13,'add_room'),(50,'Can change room',13,'change_room'),(51,'Can delete room',13,'delete_room'),(52,'Can view room',13,'view_room'),(53,'Can add room participant',14,'add_roomparticipant'),(54,'Can change room participant',14,'change_roomparticipant'),(55,'Can delete room participant',14,'delete_roomparticipant'),(56,'Can view room participant',14,'view_roomparticipant'),(57,'Can add session goal',15,'add_sessiongoal'),(58,'Can change session goal',15,'change_sessiongoal'),(59,'Can delete session goal',15,'delete_sessiongoal'),(60,'Can view session goal',15,'view_sessiongoal'),(61,'Can add study session',16,'add_studysession'),(62,'Can change study session',16,'change_studysession'),(63,'Can delete study session',16,'delete_studysession'),(64,'Can view study session',16,'view_studysession'),(65,'Can add user activity log',17,'add_useractivitylog'),(66,'Can change user activity log',17,'change_useractivitylog'),(67,'Can delete user activity log',17,'delete_useractivitylog'),(68,'Can view user activity log',17,'view_useractivitylog'),(69,'Can add interest',18,'add_interest'),(70,'Can change interest',18,'change_interest'),(71,'Can delete interest',18,'delete_interest'),(72,'Can view interest',18,'view_interest'),(73,'Can add Token',19,'add_token'),(74,'Can change Token',19,'change_token'),(75,'Can delete Token',19,'delete_token'),(76,'Can view Token',19,'view_token'),(77,'Can add Token',20,'add_tokenproxy'),(78,'Can change Token',20,'change_tokenproxy'),(79,'Can delete Token',20,'delete_tokenproxy'),(80,'Can view Token',20,'view_tokenproxy'),(81,'Can add email address',21,'add_emailaddress'),(82,'Can change email address',21,'change_emailaddress'),(83,'Can delete email address',21,'delete_emailaddress'),(84,'Can view email address',21,'view_emailaddress'),(85,'Can add email confirmation',22,'add_emailconfirmation'),(86,'Can change email confirmation',22,'change_emailconfirmation'),(87,'Can delete email confirmation',22,'delete_emailconfirmation'),(88,'Can view email confirmation',22,'view_emailconfirmation'),(89,'Can add social account',23,'add_socialaccount'),(90,'Can change social account',23,'change_socialaccount'),(91,'Can delete social account',23,'delete_socialaccount'),(92,'Can view social account',23,'view_socialaccount'),(93,'Can add social application',24,'add_socialapp'),(94,'Can change social application',24,'change_socialapp'),(95,'Can delete social application',24,'delete_socialapp'),(96,'Can view social application',24,'view_socialapp'),(97,'Can add social application token',25,'add_socialtoken'),(98,'Can change social application token',25,'change_socialtoken'),(99,'Can delete social application token',25,'delete_socialtoken'),(100,'Can view social application token',25,'view_socialtoken');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_backgroundvideo`
--

DROP TABLE IF EXISTS `core_backgroundvideo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_backgroundvideo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `type_id` bigint NOT NULL,
  `youtube_url` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_backgroundvideo_type_id_d9516c7a_fk_core_back` (`type_id`),
  CONSTRAINT `core_backgroundvideo_type_id_d9516c7a_fk_core_back` FOREIGN KEY (`type_id`) REFERENCES `core_backgroundvideotype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_backgroundvideo`
--

LOCK TABLES `core_backgroundvideo` WRITE;
/*!40000 ALTER TABLE `core_backgroundvideo` DISABLE KEYS */;
INSERT INTO `core_backgroundvideo` VALUES (1,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741772666/ztudy/background-video-images/background-video_1_image.png','2025-03-12 16:52:58.872080','2025-03-12 16:56:19.074173',1,'https://www.youtube.com/watch?v=5wRWniH7rt8'),(2,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741773622/ztudy/background-video-images/background-video_2_image.png','2025-03-12 16:59:58.929288','2025-03-12 17:00:23.531084',1,'https://www.youtube.com/watch?v=1oahTaVIQvk'),(3,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741773932/ztudy/background-video-images/background-video_3_image.png','2025-03-12 17:04:59.574156','2025-03-12 17:05:32.952597',1,'https://www.youtube.com/watch?v=UWBfTjgqnGw'),(4,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741773990/ztudy/background-video-images/background-video_4_image.png','2025-03-12 17:06:15.043530','2025-03-12 17:06:31.136505',1,'https://www.youtube.com/watch?v=c3Jl8ZIPcmw'),(5,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741774504/ztudy/background-video-images/background-video_5_image.png','2025-03-12 17:14:54.025590','2025-03-12 17:15:05.542706',1,'https://www.youtube.com/watch?v=-SsD_XXPAj4'),(6,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741774587/ztudy/background-video-images/background-video_6_image.png','2025-03-12 17:16:15.852361','2025-03-12 17:16:28.409542',1,'https://www.youtube.com/watch?v=tNyz-uVfSN0'),(7,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741774630/ztudy/background-video-images/background-video_7_image.png','2025-03-12 17:16:56.572837','2025-03-12 17:17:11.506504',1,'https://www.youtube.com/watch?v=uDNr-y7xdiQ'),(8,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741774687/ztudy/background-video-images/background-video_8_image.png','2025-03-12 17:17:55.472139','2025-03-12 17:18:07.986808',1,'https://www.youtube.com/watch?v=S_uD_BqC2gg'),(9,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741774731/ztudy/background-video-images/background-video_9_image.png','2025-03-12 17:18:32.676078','2025-03-12 17:18:52.249973',1,'https://www.youtube.com/watch?v=gvNmkJnCjdU'),(10,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741775320/ztudy/background-video-images/background-video_10_image.png','2025-03-12 17:20:18.245787','2025-03-12 17:28:41.122429',2,'https://www.youtube.com/watch?v=cLOP0Kr36ZA'),(11,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779694/ztudy/background-video-images/background-video_11_image.png','2025-03-12 18:41:21.107400','2025-03-12 18:41:35.367241',2,'https://www.youtube.com/watch?v=CHFif_y2TyM'),(12,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741775680/ztudy/background-video-images/background-video_12_image.png','2025-03-12 17:29:29.674730','2025-03-12 17:34:40.920558',2,'https://www.youtube.com/watch?v=Ab0DhO2gYf0'),(13,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741775842/ztudy/background-video-images/background-video_13_image.png','2025-03-12 17:37:04.167416','2025-03-12 17:37:22.799495',2,'https://www.youtube.com/watch?v=mlbZE-0A2EM'),(14,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741775905/ztudy/background-video-images/background-video_14_image.png','2025-03-12 17:38:13.203651','2025-03-12 17:38:25.830645',2,'https://www.youtube.com/watch?v=5TtBW2FnFdk'),(15,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741775949/ztudy/background-video-images/background-video_15_image.png','2025-03-12 17:38:59.072721','2025-03-12 17:39:10.246215',2,'https://www.youtube.com/watch?v=rGfWVK5hSnw'),(16,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741776008/ztudy/background-video-images/background-video_16_image.png','2025-03-12 17:39:56.682761','2025-03-12 17:40:09.356438',2,'https://www.youtube.com/watch?v=rVA6y7NzBaQ'),(17,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741776092/ztudy/background-video-images/background-video_17_image.png','2025-03-12 17:41:23.583003','2025-03-12 17:41:33.355744',2,'https://www.youtube.com/watch?v=UFn5KHye6_g'),(18,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741776126/ztudy/background-video-images/background-video_18_image.png','2025-03-12 17:41:56.002639','2025-03-12 17:42:07.262450',2,'https://www.youtube.com/watch?v=DZtxEdFJJiU'),(19,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741776429/ztudy/background-video-images/background-video_19_image.png','2025-03-12 17:46:56.012806','2025-03-12 17:47:11.447508',3,'https://www.youtube.com/watch?v=XxEhuSJF780'),(20,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741776474/ztudy/background-video-images/background-video_20_image.png','2025-03-12 17:47:40.098711','2025-03-12 17:47:55.644482',3,'https://www.youtube.com/watch?v=xNN7iTA57jM'),(21,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741776521/ztudy/background-video-images/background-video_21_image.png','2025-03-12 17:48:26.581696','2025-03-12 17:48:41.853964',3,'https://www.youtube.com/watch?v=ujudMBJ6XhA'),(22,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741776555/ztudy/background-video-images/background-video_22_image.png','2025-03-12 17:49:04.471109','2025-03-12 17:49:16.655175',3,'https://www.youtube.com/watch?v=wRmGG2iz7KA'),(23,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741776589/ztudy/background-video-images/background-video_23_image.png','2025-03-12 17:49:33.584536','2025-03-12 17:49:50.570852',3,'https://www.youtube.com/watch?v=VOsejnWnhSg'),(24,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741776626/ztudy/background-video-images/background-video_24_image.png','2025-03-12 17:50:14.718151','2025-03-12 17:50:27.482966',3,'https://www.youtube.com/watch?v=acsLxmnjMho'),(25,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741776653/ztudy/background-video-images/background-video_25_image.png','2025-03-12 17:50:45.058015','2025-03-12 17:50:54.280831',3,'https://www.youtube.com/watch?v=GJ7jIOzLZwM'),(26,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741776692/ztudy/background-video-images/background-video_26_image.png','2025-03-12 17:51:17.941756','2025-03-12 17:51:32.921157',3,'https://www.youtube.com/watch?v=8FMBtusLdPU'),(27,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741776716/ztudy/background-video-images/background-video_27_image.png','2025-03-12 17:51:47.633631','2025-03-12 17:51:57.833333',3,'https://www.youtube.com/watch?v=ZaQgAqsEQkw'),(28,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741777166/ztudy/background-video-images/background-video_28_image.png','2025-03-12 17:59:09.672322','2025-03-12 17:59:26.725758',4,'https://www.youtube.com/watch?v=Z_JU4NE90gI'),(29,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741777255/ztudy/background-video-images/background-video_29_image.png','2025-03-12 18:00:42.370951','2025-03-12 18:00:55.852548',4,'https://www.youtube.com/watch?v=GrG2-oX5z24'),(30,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741777301/ztudy/background-video-images/background-video_30_image.png','2025-03-12 18:01:20.012727','2025-03-12 18:01:42.164198',4,'https://www.youtube.com/watch?v=3hJrQgh5Ad4'),(31,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741777461/ztudy/background-video-images/background-video_31_image.png','2025-03-12 18:04:09.857751','2025-03-12 18:04:22.433928',4,'https://www.youtube.com/watch?v=yfhiEH2EkBI'),(32,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741777497/ztudy/background-video-images/background-video_32_image.png','2025-03-12 18:04:41.622709','2025-03-12 18:04:57.899220',4,'https://www.youtube.com/watch?v=4NrpprUAa2U'),(33,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741777533/ztudy/background-video-images/background-video_33_image.png','2025-03-12 18:05:20.038799','2025-03-12 18:05:34.621251',4,'https://www.youtube.com/watch?v=PX7Oy4ttC48'),(34,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741777574/ztudy/background-video-images/background-video_34_image.png','2025-03-12 18:05:52.828369','2025-03-12 18:06:15.584780',4,'https://www.youtube.com/watch?v=_jqWwQNWsg4'),(35,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741777606/ztudy/background-video-images/background-video_35_image.png','2025-03-12 18:06:35.712828','2025-03-12 18:06:47.591367',4,'https://www.youtube.com/watch?v=cExYJVF3f6I'),(36,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741777643/ztudy/background-video-images/background-video_36_image.png','2025-03-12 18:07:11.103824','2025-03-12 18:07:23.679924',4,'https://www.youtube.com/watch?v=zJ7hUvU-d2Q'),(37,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741777940/ztudy/background-video-images/background-video_37_image.png','2025-03-12 18:12:06.011194','2025-03-12 18:12:21.390008',5,'https://www.youtube.com/watch?v=6WXMivVkiR8'),(38,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741777993/ztudy/background-video-images/background-video_38_image.png','2025-03-12 18:13:02.451316','2025-03-12 18:13:13.992645',5,'https://www.youtube.com/watch?v=c0_ejQQcrwI'),(39,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778037/ztudy/background-video-images/background-video_39_image.png','2025-03-12 18:13:41.301922','2025-03-12 18:13:58.002778',5,'https://www.youtube.com/watch?v=4IZq3GsNfLg'),(40,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778071/ztudy/background-video-images/background-video_40_image.png','2025-03-12 18:14:17.814007','2025-03-12 18:14:32.345233',5,'https://www.youtube.com/watch?v=uU_RxnJOdMQ'),(41,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778110/ztudy/background-video-images/background-video_41_image.png','2025-03-12 18:14:58.996621','2025-03-12 18:15:10.939457',5,'https://www.youtube.com/watch?v=VMAPTo7RVCo'),(42,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778142/ztudy/background-video-images/background-video_42_image.png','2025-03-12 18:15:30.289398','2025-03-12 18:15:43.313726',5,'https://www.youtube.com/watch?v=roABNwbjZf4'),(43,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778177/ztudy/background-video-images/background-video_43_image.png','2025-03-12 18:16:11.942011','2025-03-12 18:19:47.513267',5,'https://www.youtube.com/watch?v=0QKdqm5TX6c'),(44,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778211/ztudy/background-video-images/background-video_44_image.png','2025-03-12 18:16:40.476711','2025-03-12 18:19:33.418951',5,'https://www.youtube.com/watch?v=oW0ox0-8lRE'),(45,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778278/ztudy/background-video-images/background-video_45_image.png','2025-03-12 18:17:15.572004','2025-03-12 18:17:58.923536',5,'https://www.youtube.com/watch?v=Tzh5zDvJJ2c'),(46,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778703/ztudy/background-video-images/background-video_46_image.png','2025-03-12 18:21:46.992099','2025-03-12 18:25:03.825684',6,'https://www.youtube.com/watch?v=0-fJS-j_UEE'),(47,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778713/ztudy/background-video-images/background-video_47_image.png','2025-03-12 18:22:38.158443','2025-03-12 18:25:13.937449',6,'https://www.youtube.com/watch?v=gvqhjyjiguM'),(48,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778722/ztudy/background-video-images/background-video_48_image.png','2025-03-12 18:22:58.816989','2025-03-12 18:25:22.968756',6,'https://www.youtube.com/watch?v=y27-OpyQJeE'),(49,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778733/ztudy/background-video-images/background-video_49_image.png','2025-03-12 18:23:15.923044','2025-03-12 18:25:33.980224',6,'https://www.youtube.com/watch?v=CfPxlb8-ZQ0'),(50,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778741/ztudy/background-video-images/background-video_50_image.png','2025-03-12 18:23:32.111584','2025-03-12 18:25:42.369911',6,'https://www.youtube.com/watch?v=NMs01BXPP2M'),(51,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778750/ztudy/background-video-images/background-video_51_image.png','2025-03-12 18:23:45.881691','2025-03-12 18:25:51.210157',6,'https://www.youtube.com/watch?v=MWkIxYtB8Ag'),(52,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778758/ztudy/background-video-images/background-video_52_image.png','2025-03-12 18:24:04.686933','2025-03-12 18:25:59.355616',6,'https://www.youtube.com/watch?v=X2-EVyGFWqA'),(53,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778767/ztudy/background-video-images/background-video_53_image.png','2025-03-12 18:24:26.344346','2025-03-12 18:26:08.122482',6,'https://www.youtube.com/watch?v=iMj3NNCNmBE'),(54,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741778776/ztudy/background-video-images/background-video_54_image.png','2025-03-12 18:24:38.678888','2025-03-12 18:26:17.736027',6,'https://www.youtube.com/watch?v=e9dCKJjh278'),(55,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779351/ztudy/background-video-images/background-video_55_image.png','2025-03-12 18:30:05.356892','2025-03-12 18:35:52.030688',7,'https://www.youtube.com/watch?v=iIuuMNbSjDE'),(56,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779363/ztudy/background-video-images/background-video_56_image.png','2025-03-12 18:30:23.919745','2025-03-12 18:36:03.765894',7,'https://www.youtube.com/watch?v=y-JtsmxGZnU'),(57,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779377/ztudy/background-video-images/background-video_57_image.png','2025-03-12 18:30:45.478022','2025-03-12 18:36:18.205028',7,'https://www.youtube.com/watch?v=QUqhgZjrrsE'),(58,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779387/ztudy/background-video-images/background-video_58_image.png','2025-03-12 18:31:40.853814','2025-03-12 18:36:27.885746',7,'https://www.youtube.com/watch?v=yttvb9ByOtY'),(59,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779404/ztudy/background-video-images/background-video_59_image.png','2025-03-12 18:31:57.681078','2025-03-12 18:36:45.044012',7,'https://www.youtube.com/watch?v=CiGHT4eS-oU'),(60,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779414/ztudy/background-video-images/background-video_60_image.png','2025-03-12 18:32:16.086212','2025-03-12 18:36:55.246006',7,'https://www.youtube.com/watch?v=B6eL_N0N5KI'),(61,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779423/ztudy/background-video-images/background-video_61_image.png','2025-03-12 18:32:37.292812','2025-03-12 18:37:04.316986',7,'https://www.youtube.com/watch?v=RKKlFWU-N5s'),(62,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779432/ztudy/background-video-images/background-video_62_image.png','2025-03-12 18:32:50.879810','2025-03-12 18:37:13.695746',7,'https://www.youtube.com/watch?v=W5KJsQMKbwM'),(63,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779444/ztudy/background-video-images/background-video_63_image.png','2025-03-12 18:33:03.086587','2025-03-12 18:37:24.960964',7,'https://www.youtube.com/watch?v=e97Xe7544Yg'),(64,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779462/ztudy/background-video-images/background-video_64_image.png','2025-03-12 18:33:53.482743','2025-03-12 18:37:43.682687',9,'https://www.youtube.com/watch?v=y7-Svpotd3s'),(65,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779470/ztudy/background-video-images/background-video_65_image.png','2025-03-12 18:34:09.983228','2025-03-12 18:37:50.938605',9,'https://www.youtube.com/watch?v=atjAURP2_9o'),(66,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779477/ztudy/background-video-images/background-video_66_image.png','2025-03-12 18:34:21.110329','2025-03-12 18:37:58.497794',9,'https://www.youtube.com/watch?v=wjQq0nSGS28'),(67,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779486/ztudy/background-video-images/background-video_67_image.png','2025-03-12 18:34:33.949818','2025-03-12 18:38:07.206567',9,'https://www.youtube.com/watch?v=zxbO_dZeTrg'),(68,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779493/ztudy/background-video-images/background-video_68_image.png','2025-03-12 18:34:45.400319','2025-03-12 18:38:14.006079',9,'https://www.youtube.com/watch?v=F9UP2CHFS7A'),(69,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779501/ztudy/background-video-images/background-video_69_image.png','2025-03-12 18:34:57.430848','2025-03-12 18:38:22.062798',9,'https://www.youtube.com/watch?v=eLLfOVkp6so'),(70,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779509/ztudy/background-video-images/background-video_70_image.png','2025-03-12 18:35:06.801916','2025-03-12 18:38:30.454652',9,'https://www.youtube.com/watch?v=Wimkqo8gDZ0'),(71,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779516/ztudy/background-video-images/background-video_71_image.png','2025-03-12 18:35:14.986398','2025-03-12 18:38:37.729076',9,'https://www.youtube.com/watch?v=SEk7Bp6GZ7g'),(72,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1741779523/ztudy/background-video-images/background-video_72_image.png','2025-03-12 18:35:24.526120','2025-03-12 18:38:44.265333',9,'https://www.youtube.com/watch?v=eTD0WWFIDAg'),(73,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1743165982/ztudy/background-video-images/background-video_73_image.png','2025-03-29 19:42:03.531626','2025-03-31 22:44:46.704447',10,'https://www.youtube.com/embed/6An38kUcNFs'),(74,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1743435520/ztudy/background-video-images/background-video_74_image.png','2025-03-31 22:37:11.291927','2025-03-31 22:44:52.188254',10,'https://www.youtube.com/watch?v=vciMg0s-Gos'),(75,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1743524775/ztudy/background-video-images/background-video_75_image.png','2025-04-01 23:25:24.855283','2025-04-01 23:26:16.307129',10,'https://www.youtube.com/watch?v=gjWZzv0O9H8'),(81,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1743788743/ztudy/background-video-images/background-video_81_image.png','2025-04-05 00:44:32.731310','2025-04-05 00:45:43.584861',10,'https://www.youtube.com/watch?v=dLmczwDCEZI'),(115,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1743793769/ztudy/background-video-images/background-video_115_image.png','2025-04-05 02:09:27.622470','2025-04-05 02:09:29.787703',10,'https://www.youtube.com/watch?v=p3MivL4Fyk8'),(116,'image/upload/https://res.cloudinary.com/dloeqfbwm/image/upload/v1743794373/ztudy/background-video-images/background-video_116_image.png','2025-04-05 02:19:31.735077','2025-04-05 02:19:46.237551',10,'https://www.youtube.com/watch?v=kV3famkRaA4'),(117,NULL,'2025-04-06 18:36:53.001880','2025-04-06 18:36:53.006375',10,'https://www.youtube.com/watch?v=1BsTe0zPa-U');
/*!40000 ALTER TABLE `core_backgroundvideo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_backgroundvideotype`
--

DROP TABLE IF EXISTS `core_backgroundvideotype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_backgroundvideotype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `deleted_at` datetime(6) DEFAULT NULL,
  `restored_at` datetime(6) DEFAULT NULL,
  `transaction_id` char(32) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `description` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_backgroundvideotype`
--

LOCK TABLES `core_backgroundvideotype` WRITE;
/*!40000 ALTER TABLE `core_backgroundvideotype` DISABLE KEYS */;
INSERT INTO `core_backgroundvideotype` VALUES (1,NULL,NULL,NULL,'\\U0001f338 Anime','\\U0001f338 Anime','2025-02-25 06:55:00.269109','2025-03-09 04:28:28.623881'),(2,NULL,NULL,NULL,'\\U0001f4da Library','\\U0001f4da Library','2025-02-25 08:27:28.713839','2025-03-09 04:28:40.348026'),(3,NULL,NULL,NULL,'\\U0001f33f Nature','\\U0001f33f Nature','2025-03-06 17:45:58.325578','2025-03-09 04:28:49.674595'),(4,NULL,NULL,NULL,'\\U0001f431 Animals','\\U0001f431 Animals','2025-03-06 17:46:15.289841','2025-03-09 04:29:01.471900'),(5,NULL,NULL,NULL,'\\u2615 Cafe','\\u2615 Cafe','2025-03-06 17:46:32.533658','2025-03-09 04:29:16.653062'),(6,NULL,NULL,NULL,'\\U0001f4bb\\ufe0f\\ufe0f Desk','\\U0001f4bb\\ufe0f\\ufe0f Desk','2025-03-06 17:46:44.151045','2025-03-09 04:29:50.073775'),(7,NULL,NULL,NULL,'\\U0001f3d9\\ufe0f  City','\\U0001f3d9\\ufe0f  City','2025-03-06 17:47:01.193414','2025-03-09 04:29:38.321005'),(8,NULL,NULL,NULL,'\\U0001f308 Colors','\\U0001f308 Colors','2025-03-06 17:47:11.842661','2025-03-09 04:30:02.675517'),(9,NULL,NULL,NULL,'\\u2728 Other','\\u2728 Other','2025-03-06 17:47:21.961778','2025-03-09 04:30:12.926674'),(10,NULL,NULL,NULL,'\\u227d^\\u2022 \\u02d5 \\u2022 \\u0f80\\u0f72\\u227c','\\u227d^\\u2022 \\u02d5 \\u2022 \\u0f80\\u0f72\\u227c','2025-03-31 22:43:50.322795','2025-03-31 22:43:50.322795');
/*!40000 ALTER TABLE `core_backgroundvideotype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_interest`
--

DROP TABLE IF EXISTS `core_interest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_interest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_interest_user_id_category_id_6109df03_uniq` (`user_id`,`category_id`),
  KEY `core_interest_category_id_f7275b15_fk_core_roomcategory_id` (`category_id`),
  CONSTRAINT `core_interest_category_id_f7275b15_fk_core_roomcategory_id` FOREIGN KEY (`category_id`) REFERENCES `core_roomcategory` (`id`),
  CONSTRAINT `core_interest_user_id_efad404c_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_interest`
--

LOCK TABLES `core_interest` WRITE;
/*!40000 ALTER TABLE `core_interest` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_interest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_motivationalquote`
--

DROP TABLE IF EXISTS `core_motivationalquote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_motivationalquote` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quote` longtext NOT NULL,
  `author` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_motivationalquote`
--

LOCK TABLES `core_motivationalquote` WRITE;
/*!40000 ALTER TABLE `core_motivationalquote` DISABLE KEYS */;
INSERT INTO `core_motivationalquote` VALUES (1,'Success is the sum of small efforts, repeated day in and day out.','Robert Collier','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(2,'The future belongs to those who believe in the beauty of their dreams.','Eleanor Roosevelt','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(3,'Don\'t watch the clock; do what it does. Keep going.','Sam Levenson','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(4,'The only way to do great work is to love what you do.','Steve Jobs','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(5,'Education is the passport to the future, for tomorrow belongs to those who prepare for it today.','Malcolm X','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(6,'Believe you can and you\'re halfway there.','Theodore Roosevelt','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(7,'The expert in anything was once a beginner.','Helen Hayes','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(8,'Your education is a dress rehearsal for a life that is yours to lead.','Nora Ephron','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(9,'It always seems impossible until it’s done.','Nelson Mandela','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(10,'Work hard in silence, let your success be the noise.','Frank Ocean','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000');
/*!40000 ALTER TABLE `core_motivationalquote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_room`
--

DROP TABLE IF EXISTS `core_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_room` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(7) NOT NULL,
  `thumbnail` varchar(255) DEFAULT NULL,
  `code_invite` varchar(255) DEFAULT NULL,
  `max_participants` int DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `creator_user_id` bigint DEFAULT NULL,
  `category_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_room_creator_user_id_537a62ec_fk_core_user_id` (`creator_user_id`),
  KEY `core_room_category_id_95e22533_fk_core_roomcategory_id` (`category_id`),
  CONSTRAINT `core_room_category_id_95e22533_fk_core_roomcategory_id` FOREIGN KEY (`category_id`) REFERENCES `core_roomcategory` (`id`),
  CONSTRAINT `core_room_creator_user_id_537a62ec_fk_core_user_id` FOREIGN KEY (`creator_user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_room`
--

LOCK TABLES `core_room` WRITE;
/*!40000 ALTER TABLE `core_room` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_roomcategory`
--

DROP TABLE IF EXISTS `core_roomcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_roomcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `thumbnail` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_roomcategory`
--

LOCK TABLES `core_roomcategory` WRITE;
/*!40000 ALTER TABLE `core_roomcategory` DISABLE KEYS */;
INSERT INTO `core_roomcategory` VALUES (1,'\\U0001f3af Goal Setting & Productivity','Learn techniques to set and achieve personal and professional goals efficiently.','2025-02-28 06:57:05.231675','2025-03-09 04:20:38.632827','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_1_thumbnail.png'),(2,'\\U0001f4bb Programming & Coding','Engage in coding challenges and learn various programming languages.','2025-02-28 06:57:12.403610','2025-03-09 04:21:38.363590','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_2_thumbnail.png'),(3,'\\U0001f4da Academic Studies','Join discussions and study sessions for various academic subjects.','2025-02-28 06:57:16.999297','2025-03-09 04:21:48.471068','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_3_thumbnail.png'),(4,'\\U0001f5e3\\ufe0f Language Learning','Improve your speaking and comprehension skills in different languages.','2025-02-28 06:57:22.573353','2025-03-09 04:22:00.175884','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_4_thumbnail.png'),(5,'\\U0001f4ca Business & Entrepreneurship','Explore business strategies, startups, and financial literacy.','2025-02-28 06:57:49.036349','2025-03-09 04:22:08.641081','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_5_thumbnail.png'),(6,'\\U0001f3a8 Art & Creativity','Express yourself through drawing, painting, design, and creative thinking.','2025-02-28 06:57:55.733771','2025-03-09 04:22:16.254661','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_6_thumbnail.png'),(7,'\\U0001f3b5 Music & Instrument Learning','Learn how to play musical instruments and discuss music theory.','2025-02-28 06:58:01.591384','2025-03-09 04:22:26.237469','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_7_thumbnail.png'),(8,'\\U0001f4aa Health & Fitness','Discover workout routines, healthy diets, and mental well-being tips.','2025-02-28 06:58:05.861529','2025-03-09 04:22:36.380480','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_8_thumbnail.png'),(9,'\\U0001f9e9 Problem Solving & Critical Thinking','Engage in logical reasoning, puzzles, and brainstorming exercises.','2025-02-28 06:58:09.945305','2025-03-09 04:22:45.763464','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_9_thumbnail.png'),(10,'\\U0001f680 Science & Innovation','Discuss scientific discoveries, technology, and futuristic innovations.','2025-02-28 06:58:12.914683','2025-03-09 04:22:59.510492','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_10_thumbnail.png'),(11,'\\U0001f4dd Writing & Blogging','Improve your writing skills, explore storytelling, and learn about blogging.','2025-02-28 06:59:08.908841','2025-03-09 04:23:11.937304','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_11_thumbnail.png'),(12,'\\U0001f4d6 Book Club & Literature','Discuss classic and modern literature, book reviews, and storytelling techniques.','2025-02-28 06:59:23.025493','2025-03-09 04:23:19.835781','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_12_thumbnail.png'),(13,'\\U0001f3a5 Film & Media Studies','Analyze movies, cinematography, and media trends.','2025-02-28 06:59:28.018628','2025-03-09 04:23:27.026068','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_13_thumbnail.png'),(14,'\\U0001f3ae Gaming & Game Development','Discuss video games, strategies, and learn game development.','2025-02-28 06:59:33.162143','2025-03-09 04:23:34.853658','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_14_thumbnail.png'),(15,'\\U0001f9d8 Mindfulness & Meditation','Practice mindfulness, meditation, and stress management techniques.','2025-02-28 06:59:36.957548','2025-03-09 04:23:46.801230','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_15_thumbnail.png'),(16,'\\u2696\\ufe0f Law & Legal Studies','Explore legal concepts, rights, and justice systems.','2025-02-28 06:59:40.410811','2025-03-09 04:23:54.539301','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_16_thumbnail.png'),(17,'\\U0001f3e6 Personal Finance & Investing','Learn about budgeting, saving, and investing strategies.','2025-02-28 06:59:44.127827','2025-03-09 04:24:04.152389','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_17_thumbnail.png'),(18,'\\U0001f30d Travel & Cultural Exchange','Share travel experiences, cultural insights, and language tips.','2025-02-28 06:59:47.536245','2025-03-09 04:24:14.459728','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_18_thumbnail.png'),(19,'\\U0001f6e0\\ufe0f DIY & Handcrafts','Learn about crafting, DIY projects, and home improvement.','2025-02-28 06:59:51.055240','2025-03-09 04:24:23.182103','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_19_thumbnail.png'),(20,'\\U0001f373 Cooking & Culinary Arts','Explore cooking techniques, recipes, and food cultures.','2025-02-28 06:59:54.184714','2025-03-09 04:24:30.791165','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_20_thumbnail.png'),(21,'\\U0001f3c6 Sports & Athletics','Discuss sports training, events, and fitness techniques.','2025-02-28 07:00:01.178859','2025-03-09 04:25:06.149952','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_21_thumbnail.png'),(22,'\\U0001f3a4 Public Speaking & Debate','Develop confidence in public speaking and debate techniques.','2025-02-28 07:00:06.178908','2025-03-09 04:24:58.625573','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_22_thumbnail.png'),(23,'\\U0001f331 Sustainability & Environment','Learn about eco-friendly living, climate change, and conservation.','2025-02-28 07:00:09.516040','2025-03-09 04:25:18.943261','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_23_thumbnail.png'),(24,'\\U0001f4c8 Data Science & AI','Explore machine learning, artificial intelligence, and data analysis.','2025-02-28 07:00:12.717452','2025-03-09 04:25:33.888806','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_24_thumbnail.png'),(25,'\\U0001f527 Engineering & Technology','Discuss engineering principles, robotics, and tech innovations.','2025-02-28 07:00:16.162828','2025-03-09 04:25:43.399808','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_25_thumbnail.png'),(26,'\\U0001f6cd\\ufe0f Marketing & Branding','Learn about digital marketing, branding, and advertising strategies.','2025-02-28 07:00:19.871318','2025-03-09 04:25:50.961622','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_26_thumbnail.png'),(27,'\\U0001f3ad Theater & Performing Arts','Engage in acting, stage performance, and theatrical storytelling.','2025-02-28 07:00:27.237193','2025-03-09 04:26:02.112710','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_27_thumbnail.png'),(28,'\\U0001f91d Networking & Career Growth','Develop career skills, networking strategies, and job search tips.','2025-02-28 07:00:31.409968','2025-03-09 04:26:10.037457','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_28_thumbnail.png'),(29,'\\U0001f3e1 Home Organization & Minimalism','Learn about decluttering, home organization, and minimalist living.','2025-02-28 07:00:37.105055','2025-03-09 04:26:18.156417','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_29_thumbnail.png'),(30,'\\U0001f9e0 Memory & Learning Hacks','Enhance memory, speed reading, and effective study techniques.','2025-02-28 07:00:41.422591','2025-03-09 04:26:26.015011','https://res.cloudinary.com/dloeqfbwm/image/upload/v1742630702/ztudy/category_thumbnails/category_30_thumbnail.png');
/*!40000 ALTER TABLE `core_roomcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_roomparticipant`
--

DROP TABLE IF EXISTS `core_roomparticipant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_roomparticipant` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `joined_at` datetime(6) NOT NULL,
  `role` varchar(10) NOT NULL,
  `is_out` tinyint(1) NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `room_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_roomparticipant_room_id_446c364d_fk_core_room_id` (`room_id`),
  KEY `core_roomparticipant_user_id_fe6afefb_fk_core_user_id` (`user_id`),
  CONSTRAINT `core_roomparticipant_room_id_446c364d_fk_core_room_id` FOREIGN KEY (`room_id`) REFERENCES `core_room` (`id`),
  CONSTRAINT `core_roomparticipant_user_id_fe6afefb_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_roomparticipant`
--

LOCK TABLES `core_roomparticipant` WRITE;
/*!40000 ALTER TABLE `core_roomparticipant` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_roomparticipant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_sessiongoal`
--

DROP TABLE IF EXISTS `core_sessiongoal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_sessiongoal` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `goal` varchar(255) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_sessiongoal_user_id_91cce8e0_fk_core_user_id` (`user_id`),
  CONSTRAINT `core_sessiongoal_user_id_91cce8e0_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_sessiongoal`
--

LOCK TABLES `core_sessiongoal` WRITE;
/*!40000 ALTER TABLE `core_sessiongoal` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_sessiongoal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_sound`
--

DROP TABLE IF EXISTS `core_sound`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_sound` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `sound_file` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_sound`
--

LOCK TABLES `core_sound` WRITE;
/*!40000 ALTER TABLE `core_sound` DISABLE KEYS */;
INSERT INTO `core_sound` VALUES (1,'\\U0001f320 LoFi beats','2025-02-27 07:03:08.123205','2025-03-09 04:32:33.801226','sounds/1Lofi.mp3'),(2,'\\U0001f33f Nature sounds','2025-02-27 07:03:58.388247','2025-03-09 04:32:41.054153','sounds/2Nature.mp3'),(3,'\\U0001f4a7 Rain sounds','2025-02-27 07:04:08.200150','2025-03-09 04:32:50.212181','sounds/3rain-01.mp3'),(4,'\\U0001f525 Fireplace sounds','2025-02-27 07:04:21.710644','2025-03-09 04:32:58.749523','sounds/4Fire.mp3'),(5,'\\U0001f4da Library ambience','2025-02-27 07:04:28.652206','2025-03-09 04:33:11.636709','sounds/5Library.mp3'),(6,'\\U0001f3b9 Piano music','2025-02-27 07:04:37.502066','2025-03-09 04:33:19.069544','sounds/6piano.mp3'),(7,'\\U0001f3b7 Jazz music','2025-02-27 07:04:45.648010','2025-03-09 04:33:26.953778','sounds/7Jazz.mp3'),(8,'\\U0001f409 Studio Ghibli music','2025-02-27 07:04:55.410570','2025-03-09 04:33:33.783879','sounds/8Studioghibli.mp3'),(9,'\\U0001f9e0 Binaural beats','2025-02-27 07:05:12.080209','2025-03-09 04:33:59.209892','sounds/9Binauralbeats.mp3'),(10,'\\u2615 Coffee shop ambience','2025-02-27 07:05:21.695602','2025-03-09 04:34:08.887181','sounds/10Coffeeshop.mp3');
/*!40000 ALTER TABLE `core_sound` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_studysession`
--

DROP TABLE IF EXISTS `core_studysession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_studysession` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `total_time` double NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_studysession_user_id_c1460560_fk_core_user_id` (`user_id`),
  CONSTRAINT `core_studysession_user_id_c1460560_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_studysession`
--

LOCK TABLES `core_studysession` WRITE;
/*!40000 ALTER TABLE `core_studysession` DISABLE KEYS */;
INSERT INTO `core_studysession` VALUES (2,'2025-04-07',0.008331341111111112,2);
/*!40000 ALTER TABLE `core_studysession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user`
--

DROP TABLE IF EXISTS `core_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `restored_at` datetime(6) DEFAULT NULL,
  `transaction_id` char(32) DEFAULT NULL,
  `username` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_online` tinyint(1) NOT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `monthly_study_time` double NOT NULL,
  `monthly_level` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user`
--

LOCK TABLES `core_user` WRITE;
/*!40000 ALTER TABLE `core_user` DISABLE KEYS */;
INSERT INTO `core_user` VALUES (1,'pbkdf2_sha256$870000$ywx35ZfBmexPxtOU6Wb0am$Qu1JMwspCqifl2yl7RmtAroGkPDI/9ixGeapv9ynH9E=','2025-04-07 14:39:14.971909',1,'','',1,1,'2025-04-07 14:32:29.927085',NULL,NULL,NULL,'admin','admin@gmail.com',0,NULL,'2025-04-07 14:32:30.240428','2025-04-07 14:32:30.240428',0,'MEMBER'),(2,'pbkdf2_sha256$870000$EMeTaicQ5GCKOQfKgTpmSS$+AAnhs/2v2QEcTtAycWPgz68wZaqxNTo4NANjgPT/58=','2025-04-07 14:36:26.502584',0,'','',0,1,'2025-04-07 14:36:03.050780',NULL,NULL,NULL,'user1','user1@gmail.com',0,'https://res.cloudinary.com/dloeqfbwm/image/upload/v1742014468/ztudy/avatars/default_avatar.jpg','2025-04-07 14:36:03.358818','2025-04-07 14:36:03.366664',0.06988424583333333,'MEMBER');
/*!40000 ALTER TABLE `core_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user_groups`
--

DROP TABLE IF EXISTS `core_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_groups_user_id_group_id_c82fcad1_uniq` (`user_id`,`group_id`),
  KEY `core_user_groups_group_id_fe8c697f_fk_auth_group_id` (`group_id`),
  CONSTRAINT `core_user_groups_group_id_fe8c697f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `core_user_groups_user_id_70b4d9b8_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user_groups`
--

LOCK TABLES `core_user_groups` WRITE;
/*!40000 ALTER TABLE `core_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user_user_permissions`
--

DROP TABLE IF EXISTS `core_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_user_permissions_user_id_permission_id_73ea0daa_uniq` (`user_id`,`permission_id`),
  KEY `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` (`permission_id`),
  CONSTRAINT `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `core_user_user_permissions_user_id_085123d3_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user_user_permissions`
--

LOCK TABLES `core_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `core_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_useractivitylog`
--

DROP TABLE IF EXISTS `core_useractivitylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_useractivitylog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `joined_at` datetime(6) NOT NULL,
  `left_at` datetime(6) DEFAULT NULL,
  `interaction_count` int NOT NULL,
  `room_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_useractivitylog_room_id_94dc075e_fk_core_room_id` (`room_id`),
  KEY `core_useractivitylog_user_id_ddde4fb2_fk_core_user_id` (`user_id`),
  CONSTRAINT `core_useractivitylog_room_id_94dc075e_fk_core_room_id` FOREIGN KEY (`room_id`) REFERENCES `core_room` (`id`),
  CONSTRAINT `core_useractivitylog_user_id_ddde4fb2_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_useractivitylog`
--

LOCK TABLES `core_useractivitylog` WRITE;
/*!40000 ALTER TABLE `core_useractivitylog` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_useractivitylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_core_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (21,'account','emailaddress'),(22,'account','emailconfirmation'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(19,'authtoken','token'),(20,'authtoken','tokenproxy'),(4,'contenttypes','contenttype'),(12,'core','backgroundvideo'),(7,'core','backgroundvideotype'),(18,'core','interest'),(8,'core','motivationalquote'),(13,'core','room'),(9,'core','roomcategory'),(14,'core','roomparticipant'),(15,'core','sessiongoal'),(10,'core','sound'),(16,'core','studysession'),(11,'core','user'),(17,'core','useractivitylog'),(5,'sessions','session'),(6,'sites','site'),(23,'socialaccount','socialaccount'),(24,'socialaccount','socialapp'),(25,'socialaccount','socialtoken');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-04-07 14:05:37.859791'),(2,'contenttypes','0002_remove_content_type_name','2025-04-07 14:05:37.917718'),(3,'auth','0001_initial','2025-04-07 14:05:38.166085'),(4,'auth','0002_alter_permission_name_max_length','2025-04-07 14:05:38.217045'),(5,'auth','0003_alter_user_email_max_length','2025-04-07 14:05:38.221598'),(6,'auth','0004_alter_user_username_opts','2025-04-07 14:05:38.225786'),(7,'auth','0005_alter_user_last_login_null','2025-04-07 14:05:38.230356'),(8,'auth','0006_require_contenttypes_0002','2025-04-07 14:05:38.233364'),(9,'auth','0007_alter_validators_add_error_messages','2025-04-07 14:05:38.237378'),(10,'auth','0008_alter_user_username_max_length','2025-04-07 14:05:38.241508'),(11,'auth','0009_alter_user_last_name_max_length','2025-04-07 14:05:38.248421'),(12,'auth','0010_alter_group_name_max_length','2025-04-07 14:05:38.259513'),(13,'auth','0011_update_proxy_permissions','2025-04-07 14:05:38.266530'),(14,'auth','0012_alter_user_first_name_max_length','2025-04-07 14:05:38.270597'),(15,'core','0001_initial','2025-04-07 14:05:39.200873'),(16,'account','0001_initial','2025-04-07 14:05:39.345903'),(17,'account','0002_email_max_length','2025-04-07 14:05:39.362041'),(18,'account','0003_alter_emailaddress_create_unique_verified_email','2025-04-07 14:05:39.387009'),(19,'account','0004_alter_emailaddress_drop_unique_email','2025-04-07 14:05:39.409782'),(20,'account','0005_emailaddress_idx_upper_email','2025-04-07 14:05:39.432477'),(21,'account','0006_emailaddress_lower','2025-04-07 14:05:39.446608'),(22,'account','0007_emailaddress_idx_email','2025-04-07 14:05:39.486124'),(23,'account','0008_emailaddress_unique_primary_email_fixup','2025-04-07 14:05:39.502943'),(24,'account','0009_emailaddress_unique_primary_email','2025-04-07 14:05:39.510623'),(25,'admin','0001_initial','2025-04-07 14:05:39.649488'),(26,'admin','0002_logentry_remove_auto_add','2025-04-07 14:05:39.661045'),(27,'admin','0003_logentry_add_action_flag_choices','2025-04-07 14:05:39.672858'),(28,'authtoken','0001_initial','2025-04-07 14:05:39.757162'),(29,'authtoken','0002_auto_20160226_1747','2025-04-07 14:05:39.787256'),(30,'authtoken','0003_tokenproxy','2025-04-07 14:05:39.790326'),(31,'authtoken','0004_alter_tokenproxy_options','2025-04-07 14:05:39.794257'),(32,'sessions','0001_initial','2025-04-07 14:05:39.824982'),(33,'sites','0001_initial','2025-04-07 14:05:39.841018'),(34,'sites','0002_alter_domain_unique','2025-04-07 14:05:39.855296'),(35,'socialaccount','0001_initial','2025-04-07 14:05:40.231895'),(36,'socialaccount','0002_token_max_lengths','2025-04-07 14:05:40.278659'),(37,'socialaccount','0003_extra_data_default_dict','2025-04-07 14:05:40.290983'),(38,'socialaccount','0004_app_provider_id_settings','2025-04-07 14:05:40.433321'),(39,'socialaccount','0005_socialtoken_nullable_app','2025-04-07 14:05:40.626669'),(40,'socialaccount','0006_alter_socialaccount_extra_data','2025-04-07 14:05:40.690694');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('88btcm5d8vberwbyz96iwrana9vin2hv','.eJxVjMsOgyAQRf9l1o0B8b1rf4TMDEMkpZgodNP036uNG5fnPs4HkHkpKdu3rMEHcVZeGCJMqcR4A4slz7ZsstrgYIIaLhkhPyUdBcZ4xNWpq_6bs96q-06ScmDMYUmP83VRzbjNu4dN6x37FpXWPSnUuhvNTsy1Zt0MA_KA5NCRIiFlpB5bxIa4G6n3nYHvD5tsSKA:1u1h1X:sh9wCt2jgD89uZH6ElPmShXCS_9Gnvyj0MbP9tJV82s','2025-04-21 14:36:03.407409'),('hsk6plhu7vzrxkay3r1sz9fu39r83dby','.eJxVjMsOwiAQRf-FtSFAebp07zcQZhikaiAp7cr479qkC93ec859sZi2tcZt0BLnzM5MstPvBgkf1HaQ76ndOsfe1mUGviv8oINfe6bn5XD_Dmoa9Vt7IcFNzgiNWkH2iZQDsFlYazUGY01x0nidbKAwGaWD9wUdFcxKAgj2_gDBXTdV:1u1h4c:Pl689qAWBoGGO43B_kKP2pyz2_C07Iwi10cUp-g8d-E','2025-04-21 14:39:14.976142');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_site` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(200) NOT NULL,
  `uid` varchar(191) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` json NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_core_user_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialaccount`
--

LOCK TABLES `socialaccount_socialaccount` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(191) NOT NULL,
  `secret` varchar(191) NOT NULL,
  `key` varchar(191) NOT NULL,
  `provider_id` varchar(200) NOT NULL,
  `settings` json NOT NULL DEFAULT (_utf8mb4'{}'),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp`
--

LOCK TABLES `socialaccount_socialapp` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp_sites`
--

DROP TABLE IF EXISTS `socialaccount_socialapp_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp_sites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `socialapp_id` int NOT NULL,
  `site_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`),
  CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp_sites`
--

LOCK TABLES `socialaccount_socialapp_sites` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int NOT NULL,
  `app_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialtoken`
--

LOCK TABLES `socialaccount_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-07 14:40:43
