-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: smartllocksystem
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `access_time`
--

DROP TABLE IF EXISTS `access_time`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `access_time` (
  `access_time` datetime NOT NULL,
  PRIMARY KEY (`access_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `access_time`
--

LOCK TABLES `access_time` WRITE;
/*!40000 ALTER TABLE `access_time` DISABLE KEYS */;
/*!40000 ALTER TABLE `access_time` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valid_pin`
--

DROP TABLE IF EXISTS `valid_pin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `valid_pin` (
  `valid_pin` int(11) NOT NULL,
  `valid_pinnumber` int(11) NOT NULL,
  PRIMARY KEY (`valid_pinnumber`,`valid_pin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valid_pin`
--

LOCK TABLES `valid_pin` WRITE;
/*!40000 ALTER TABLE `valid_pin` DISABLE KEYS */;
INSERT INTO `valid_pin` VALUES (1,22222),(3,36452),(2,96352);
/*!40000 ALTER TABLE `valid_pin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valid_tagid`
--

DROP TABLE IF EXISTS `valid_tagid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `valid_tagid` (
  `valid_tagid` int(11) NOT NULL,
  `valid_tagidnumber` int(11) NOT NULL,
  PRIMARY KEY (`valid_tagid`,`valid_tagidnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valid_tagid`
--

LOCK TABLES `valid_tagid` WRITE;
/*!40000 ALTER TABLE `valid_tagid` DISABLE KEYS */;
INSERT INTO `valid_tagid` VALUES (1,789456),(2,654987),(3,321654);
/*!40000 ALTER TABLE `valid_tagid` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-12-02  1:50:56
