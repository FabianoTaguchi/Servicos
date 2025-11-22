-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: agromail
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `cultivares`
--

DROP TABLE IF EXISTS `cultivares`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cultivares` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `especie` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cultivares`
--

LOCK TABLES `cultivares` WRITE;
/*!40000 ALTER TABLE `cultivares` DISABLE KEYS */;
INSERT INTO `cultivares` VALUES (1,'Soja','Tipo I','2025-11-22 17:25:08'),(2,'Soja','Tipo II','2025-11-22 17:25:14'),(3,'Algodão','Tipo I','2025-11-22 17:25:19'),(4,'Algodão','Tipo II','2025-11-22 17:25:23'),(5,'Girassol','Tipo I','2025-11-22 17:25:28'),(6,'Girassol','Tipo II','2025-11-22 17:25:33');
/*!40000 ALTER TABLE `cultivares` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordens`
--

DROP TABLE IF EXISTS `ordens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordens` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descricao` text COLLATE utf8mb4_unicode_ci,
  `quantidade` int DEFAULT NULL,
  `sla` text COLLATE utf8mb4_unicode_ci,
  `data_entrega` date DEFAULT NULL,
  `data_finalizacao` datetime DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'aberta',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `solicitante_id` int NOT NULL,
  `cultivar_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_ordens_status` (`status`),
  KEY `ix_ordens_solicitante` (`solicitante_id`),
  KEY `fk_ordens_cultivar` (`cultivar_id`),
  CONSTRAINT `fk_ordens_cultivar` FOREIGN KEY (`cultivar_id`) REFERENCES `cultivares` (`id`),
  CONSTRAINT `fk_ordens_user` FOREIGN KEY (`solicitante_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordens`
--

LOCK TABLES `ordens` WRITE;
/*!40000 ALTER TABLE `ordens` DISABLE KEYS */;
INSERT INTO `ordens` VALUES (1,'Ordem para Algodão - Tipo II','Entregar na portaria',100,'Alto','2025-11-25',NULL,'aberta','2025-11-22 17:25:57','2025-11-22 17:25:57',2,4),(2,'Ordem para Girassol - Tipo I','Entregar na Fazenda X',250,'Médio','2025-11-28','2025-11-22 17:27:05','finalizado','2025-11-22 17:26:12','2025-11-22 17:27:05',2,5),(3,'Ordem para Soja - Tipo I','Entregar no departamento de pesquisa',1000,'Alto','2025-11-29',NULL,'aberta','2025-11-22 17:26:51','2025-11-22 17:26:51',3,1),(4,'Ordem para Algodão - Tipo II','Entregar na Fazenda Y',250,'Alta','2025-11-25',NULL,'aberta','2025-11-22 17:29:14','2025-11-22 17:29:14',3,4);
/*!40000 ALTER TABLE `ordens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'solicitante',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_user_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'adm','adm','operador','2025-11-22 17:24:33'),(2,'teste1','teste123','solicitante','2025-11-22 17:24:44'),(3,'teste2','teste123','solicitante','2025-11-22 17:24:52');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-22 17:29:58
