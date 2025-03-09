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
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_api_user_id` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
INSERT INTO `account_emailaddress` VALUES (1,'user1@gmail.com',0,1,2),(4,'user3@gmail.com',0,1,3),(5,'user2@gmail.com',0,1,4),(6,'user4@gmail.com',0,1,5),(7,'user5@gmail.com',0,1,6),(8,'user6@gmail.com',0,1,7),(9,'user7@gmail.com',0,1,8),(10,'user8@gmail.com',0,1,9),(11,'user9@gmail.com',0,1,10),(12,'user10@gmail.com',0,1,11);
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
-- Table structure for table `api_backgroundvideo`
--

DROP TABLE IF EXISTS `api_backgroundvideo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_backgroundvideo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `type_id` bigint NOT NULL,
  `youtube_code` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_backgroundvideo_type_id_7b6f77be_fk_api_backg` (`type_id`),
  CONSTRAINT `api_backgroundvideo_type_id_7b6f77be_fk_api_backg` FOREIGN KEY (`type_id`) REFERENCES `api_backgroundvideotype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_backgroundvideo`
--

LOCK TABLES `api_backgroundvideo` WRITE;
/*!40000 ALTER TABLE `api_backgroundvideo` DISABLE KEYS */;
INSERT INTO `api_backgroundvideo` VALUES (1,'https://study-together-static-prod.st-static.com/solo-thumbnails/1-1.png','2025-03-06 17:51:49.524164','2025-03-06 17:51:49.524164',1,'5wRWniH7rt8'),(2,'https://study-together-static-prod.st-static.com/solo-thumbnails/1-2.png','2025-03-07 18:04:20.085979','2025-03-07 18:04:20.085979',1,'1oahTaVIQvk');
/*!40000 ALTER TABLE `api_backgroundvideo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_backgroundvideotype`
--

DROP TABLE IF EXISTS `api_backgroundvideotype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_backgroundvideotype` (
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_backgroundvideotype`
--

