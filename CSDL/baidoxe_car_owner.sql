-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: baidoxe
-- ------------------------------------------------------
-- Server version	8.0.29

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
-- Table structure for table `car_owner`
--

DROP TABLE IF EXISTS `car_owner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `car_owner` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Mã chủ xe',
  `name` varchar(250) DEFAULT NULL COMMENT 'Họ và tên',
  `identity_id` varchar(45) DEFAULT NULL COMMENT 'CMND/CCCD',
  `number_plate` varchar(45) DEFAULT NULL COMMENT 'Biển số xe',
  `ticket_code` varchar(45) DEFAULT NULL COMMENT 'Mã vé',
  `ticket_type` varchar(250) DEFAULT NULL COMMENT 'Loại vé (Vé ngày, Vé tuần, Vé tháng, Vé năm)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Lưu thông tin chủ xe đã đăng ký vé';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car_owner`
--

LOCK TABLES `car_owner` WRITE;
/*!40000 ALTER TABLE `car_owner` DISABLE KEYS */;
INSERT INTO `car_owner` VALUES (1,'Trần Văn Nam','00341125467','G241GH','TK001','Vé tháng'),(2,'Nguyễn Thu Hà','00341132467','CZI7KOD','TK001','Vé tuần'),(3,'Trịnh Quý Công','00141125467','MH14TC206AN','TK001','Vé năm'),(4,'Nguyễn Nam Hải','00341545467','7XFT96','TK001','Vé tháng'),(5,'Vũ Thu Phương','00341125237','MH20EE7597','TK001','Vé tháng'),(6,'Nguyễn Thu Hoài','00341125367','51A01204','TK001','Vé năm'),(7,'Vũ Thị Sen','00341125467','51F07973','TK001','Vé tháng'),(8,'Trần Văn Nam','00341125432','51F61712','TK001','Vé tuần'),(9,'Đặng Thái Quý','00341125454','51F88270','TK001','Vé tháng'),(10,'Nguyễn Tuấn Hải','00341125322','51A89714','TK001','Vé tháng'),(11,'Trịnh Thu Thảo','00323435123','51F86988','TK011','Vé tháng'),(12,'Vũ Văn Hòa','00312435663','77ZFK8','TK012','Vé tháng'),(13,'Lâm Đình Phong','00312435433','PJ323K','TK013','Vé tuần'),(14,'Vũ Thu Trà','00212435433','JP548J','TK014','Vé tuần'),(15,'Vũ Thị Hải Yến','00212435432','56ZFDL','TK015','Vé tháng'),(16,'Trần Văn Năm','00031254545','KL16J3636','TK16','Vé năm');
/*!40000 ALTER TABLE `car_owner` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-17 16:31:00