LOCK TABLES `api_backgroundvideotype` WRITE;
/*!40000 ALTER TABLE `api_backgroundvideotype` DISABLE KEYS */;
INSERT INTO `api_backgroundvideotype` VALUES (1,NULL,NULL,NULL,'\\U0001f338 Anime','\\U0001f338 Anime','2025-02-25 06:55:00.269109','2025-03-09 04:28:28.623881'),(2,NULL,NULL,NULL,'\\U0001f4da Library','\\U0001f4da Library','2025-02-25 08:27:28.713839','2025-03-09 04:28:40.348026'),(3,NULL,NULL,NULL,'\\U0001f33f Nature','\\U0001f33f Nature','2025-03-06 17:45:58.325578','2025-03-09 04:28:49.674595'),(4,NULL,NULL,NULL,'\\U0001f431 Animals','\\U0001f431 Animals','2025-03-06 17:46:15.289841','2025-03-09 04:29:01.471900'),(5,NULL,NULL,NULL,'\\u2615 Cafe','\\u2615 Cafe','2025-03-06 17:46:32.533658','2025-03-09 04:29:16.653062'),(6,NULL,NULL,NULL,'\\U0001f4bb\\ufe0f\\ufe0f Desk','\\U0001f4bb\\ufe0f\\ufe0f Desk','2025-03-06 17:46:44.151045','2025-03-09 04:29:50.073775'),(7,NULL,NULL,NULL,'\\U0001f3d9\\ufe0f  City','\\U0001f3d9\\ufe0f  City','2025-03-06 17:47:01.193414','2025-03-09 04:29:38.321005'),(8,NULL,NULL,NULL,'\\U0001f308 Colors','\\U0001f308 Colors','2025-03-06 17:47:11.842661','2025-03-09 04:30:02.675517'),(9,NULL,NULL,NULL,'\\u2728 Other','\\u2728 Other','2025-03-06 17:47:21.961778','2025-03-09 04:30:12.926674');
/*!40000 ALTER TABLE `api_backgroundvideotype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_interest`
--

DROP TABLE IF EXISTS `api_interest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_interest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `category_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_interest_user_id_category_id_0ec35904_uniq` (`user_id`,`category_id`),
  KEY `api_interest_category_id_1fe85dec_fk_api_roomcategory_id` (`category_id`),
  CONSTRAINT `api_interest_category_id_1fe85dec_fk_api_roomcategory_id` FOREIGN KEY (`category_id`) REFERENCES `api_roomcategory` (`id`),
  CONSTRAINT `api_interest_user_id_7050e18c_fk_api_user_id` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_interest`
--

LOCK TABLES `api_interest` WRITE;
/*!40000 ALTER TABLE `api_interest` DISABLE KEYS */;
INSERT INTO `api_interest` VALUES (1,'2025-02-28 07:04:11.417716',1,2),(2,'2025-02-28 07:04:11.417716',2,2),(3,'2025-02-28 07:04:11.417716',3,2);
/*!40000 ALTER TABLE `api_interest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_motivationalquote`
--

DROP TABLE IF EXISTS `api_motivationalquote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_motivationalquote` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quote` longtext NOT NULL,
  `author` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_motivationalquote`
--

LOCK TABLES `api_motivationalquote` WRITE;
/*!40000 ALTER TABLE `api_motivationalquote` DISABLE KEYS */;
INSERT INTO `api_motivationalquote` VALUES (1,'Success is the sum of small efforts, repeated day in and day out.','Robert Collier','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(2,'The future belongs to those who believe in the beauty of their dreams.','Eleanor Roosevelt','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(3,'Don\'t watch the clock; do what it does. Keep going.','Sam Levenson','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(4,'The only way to do great work is to love what you do.','Steve Jobs','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(5,'Education is the passport to the future, for tomorrow belongs to those who prepare for it today.','Malcolm X','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(6,'Believe you can and you\'re halfway there.','Theodore Roosevelt','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(7,'The expert in anything was once a beginner.','Helen Hayes','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(8,'Your education is a dress rehearsal for a life that is yours to lead.','Nora Ephron','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(9,'It always seems impossible until it’s done.','Nelson Mandela','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000'),(10,'Work hard in silence, let your success be the noise.','Frank Ocean','2025-02-24 14:23:23.000000','2025-02-24 14:23:23.000000');
/*!40000 ALTER TABLE `api_motivationalquote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_room`
--

DROP TABLE IF EXISTS `api_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_room` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(7) NOT NULL,
  `code_invite` varchar(255) DEFAULT NULL,
  `max_participants` int DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `creator_user_id` bigint DEFAULT NULL,
  `category_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_room_creator_user_id_4862431b_fk_api_user_id` (`creator_user_id`),
  KEY `api_room_category_id_5da56573_fk_api_roomcategory_id` (`category_id`),
  CONSTRAINT `api_room_category_id_5da56573_fk_api_roomcategory_id` FOREIGN KEY (`category_id`) REFERENCES `api_roomcategory` (`id`),
  CONSTRAINT `api_room_creator_user_id_4862431b_fk_api_user_id` FOREIGN KEY (`creator_user_id`) REFERENCES `api_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_room`
--

LOCK TABLES `api_room` WRITE;
/*!40000 ALTER TABLE `api_room` DISABLE KEYS */;
INSERT INTO `api_room` VALUES (10,'room1','PUBLIC','mfu96x',10,'2025-03-07 14:23:38.599643','2025-03-07 16:57:03.615160',1,2,1),(11,'room2','PUBLIC','fnikpb',10,'2025-03-07 14:33:20.395029','2025-03-07 14:33:20.395029',1,3,1);
/*!40000 ALTER TABLE `api_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_roomcategory`
--

DROP TABLE IF EXISTS `api_roomcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_roomcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_roomcategory`
--

LOCK TABLES `api_roomcategory` WRITE;
/*!40000 ALTER TABLE `api_roomcategory` DISABLE KEYS */;
INSERT INTO `api_roomcategory` VALUES (1,'\\U0001f3af Goal Setting & Productivity','Learn techniques to set and achieve personal and professional goals efficiently.','2025-02-28 06:57:05.231675','2025-03-09 04:20:38.632827'),(2,'\\U0001f4bb Programming & Coding','Engage in coding challenges and learn various programming languages.','2025-02-28 06:57:12.403610','2025-03-09 04:21:38.363590'),(3,'\\U0001f4da Academic Studies','Join discussions and study sessions for various academic subjects.','2025-02-28 06:57:16.999297','2025-03-09 04:21:48.471068'),(4,'\\U0001f5e3\\ufe0f Language Learning','Improve your speaking and comprehension skills in different languages.','2025-02-28 06:57:22.573353','2025-03-09 04:22:00.175884'),(5,'\\U0001f4ca Business & Entrepreneurship','Explore business strategies, startups, and financial literacy.','2025-02-28 06:57:49.036349','2025-03-09 04:22:08.641081'),(6,'\\U0001f3a8 Art & Creativity','Express yourself through drawing, painting, design, and creative thinking.','2025-02-28 06:57:55.733771','2025-03-09 04:22:16.254661'),(7,'\\U0001f3b5 Music & Instrument Learning','Learn how to play musical instruments and discuss music theory.','2025-02-28 06:58:01.591384','2025-03-09 04:22:26.237469'),(8,'\\U0001f4aa Health & Fitness','Discover workout routines, healthy diets, and mental well-being tips.','2025-02-28 06:58:05.861529','2025-03-09 04:22:36.380480'),(9,'\\U0001f9e9 Problem Solving & Critical Thinking','Engage in logical reasoning, puzzles, and brainstorming exercises.','2025-02-28 06:58:09.945305','2025-03-09 04:22:45.763464'),(10,'\\U0001f680 Science & Innovation','Discuss scientific discoveries, technology, and futuristic innovations.','2025-02-28 06:58:12.914683','2025-03-09 04:22:59.510492'),(11,'\\U0001f4dd Writing & Blogging','Improve your writing skills, explore storytelling, and learn about blogging.','2025-02-28 06:59:08.908841','2025-03-09 04:23:11.937304'),(12,'\\U0001f4d6 Book Club & Literature','Discuss classic and modern literature, book reviews, and storytelling techniques.','2025-02-28 06:59:23.025493','2025-03-09 04:23:19.835781'),(13,'\\U0001f3a5 Film & Media Studies','Analyze movies, cinematography, and media trends.','2025-02-28 06:59:28.018628','2025-03-09 04:23:27.026068'),(14,'\\U0001f3ae Gaming & Game Development','Discuss video games, strategies, and learn game development.','2025-02-28 06:59:33.162143','2025-03-09 04:23:34.853658'),(15,'\\U0001f9d8 Mindfulness & Meditation','Practice mindfulness, meditation, and stress management techniques.','2025-02-28 06:59:36.957548','2025-03-09 04:23:46.801230'),(16,'\\u2696\\ufe0f Law & Legal Studies','Explore legal concepts, rights, and justice systems.','2025-02-28 06:59:40.410811','2025-03-09 04:23:54.539301'),(17,'\\U0001f3e6 Personal Finance & Investing','Learn about budgeting, saving, and investing strategies.','2025-02-28 06:59:44.127827','2025-03-09 04:24:04.152389'),(18,'\\U0001f30d Travel & Cultural Exchange','Share travel experiences, cultural insights, and language tips.','2025-02-28 06:59:47.536245','2025-03-09 04:24:14.459728'),(19,'\\U0001f6e0\\ufe0f DIY & Handcrafts','Learn about crafting, DIY projects, and home improvement.','2025-02-28 06:59:51.055240','2025-03-09 04:24:23.182103'),(20,'\\U0001f373 Cooking & Culinary Arts','Explore cooking techniques, recipes, and food cultures.','2025-02-28 06:59:54.184714','2025-03-09 04:24:30.791165'),(21,'\\U0001f3c6 Sports & Athletics','Discuss sports training, events, and fitness techniques.','2025-02-28 07:00:01.178859','2025-03-09 04:25:06.149952'),(22,'\\U0001f3a4 Public Speaking & Debate','Develop confidence in public speaking and debate techniques.','2025-02-28 07:00:06.178908','2025-03-09 04:24:58.625573'),(23,'\\U0001f331 Sustainability & Environment','Learn about eco-friendly living, climate change, and conservation.','2025-02-28 07:00:09.516040','2025-03-09 04:25:18.943261'),(24,'\\U0001f4c8 Data Science & AI','Explore machine learning, artificial intelligence, and data analysis.','2025-02-28 07:00:12.717452','2025-03-09 04:25:33.888806'),(25,'\\U0001f527 Engineering & Technology','Discuss engineering principles, robotics, and tech innovations.','2025-02-28 07:00:16.162828','2025-03-09 04:25:43.399808'),(26,'\\U0001f6cd\\ufe0f Marketing & Branding','Learn about digital marketing, branding, and advertising strategies.','2025-02-28 07:00:19.871318','2025-03-09 04:25:50.961622'),(27,'\\U0001f3ad Theater & Performing Arts','Engage in acting, stage performance, and theatrical storytelling.','2025-02-28 07:00:27.237193','2025-03-09 04:26:02.112710'),(28,'\\U0001f91d Networking & Career Growth','Develop career skills, networking strategies, and job search tips.','2025-02-28 07:00:31.409968','2025-03-09 04:26:10.037457'),(29,'\\U0001f3e1 Home Organization & Minimalism','Learn about decluttering, home organization, and minimalist living.','2025-02-28 07:00:37.105055','2025-03-09 04:26:18.156417'),(30,'\\U0001f9e0 Memory & Learning Hacks','Enhance memory, speed reading, and effective study techniques.','2025-02-28 07:00:41.422591','2025-03-09 04:26:26.015011');
/*!40000 ALTER TABLE `api_roomcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_roomparticipant`
--

DROP TABLE IF EXISTS `api_roomparticipant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_roomparticipant` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `joined_at` datetime(6) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `room_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `is_out` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_roomparticipant_room_id_b0603d42_fk_api_room_id` (`room_id`),
  KEY `api_roomparticipant_user_id_41db2f94_fk_api_user_id` (`user_id`),
  CONSTRAINT `api_roomparticipant_room_id_b0603d42_fk_api_room_id` FOREIGN KEY (`room_id`) REFERENCES `api_room` (`id`),
  CONSTRAINT `api_roomparticipant_user_id_41db2f94_fk_api_user_id` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_roomparticipant`
--

LOCK TABLES `api_roomparticipant` WRITE;
/*!40000 ALTER TABLE `api_roomparticipant` DISABLE KEYS */;
INSERT INTO `api_roomparticipant` VALUES (13,'2025-03-07 14:23:38.603631',1,10,2,1,1),(14,'2025-03-07 14:25:30.027490',0,10,4,1,1),(15,'2025-03-07 14:33:20.398402',1,11,3,0,0),(16,'2025-03-07 14:33:28.931328',0,11,4,1,0);
/*!40000 ALTER TABLE `api_roomparticipant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_sessiongoal`
--

DROP TABLE IF EXISTS `api_sessiongoal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_sessiongoal` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `goal` varchar(255) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_sessiongoal_user_id_88a2e561_fk_api_user_id` (`user_id`),
  CONSTRAINT `api_sessiongoal_user_id_88a2e561_fk_api_user_id` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_sessiongoal`
--

LOCK TABLES `api_sessiongoal` WRITE;
/*!40000 ALTER TABLE `api_sessiongoal` DISABLE KEYS */;
INSERT INTO `api_sessiongoal` VALUES (2,'string','COMPLETED','2025-02-26 12:28:46.032051','2025-02-26 12:29:29.503016',2),(3,'string2','OPEN','2025-02-26 12:49:23.957629','2025-02-26 12:49:23.957629',2);
/*!40000 ALTER TABLE `api_sessiongoal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_sound`
--

DROP TABLE IF EXISTS `api_sound`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_sound` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `sound_file` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_sound`
--

LOCK TABLES `api_sound` WRITE;
/*!40000 ALTER TABLE `api_sound` DISABLE KEYS */;
INSERT INTO `api_sound` VALUES (1,'\\U0001f320 LoFi beats','2025-02-27 07:03:08.123205','2025-03-09 04:32:33.801226','sounds/1Lofi.mp3'),(2,'\\U0001f33f Nature sounds','2025-02-27 07:03:58.388247','2025-03-09 04:32:41.054153','sounds/2Nature.mp3'),(3,'\\U0001f4a7 Rain sounds','2025-02-27 07:04:08.200150','2025-03-09 04:32:50.212181','sounds/3rain-01.mp3'),(4,'\\U0001f525 Fireplace sounds','2025-02-27 07:04:21.710644','2025-03-09 04:32:58.749523','sounds/4Fire.mp3'),(5,'\\U0001f4da Library ambience','2025-02-27 07:04:28.652206','2025-03-09 04:33:11.636709','sounds/5Library.mp3'),(6,'\\U0001f3b9 Piano music','2025-02-27 07:04:37.502066','2025-03-09 04:33:19.069544','sounds/6piano.mp3'),(7,'\\U0001f3b7 Jazz music','2025-02-27 07:04:45.648010','2025-03-09 04:33:26.953778','sounds/7Jazz.mp3'),(8,'\\U0001f409 Studio Ghibli music','2025-02-27 07:04:55.410570','2025-03-09 04:33:33.783879','sounds/8Studioghibli.mp3'),(9,'\\U0001f9e0 Binaural beats','2025-02-27 07:05:12.080209','2025-03-09 04:33:59.209892','sounds/9Binauralbeats.mp3'),(10,'\\u2615 Coffee shop ambience','2025-02-27 07:05:21.695602','2025-03-09 04:34:08.887181','sounds/10Coffeeshop.mp3');
/*!40000 ALTER TABLE `api_sound` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_user`
--

DROP TABLE IF EXISTS `api_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `restored_at` datetime(6) DEFAULT NULL,
  `transaction_id` char(32) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `api_user_email_9ef5afa6_uniq` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_user`
--

LOCK TABLES `api_user` WRITE;
/*!40000 ALTER TABLE `api_user` DISABLE KEYS */;
INSERT INTO `api_user` VALUES (1,'pbkdf2_sha256$870000$xMKWe29tm3YYdpbopZe1Cz$vDp2pMSDJj6u73P2dlkrtqA7VVtQVrjIHBTVnQOBn4M=','2025-03-06 08:06:12.609711',1,'baobui','','',1,1,'2025-02-26 12:14:41.196439',NULL,NULL,NULL,'hongbao2003@gmail.com','2025-02-26 12:14:41.485540','2025-02-26 12:14:41.485540'),(2,'pbkdf2_sha256$870000$j3tlmchd2R32gpaDPdPqSG$cO4ORpNlZDH6oIYfMHbtE2MVCE4MkcgYZGPSRF2JaNY=','2025-03-07 17:16:41.781989',0,'user1','','',0,1,'2025-02-26 12:25:20.797620',NULL,NULL,NULL,'user1@gmail.com','2025-02-26 12:25:21.110403','2025-02-26 12:25:21.110403'),(3,'pbkdf2_sha256$870000$j3tlmchd2R32gpaDPdPqSG$cO4ORpNlZDH6oIYfMHbtE2MVCE4MkcgYZGPSRF2JaNY=','2025-03-01 07:02:38.515493',0,'user3','','',0,1,'2025-03-01 07:02:38.201805',NULL,NULL,NULL,'user3@gmail.com','2025-03-01 07:02:38.502709','2025-03-01 07:02:38.502709'),(4,'pbkdf2_sha256$870000$hbcwtYC6xy9AOOenZSjgsP$t+74j+Jk0X1u6EytL91hjTRejnujPBS3cg4NI6qsBII=','2025-03-07 16:58:48.617312',0,'user2','','',0,1,'2025-03-01 07:03:13.406795',NULL,NULL,NULL,'user2@gmail.com','2025-03-01 07:03:13.696516','2025-03-01 07:03:13.696516'),(5,'pbkdf2_sha256$870000$HmeKUeTd1UIQoIGPtxAbdE$+xLEHBAqS8pgX/vTEeU+YG4mpVEIlWO2V74xynIH46o=','2025-03-01 07:03:22.570604',0,'user4','','',0,1,'2025-03-01 07:03:22.253365',NULL,NULL,NULL,'user4@gmail.com','2025-03-01 07:03:22.542718','2025-03-01 07:03:22.542718'),(6,'pbkdf2_sha256$870000$HmlnpN606aC2u4Dskub0lE$ExzA5JBXnZXaj8Of0X0IUiwE7cNmyAnPxcRSjr39Guc=','2025-03-01 07:03:25.795193',0,'user5','','',0,1,'2025-03-01 07:03:25.450371',NULL,NULL,NULL,'user5@gmail.com','2025-03-01 07:03:25.757597','2025-03-01 07:03:25.757597'),(7,'pbkdf2_sha256$870000$Ie6rsetcwsgKHKtg9UOIth$SJRrWd/iDnEANfiRnfmLDeqG2VFiN19KeSR4y16RTx8=','2025-03-01 07:03:29.051555',0,'user6','','',0,1,'2025-03-01 07:03:28.740748',NULL,NULL,NULL,'user6@gmail.com','2025-03-01 07:03:29.040990','2025-03-01 07:03:29.040990'),(8,'pbkdf2_sha256$870000$SH01vLlXOpR1n5c95IiBn6$YuFBO2ixUVPc1q1nrZ4eHZZ7u4JTcHysZDjsxh+cfGU=','2025-03-01 07:03:35.307335',0,'user7','','',0,1,'2025-03-01 07:03:34.973377',NULL,NULL,NULL,'user7@gmail.com','2025-03-01 07:03:35.277342','2025-03-01 07:03:35.277342'),(9,'pbkdf2_sha256$870000$21vVXs4YtFna87RTnwnMKH$J8fVPp+04IuZv4zLIXOmQbI6aYtbdwKwyXWk9mDnC+Q=','2025-03-01 07:03:37.781073',0,'user8','','',0,1,'2025-03-01 07:03:37.483739',NULL,NULL,NULL,'user8@gmail.com','2025-03-01 07:03:37.771210','2025-03-01 07:03:37.771210'),(10,'pbkdf2_sha256$870000$7Qw8WgsKslLkfNvnOCamLA$XdVmT3DjzGvX51EOwqECkvw9FOnESSSguyqn9ZvefQ8=','2025-03-01 07:03:41.264870',0,'user9','','',0,1,'2025-03-01 07:03:40.957513',NULL,NULL,NULL,'user9@gmail.com','2025-03-01 07:03:41.255211','2025-03-01 07:03:41.255211'),(11,'pbkdf2_sha256$870000$HLust3mdZHukZ8ySgqBRvf$Q/UAIGcZPT4MT1tMi43g/0w7XQ7F1ePdkL4N/bNwb1k=','2025-03-01 07:03:45.117258',0,'user10','','',0,1,'2025-03-01 07:03:44.789422',NULL,NULL,NULL,'user10@gmail.com','2025-03-01 07:03:45.089615','2025-03-01 07:03:45.089615');
/*!40000 ALTER TABLE `api_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_user_groups`
--

DROP TABLE IF EXISTS `api_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_user_groups_user_id_group_id_9c7ddfb5_uniq` (`user_id`,`group_id`),
  KEY `api_user_groups_group_id_3af85785_fk_auth_group_id` (`group_id`),
  CONSTRAINT `api_user_groups_group_id_3af85785_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `api_user_groups_user_id_a5ff39fa_fk_api_user_id` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_user_groups`
--

LOCK TABLES `api_user_groups` WRITE;
/*!40000 ALTER TABLE `api_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_user_user_permissions`
--

DROP TABLE IF EXISTS `api_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_user_user_permissions_user_id_permission_id_a06dd704_uniq` (`user_id`,`permission_id`),
  KEY `api_user_user_permis_permission_id_305b7fea_fk_auth_perm` (`permission_id`),
  CONSTRAINT `api_user_user_permis_permission_id_305b7fea_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `api_user_user_permissions_user_id_f3945d65_fk_api_user_id` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_user_user_permissions`
--

LOCK TABLES `api_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `api_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_useractivitylog`
--

DROP TABLE IF EXISTS `api_useractivitylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_useractivitylog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `joined_at` datetime(6) NOT NULL,
  `left_at` datetime(6) DEFAULT NULL,
  `interaction_count` int NOT NULL,
  `room_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_useractivitylog_room_id_7b6a7f02_fk_api_room_id` (`room_id`),
  KEY `api_useractivitylog_user_id_d357f7e9_fk_api_user_id` (`user_id`),
  CONSTRAINT `api_useractivitylog_room_id_7b6a7f02_fk_api_room_id` FOREIGN KEY (`room_id`) REFERENCES `api_room` (`id`),
  CONSTRAINT `api_useractivitylog_user_id_d357f7e9_fk_api_user_id` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_useractivitylog`
--

LOCK TABLES `api_useractivitylog` WRITE;
/*!40000 ALTER TABLE `api_useractivitylog` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_useractivitylog` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add site',6,'add_site'),(22,'Can change site',6,'change_site'),(23,'Can delete site',6,'delete_site'),(24,'Can view site',6,'view_site'),(25,'Can add background video type',7,'add_backgroundvideotype'),(26,'Can change background video type',7,'change_backgroundvideotype'),(27,'Can delete background video type',7,'delete_backgroundvideotype'),(28,'Can view background video type',7,'view_backgroundvideotype'),(29,'Can add motivational quote',8,'add_motivationalquote'),(30,'Can change motivational quote',8,'change_motivationalquote'),(31,'Can delete motivational quote',8,'delete_motivationalquote'),(32,'Can view motivational quote',8,'view_motivationalquote'),(33,'Can add user',9,'add_user'),(34,'Can change user',9,'change_user'),(35,'Can delete user',9,'delete_user'),(36,'Can view user',9,'view_user'),(37,'Can add background video',10,'add_backgroundvideo'),(38,'Can change background video',10,'change_backgroundvideo'),(39,'Can delete background video',10,'delete_backgroundvideo'),(40,'Can view background video',10,'view_backgroundvideo'),(41,'Can add session goal',11,'add_sessiongoal'),(42,'Can change session goal',11,'change_sessiongoal'),(43,'Can delete session goal',11,'delete_sessiongoal'),(44,'Can view session goal',11,'view_sessiongoal'),(45,'Can add Token',12,'add_token'),(46,'Can change Token',12,'change_token'),(47,'Can delete Token',12,'delete_token'),(48,'Can view Token',12,'view_token'),(49,'Can add Token',13,'add_tokenproxy'),(50,'Can change Token',13,'change_tokenproxy'),(51,'Can delete Token',13,'delete_tokenproxy'),(52,'Can view Token',13,'view_tokenproxy'),(53,'Can add email address',14,'add_emailaddress'),(54,'Can change email address',14,'change_emailaddress'),(55,'Can delete email address',14,'delete_emailaddress'),(56,'Can view email address',14,'view_emailaddress'),(57,'Can add email confirmation',15,'add_emailconfirmation'),(58,'Can change email confirmation',15,'change_emailconfirmation'),(59,'Can delete email confirmation',15,'delete_emailconfirmation'),(60,'Can view email confirmation',15,'view_emailconfirmation'),(61,'Can add social account',16,'add_socialaccount'),(62,'Can change social account',16,'change_socialaccount'),(63,'Can delete social account',16,'delete_socialaccount'),(64,'Can view social account',16,'view_socialaccount'),(65,'Can add social application',17,'add_socialapp'),(66,'Can change social application',17,'change_socialapp'),(67,'Can delete social application',17,'delete_socialapp'),(68,'Can view social application',17,'view_socialapp'),(69,'Can add social application token',18,'add_socialtoken'),(70,'Can change social application token',18,'change_socialtoken'),(71,'Can delete social application token',18,'delete_socialtoken'),(72,'Can view social application token',18,'view_socialtoken'),(73,'Can add sound',19,'add_sound'),(74,'Can change sound',19,'change_sound'),(75,'Can delete sound',19,'delete_sound'),(76,'Can view sound',19,'view_sound'),(77,'Can add room category',20,'add_roomcategory'),(78,'Can change room category',20,'change_roomcategory'),(79,'Can delete room category',20,'delete_roomcategory'),(80,'Can view room category',20,'view_roomcategory'),(81,'Can add room',21,'add_room'),(82,'Can change room',21,'change_room'),(83,'Can delete room',21,'delete_room'),(84,'Can view room',21,'view_room'),(85,'Can add room participant',22,'add_roomparticipant'),(86,'Can change room participant',22,'change_roomparticipant'),(87,'Can delete room participant',22,'delete_roomparticipant'),(88,'Can view room participant',22,'view_roomparticipant'),(89,'Can add interest',23,'add_interest'),(90,'Can change interest',23,'change_interest'),(91,'Can delete interest',23,'delete_interest'),(92,'Can view interest',23,'view_interest'),(93,'Can add user activity log',24,'add_useractivitylog'),(94,'Can change user activity log',24,'change_useractivitylog'),(95,'Can delete user activity log',24,'delete_useractivitylog'),(96,'Can view user activity log',24,'view_useractivitylog');
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
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_api_user_id` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`)
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
  KEY `django_admin_log_user_id_c564eba6_fk_api_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_api_user_id` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-03-03 17:49:17.899756','5','Free idea exchange',2,'[{\"changed\": {\"fields\": [\"Category\"]}}]',21,1),(2,'2025-03-03 17:49:31.342844','1','Welcome to the community!',2,'[{\"changed\": {\"fields\": [\"Category\"]}}]',21,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (14,'account','emailaddress'),(15,'account','emailconfirmation'),(1,'admin','logentry'),(10,'api','backgroundvideo'),(7,'api','backgroundvideotype'),(23,'api','interest'),(8,'api','motivationalquote'),(21,'api','room'),(20,'api','roomcategory'),(22,'api','roomparticipant'),(11,'api','sessiongoal'),(19,'api','sound'),(9,'api','user'),(24,'api','useractivitylog'),(3,'auth','group'),(2,'auth','permission'),(12,'authtoken','token'),(13,'authtoken','tokenproxy'),(4,'contenttypes','contenttype'),(5,'sessions','session'),(6,'sites','site'),(16,'socialaccount','socialaccount'),(17,'socialaccount','socialapp'),(18,'socialaccount','socialtoken');
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
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-02-25 06:52:09.508412'),(2,'contenttypes','0002_remove_content_type_name','2025-02-25 06:52:09.553395'),(3,'auth','0001_initial','2025-02-25 06:52:09.716996'),(4,'auth','0002_alter_permission_name_max_length','2025-02-25 06:52:09.758387'),(5,'auth','0003_alter_user_email_max_length','2025-02-25 06:52:09.762413'),(6,'auth','0004_alter_user_username_opts','2025-02-25 06:52:09.766602'),(7,'auth','0005_alter_user_last_login_null','2025-02-25 06:52:09.770613'),(8,'auth','0006_require_contenttypes_0002','2025-02-25 06:52:09.772100'),(9,'auth','0007_alter_validators_add_error_messages','2025-02-25 06:52:09.775125'),(10,'auth','0008_alter_user_username_max_length','2025-02-25 06:52:09.780107'),(11,'auth','0009_alter_user_last_name_max_length','2025-02-25 06:52:09.787119'),(12,'auth','0010_alter_group_name_max_length','2025-02-25 06:52:09.797579'),(13,'auth','0011_update_proxy_permissions','2025-02-25 06:52:09.802180'),(14,'auth','0012_alter_user_first_name_max_length','2025-02-25 06:52:09.805164'),(15,'api','0001_initial','2025-02-25 06:52:10.119142'),(16,'account','0001_initial','2025-02-25 06:52:10.239601'),(17,'account','0002_email_max_length','2025-02-25 06:52:10.252935'),(18,'account','0003_alter_emailaddress_create_unique_verified_email','2025-02-25 06:52:10.272259'),(19,'account','0004_alter_emailaddress_drop_unique_email','2025-02-25 06:52:10.296542'),(20,'account','0005_emailaddress_idx_upper_email','2025-02-25 06:52:10.316062'),(21,'account','0006_emailaddress_lower','2025-02-25 06:52:10.328190'),(22,'account','0007_emailaddress_idx_email','2025-02-25 06:52:10.358995'),(23,'account','0008_emailaddress_unique_primary_email_fixup','2025-02-25 06:52:10.368970'),(24,'account','0009_emailaddress_unique_primary_email','2025-02-25 06:52:10.374970'),(25,'admin','0001_initial','2025-02-25 06:52:10.465039'),(26,'admin','0002_logentry_remove_auto_add','2025-02-25 06:52:10.470413'),(27,'admin','0003_logentry_add_action_flag_choices','2025-02-25 06:52:10.475786'),(28,'authtoken','0001_initial','2025-02-25 06:52:10.533555'),(29,'authtoken','0002_auto_20160226_1747','2025-02-25 06:52:10.551284'),(30,'authtoken','0003_tokenproxy','2025-02-25 06:52:10.554289'),(31,'authtoken','0004_alter_tokenproxy_options','2025-02-25 06:52:10.557297'),(32,'sessions','0001_initial','2025-02-25 06:52:10.579991'),(33,'sites','0001_initial','2025-02-25 06:52:10.589615'),(34,'sites','0002_alter_domain_unique','2025-02-25 06:52:10.598207'),(35,'socialaccount','0001_initial','2025-02-25 06:52:10.863762'),(36,'socialaccount','0002_token_max_lengths','2025-02-25 06:52:10.897087'),(37,'socialaccount','0003_extra_data_default_dict','2025-02-25 06:52:10.903601'),(38,'socialaccount','0004_app_provider_id_settings','2025-02-25 06:52:11.025106'),(39,'socialaccount','0005_socialtoken_nullable_app','2025-02-25 06:52:11.115180'),(40,'socialaccount','0006_alter_socialaccount_extra_data','2025-02-25 06:52:11.158743'),(41,'api','0002_sound','2025-02-27 06:45:49.584183'),(42,'api','0003_remove_sound_url_sound_sound_file','2025-02-27 06:59:04.228873'),(43,'api','0004_roomcategory_alter_sound_sound_file_room_and_more','2025-02-28 06:11:40.141208'),(44,'api','0005_interest','2025-02-28 06:34:51.161376'),(45,'api','0006_alter_user_email','2025-02-28 09:32:18.199939'),(46,'api','0007_alter_user_email','2025-02-28 09:49:39.292990'),(47,'api','0008_useractivitylog','2025-03-01 13:10:31.243498'),(48,'api','0009_rename_link_invite_room_code_invite','2025-03-05 15:45:30.071140'),(49,'api','0010_roomparticipant_is_approved_roomparticipant_is_out','2025-03-07 13:43:16.123673'),(50,'api','0011_remove_backgroundvideo_url_and_more','2025-03-07 18:00:53.198684');
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
INSERT INTO `django_session` VALUES ('0gbymy80u50yfiqff4jlzxy549fetscf','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPqU:3Ci63B7-9nQUx2RerdO4IlVZJszQ3IjCvO1GAc8PS7o','2025-03-18 10:49:54.920606'),('0pfrwd9ql81a9yzw9jpo52okdnb43h77','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPXv:hrsjGoXwqRT1K2AadRspWYq1blChuxI3pvKVKhLUMRg','2025-03-18 10:30:43.368976'),('28x4azbgfomnlxvthcja1v8np8el1b8t','.eJxVjMEOwiAQRP-FsyFsypbiTX-k2S5LIDY0ETgZ_93W9KDHeTPzXmqm3tLcqzznHNRVWXX5ZQvxQ8pR0LoeWBPz1kvT381ZV33bk5SWmVreyv18_akS1bR7YAlGhCaOYhGiheBYJDqLjhbB0ftoAL0BCsZgmNANyDg4AAxxjE69P92_PIE:1tqYdc:UFNkEsrGDCFSX3XWp93EiRlWttXLB5Nru0MCmdYQWFw','2025-03-21 14:25:20.600363'),('2kma42gkw662hhr2qxchd9rrvzki22j8','.eJxVjMEOwiAQRP-FsyFsypbiTX-k2S5LIDY0ETgZ_93W9KDHeTPzXmqm3tLcqzznHNRVWXX5ZQvxQ8pR0LoeWBPz1kvT381ZV33bk5SWmVreyv18_akS1bR7YAlGhCaOYhGiheBYJDqLjhbB0ftoAL0BCsZgmNANyDg4AAxxjE69P92_PIE:1tqb28:iET4bppvXxLUE2b0Cdozd8v5iFOt2g7aiq4UA-HLepw','2025-03-21 16:58:48.623837'),('3par9zey0121wc8wxfe0th8g85yzszcu','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPpt:WMV5-cI8oulwT_zj8bzsMXgeHpeX-H5a2qqaYv4WW9o','2025-03-18 10:49:17.785499'),('3uqimir3nv20j6x3affm4yqtmeovce0k','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpOlG:yuJkpigfxmFr289hUjsJVxuvAYPkz_qapBdajJWBs18','2025-03-18 09:40:26.576045'),('4sphjrvwp31hoi67bnq5sgq3opday8uy','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpOoL:sX94TXkM6H9Pire7ra0rsrTOujBa9bMWBxmNGI5WBn0','2025-03-18 09:43:37.928163'),('4yxvd86cpw087ikgted53wwg23iyus1w','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPZR:4j0ZzJqXL-x2hKt3W-tdrPgqLd2WEL8Lm-geHGB5vgg','2025-03-18 10:32:17.049190'),('6f910d3xki3p9icztsjy3qotp8lp7v8l','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpOoM:puSkUlNrVsY-7iFr-EAWMmR_ZBKPbagABMdYpYbky3g','2025-03-18 09:43:38.912675'),('86f81z4564bdojlxdzsrkfg31yzdjw98','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpOlF:0yEMj4rI_no8TGVR6CftJzkBXd2Sane00hsp-vRMNoo','2025-03-18 09:40:25.690475'),('8dlsdfayegtk0n0jb8epstvztgqq83ng','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPsy:mPCJmzCPHf1u8GqC2m7Q-71ISvrFwp_yAqRI-Ugct5w','2025-03-18 10:52:28.742393'),('aqlzbuzs81gpvi0uw4h1isurgzdos3es','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpOni:tA1c703C7hUgnL27qbK46izyCmSuLx-x50kv7Leh_ck','2025-03-18 09:42:58.054610'),('bljzdh16dzpvm9r3om047df6zun92y9n','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPdV:AbGHejsdlXB2D8uU-nQdYYRGo_FdmvuNzqfvcENPIuA','2025-03-18 10:36:29.553243'),('dhwt7qbtisczx4glwo260ktvqu68vyhj','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tqYFt:_aCUMUKo0ziUvdQVJ9egqOaYMPHern5wI0LJ9uCqu_E','2025-03-21 14:00:49.350588'),('ea241f9ylkkmzwg1mpagm0pbff2uh3w3','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPvH:IcugYN9-elrpUF-Tn_89FsTr7GCv8BniMUA4VHHvXgE','2025-03-18 10:54:51.246996'),('etabyj0ml9qq2li8f2tky5vqw80suec6','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPdS:2P3JUol1iFed5XA80TTLo8UCJmyxhH7FjfGr6MCLUrc','2025-03-18 10:36:26.580691'),('f5171o9drpvkttc1689zwop8kca0tla0','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPdT:1-U0yjbY0_3iCjtujq-i6fnF_MvWQMfgojkeqbwdrDo','2025-03-18 10:36:27.878846'),('fa3uchrgop08p2s9uu82daaa1gnmbob8','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPrn:nfnbBrokHNmZ48rIPvxPqBkZIeIbOMx8Wfhz34j2DNA','2025-03-18 10:51:15.058671'),('fcavydzaxwsp0cfdov3v7qpsjo3ad0mc','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPXX:BGnQSfxHUawyB9SGu58VKFZp_YfDP8O6T4X55Gv80n0','2025-03-18 10:30:19.991997'),('fdcukgig2qk5344rrq6j02utmx4o94b5','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tqamz:9NkpwlBC_uLUOIiUZNWIKp37usYf-PMcP6xxv_dtgkM','2025-03-21 16:43:09.342271'),('g6cqanz5h57mmpawpnxis65xjhaf646u','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPXq:AayiNL2x6fNa-bbn7Z0wFcYmY0rQbrW3LeUnXHQITCY','2025-03-18 10:30:38.243482'),('gzt0f6keolz5jt65ow5f5rz39gldwc6d','.eJxVjMEOwiAQRP-FsyFsypbiTX-k2S5LIDY0ETgZ_93W9KDHeTPzXmqm3tLcqzznHNRVWXX5ZQvxQ8pR0LoeWBPz1kvT381ZV33bk5SWmVreyv18_akS1bR7YAlGhCaOYhGiheBYJDqLjhbB0ftoAL0BCsZgmNANyDg4AAxxjE69P92_PIE:1tqYGU:Fx_1cNja__WjQ8V-o8X9PLBrSkkGSYw9xIHjNFqG1gE','2025-03-21 14:01:26.363398'),('hx1ex1vwwgazdanr7i0mmkhlzvxfnagp','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpOl4:HfEhGRXMrfhWBMrdOawIOktpkkQC89T_-TjrG1pKLck','2025-03-18 09:40:14.850810'),('jm08hvjhosrwtevz2uulb9etb7kuwpzj','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPti:EoxwRjGD087-BRH1N-H4SIQXrJQB3zh_r6PS1mcbq8o','2025-03-18 10:53:14.944417'),('jycv4ggb5igmesyw3aump8x4u8jw2fmb','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpOoG:OMsXgee5yOWkyd4-Ttxbsc8qTMsASgXn729TIvTFIk4','2025-03-18 09:43:32.925910'),('k7os35k6vqb4iywpsysa6m2sm97md1ag','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpOlG:yuJkpigfxmFr289hUjsJVxuvAYPkz_qapBdajJWBs18','2025-03-18 09:40:26.753676'),('kd8biy41necq3n71uln363b6vcfb8xdc','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPZQ:hm2tGqEpPoxT-hAoC3DzfUWQ3HLoRSF9tl-etodAS1w','2025-03-18 10:32:16.012471'),('knop2i2mfn5dtpmud8dqrh50mdeiyhc7','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpOnp:toqkC2frpxhk0lGyedd47zUMiJYTspC3FXNU0sk8qwc','2025-03-18 09:43:05.828214'),('kzb3k6kfn89sbxwivkls9w0at4gqcs4c','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpQ3Y:X_lOftcN8GI0d2RGWftGuFeRpBOYvbQI2Vt_J3pWyS0','2025-03-18 11:03:24.913610'),('ls1e8a12jsmqnnt9m7cmtgphm5qgcpm5','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPqj:JWEbEUg3pCax7eIxijU5U1qxsQSa36E5IbntuuTYY_A','2025-03-18 10:50:09.723136'),('mkl2j59dpvqi1n5h6008c9w7tlc878fl','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPdF:4-veoi98scPbYDIuocEc2JcnuGeR-FUHJb8SM06cq84','2025-03-18 10:36:13.711711'),('nwcmcftdyq2tzy19mzft6lfpw7khj46f','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpOnp:toqkC2frpxhk0lGyedd47zUMiJYTspC3FXNU0sk8qwc','2025-03-18 09:43:05.174495'),('owikuwa1adyy27uskdmars7hb3mfdp2a','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPsU:I8JJuNkVoqCWkiIE3IkQD-BywitifsZbQ9YXhAwBmjg','2025-03-18 10:51:58.143900'),('q3999m8rqmj5y6uh10a5cvpfzdkt88b5','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPXY:MJsTAYzskAzOYNH02UtNyzg-C3KSt215M75xhTwEcB0','2025-03-18 10:30:20.732233'),('qcc30xlond634c2dqmqtzi6asba1m4ip','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPya:4Rfmnlyh7Tt9KmRs-P89Uz5qsO71lgu2pz8SMGxAx9c','2025-03-18 10:58:16.620761'),('qgr5zkaxm7d9u6wkobjhrs3i71c1tnbw','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPdV:AbGHejsdlXB2D8uU-nQdYYRGo_FdmvuNzqfvcENPIuA','2025-03-18 10:36:29.426207'),('r1x2wg722oi2mdejdec5cfvbw97grvio','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPrl:5xqnJSzU8w4-PXT8Dr2TaeCrfg9KbMupJUoUixa1Y20','2025-03-18 10:51:13.776551'),('rba8gztjp1x5shbodha7hrl8nlgch6zk','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPtP:A_UyC2ZiPLpdbsbRaY0_u0Y0eFcNZ_mfjEkzhMaiU2k','2025-03-18 10:52:55.171115'),('rcniisvu3am5ee5f2a4w969olr15r1yz','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPvB:IJnV9uliO1qN3igM8uWKgJvhZ_OzZkNnI37lqD3DzzE','2025-03-18 10:54:45.590873'),('setzig6nzv0nkfci5xegzui09pvx8c4u','.eJxVjMEOgyAQRP-Fc2MUXVBv7Y-QXXaNpBQThV6a_nu18eJx3sy8j0Lvl5Kye8sapiDs5IUhqjGVGG_KYcmzK5usLrAalVYXRuifko4CYzxwdeqq_-ast-q-J0k5eMxhSY_zdVHNuM27p2ceeltTwyiaDbbMgIQEbJt26KijGgSmzmgEg3qorQVrSDzIJNCT-v4AoJRIcA:1tnGTZ:c3FEBzeAh7yJEyCt8zh5iFwPKqBEpwLKCutcsGwVMkg','2025-03-12 12:25:21.156957'),('tllvpep8ais8ciqeznw4ykmhpdqb0t04','.eJxVjMsOwiAQRf-FtSEMj7bj0r3fQAYGpGogKe3K-O_apAvd3nPOfQlP21r81tPiZxZnAeL0uwWKj1R3wHeqtyZjq-syB7kr8qBdXhun5-Vw_w4K9fKtk6IA1g6gSZsUyQzIGA1EhBwMOo1GZzdaAgvKKUWjZp4mzBQBFZJ4fwDOBTct:1tp9mH:wT7bIrs-giZchx9O3aC8MHor-Xfg0cerYE0R3owE9zo','2025-03-17 17:40:29.041382'),('to1qsrmj8n7jrdpm58y0rpii408h08iz','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpQ3h:ZL-D-0tgnoK9mmYxgfETgdX7i2yjjvHR9fLsEmRskqo','2025-03-18 11:03:33.565346'),('vtjzu5fr18wd2p0njvtxgrdvd9mqb18d','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpQ3V:fwHDFvMKsAIeIVXA8e3P7v43gbp10sUG2BKA6wn5NnM','2025-03-18 11:03:21.906113'),('vua5a5z7mlw1i7dksoq83h4tiqhosvw9','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpOoI:CaWLjpElOvDqO7WZJNeBYqt0iUSZ7i_KY-PqecOUD_g','2025-03-18 09:43:34.740754'),('vuiwgb2zctjk7r0gmq2i0uo2ztwo273g','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPm1:kja8dCRCE-X3iGCHnabrq1lBosFl2rllJgqLrVroV1I','2025-03-18 10:45:17.123327'),('w8d7bhel4tbfz643c4lo00ov30n962k8','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tqbJR:lYZk4Z6cOvkk-0V-Edp1kY5u7KkOpXe1pNUNuVMHkgg','2025-03-21 17:16:41.812014'),('wm7d7zg0q4j939a2ds6kcmbv10mbbx34','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPXb:s8eGdMMWbHCqRbk6OdK7i5Z9TLx1tHwlsd5zEy3kDtw','2025-03-18 10:30:23.216635'),('xpx9y8jh61m2m3pf6c2mquos9hx9j4vl','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpQQs:hQEnYMNs-fFQMl0yZQf9nWT7mBFCLMdyF1a3IqmVqbs','2025-03-18 11:27:30.271898'),('y70sbuyecce2txemqqz02e0dmsonqtke','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPzU:u_yJ33HLdjB_ie4kHXKqo6Y8r8pb1nmKV0FiB8352Cw','2025-03-18 10:59:12.023977'),('yaylmlm1ojmv7dq3tpye61qvoeg5botz','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpOoP:eBpYIXvwqBa43SINHpaSXc31t0XQFgOuhQd9XDQFAVo','2025-03-18 09:43:41.266261'),('ylqlgrk39bb1rn5hz656z0flv90e0ite','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpOno:jplluslUYs7gOedHk9z54cNsAROXiwxzJm8DJlfE4GQ','2025-03-18 09:43:04.093400'),('za8sgyhqd2wr5u7i5ihaym293tbvhjw8','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPlg:49NGmR37kNhENH8uSvl_BHgOJmK_Ru9ytAT6HfI7cuc','2025-03-18 10:44:56.832270'),('zwja6onpsy2bsw75hlgl9no5n1ikvptm','.eJxVjMEOgjAQRP-lZ0PqAkvxJj_SLNvdtJGURNqT8d8Fw0GP897MvIynWqKvmzx9CuZmwFx-2Uz8kHwIWpYDN8S81lyab-fUW3Pfk-SSmEpa83Su_q4ibXH_6cfOOgzaItows0I7KIsjRNfRoFZ3rQizVeqD5VEgADkL0LKMVw3m_QG9yTyq:1tpPxI:i5n84CdOPfN0h1LrMF_wOUcOhRDwYLigOQWqRWjysMY','2025-03-18 10:56:56.349032');
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
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_api_user_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_api_user_id` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`)
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

-- Dump completed on 2025-03-09 11:35:59
