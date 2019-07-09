-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: infinera-prod.cnccf8ulxory.us-west-2.rds.amazonaws.com    Database: infinera_staging
-- ------------------------------------------------------
-- Server version	5.7.22-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `analysis_request`
--

DROP TABLE IF EXISTS `analysis_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analysis_request` (
  `analysis_request_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` int(11) DEFAULT NULL,
  `customer_name` varchar(5000) DEFAULT NULL,
  `analysis_name` varchar(45) DEFAULT NULL,
  `analysis_type` varchar(45) DEFAULT NULL,
  `request_type` varchar(45) DEFAULT NULL,
  `item_category` varchar(100) DEFAULT NULL,
  `product_category` varchar(100) DEFAULT NULL,
  `product_family` varchar(100) DEFAULT NULL,
  `product_phase` varchar(100) DEFAULT NULL,
  `product_type` varchar(100) DEFAULT NULL,
  `inservice_type` varchar(100) DEFAULT NULL,
  `replenish_time` varchar(45) DEFAULT NULL,
  `user_email_id` varchar(45) DEFAULT NULL,
  `analysis_request_time` datetime DEFAULT NULL,
  `dna_file_name` varchar(45) DEFAULT NULL,
  `current_inventory_file_name` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `requestStatus` varchar(100) DEFAULT 'Processing',
  `failure_reason` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`analysis_request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=387 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `analysis_type`
--

DROP TABLE IF EXISTS `analysis_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analysis_type` (
  `analysis_id` int(11) NOT NULL AUTO_INCREMENT,
  `analysis_type_name` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`analysis_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bom_record`
--

DROP TABLE IF EXISTS `bom_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bom_record` (
  `bom_record_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` varchar(45) DEFAULT NULL,
  `request_id` int(11) DEFAULT NULL,
  `part_name` varchar(45) DEFAULT NULL,
  `depot_name` varchar(45) DEFAULT NULL,
  `part_quantity` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`bom_record_id`)
) ENGINE=InnoDB AUTO_INCREMENT=188252 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `current_ib`
--

DROP TABLE IF EXISTS `current_ib`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `current_ib` (
  `current_ib_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` int(11) DEFAULT NULL,
  `product_ordering_name` varchar(45) DEFAULT NULL,
  `node_depot_belongs` varchar(45) DEFAULT NULL,
  `customer_name` varchar(5000) DEFAULT NULL,
  `pon_quanity` int(11) DEFAULT NULL,
  `request_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`current_ib_id`)
) ENGINE=InnoDB AUTO_INCREMENT=441898 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `current_inventory`
--

DROP TABLE IF EXISTS `current_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `current_inventory` (
  `current_inventory_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` int(11) DEFAULT NULL,
  `request_id` int(11) DEFAULT NULL,
  `plant_id` int(11) DEFAULT NULL,
  `storage_location` varchar(100) DEFAULT NULL,
  `material_number` varchar(45) DEFAULT NULL,
  `strip_material_number` varchar(45) DEFAULT NULL,
  `part_name` varchar(45) DEFAULT NULL,
  `total_stock` int(11) DEFAULT NULL,
  `reorder_point` int(11) DEFAULT NULL,
  `std_cost` varchar(45) DEFAULT NULL,
  `total_std_cost` varchar(45) DEFAULT NULL,
  `sto_qty` varchar(45) DEFAULT NULL,
  `del_qty` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`current_inventory_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7970758 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `cust_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_name` varchar(45) DEFAULT NULL,
  `cust_address` varchar(1000) DEFAULT NULL,
  `cust_country` varchar(45) DEFAULT NULL,
  `cust_industry` varchar(45) DEFAULT NULL,
  `cust_tz` varchar(45) DEFAULT NULL,
  `cust_geo` varchar(45) DEFAULT NULL,
  `cust_status` varchar(45) DEFAULT NULL,
  `cust_site_count` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`cust_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `customer_dna_record`
--

DROP TABLE IF EXISTS `customer_dna_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_dna_record` (
  `dna_record_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` int(11) DEFAULT NULL,
  `request_id` double DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `node_id` varchar(45) DEFAULT NULL,
  `node_name` varchar(45) DEFAULT NULL,
  `aid` varchar(45) DEFAULT NULL,
  `installed_eqpt` varchar(45) DEFAULT NULL,
  `part_ordering_name` varchar(45) DEFAULT NULL,
  `part_id` varchar(45) DEFAULT NULL,
  `serial` varchar(45) DEFAULT NULL,
  `strip_serial` varchar(45) DEFAULT NULL,
  `end_customer_id` varchar(45) DEFAULT NULL,
  `source_part_data` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`dna_record_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1066050 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `depot`
--

DROP TABLE IF EXISTS `depot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `depot` (
  `depot_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` int(11) DEFAULT NULL,
  `depot_name` varchar(45) DEFAULT NULL,
  `version_number` double DEFAULT NULL,
  `depot_address` varchar(100) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `state` varchar(45) DEFAULT NULL,
  `country` varchar(45) DEFAULT NULL,
  `region` varchar(45) DEFAULT NULL,
  `hub` int(11) DEFAULT NULL,
  `partner` varchar(45) DEFAULT NULL,
  `partner_warehouse_code` varchar(45) DEFAULT NULL,
  `contact` varchar(45) DEFAULT NULL,
  `lat` varchar(45) DEFAULT NULL,
  `long` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`depot_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5111 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ekryp_usecase`
--

DROP TABLE IF EXISTS `ekryp_usecase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ekryp_usecase` (
  `ekryp_usecase_id` int(11) NOT NULL AUTO_INCREMENT,
  `usecase` varchar(600) DEFAULT NULL,
  `brief_description` text,
  `description` text,
  PRIMARY KEY (`ekryp_usecase_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `end_customer`
--

DROP TABLE IF EXISTS `end_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `end_customer` (
  `end_cust_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` int(11) DEFAULT NULL,
  `end_cust_id_from_source` varchar(45) DEFAULT NULL,
  `end_cust_name` varchar(100) DEFAULT NULL,
  `end_cust_site_count` int(11) DEFAULT NULL,
  `end_cust_industry` varchar(45) DEFAULT NULL,
  `end_cust_target_market_segment` varchar(45) DEFAULT NULL,
  `end_cust_country` varchar(45) DEFAULT NULL,
  `end_cust_tz` varchar(45) DEFAULT NULL,
  `end_cust_geo` varchar(45) DEFAULT NULL,
  `end_cust_status` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`end_cust_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34989 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `error_records`
--

DROP TABLE IF EXISTS `error_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `error_records` (
  `error_record_id` int(11) NOT NULL AUTO_INCREMENT,
  `error_reason` varchar(100) DEFAULT NULL,
  `cust_id` varchar(45) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `PON` varchar(45) DEFAULT NULL,
  `node_name` varchar(45) DEFAULT NULL,
  `node_id` varchar(45) DEFAULT NULL,
  `aid` varchar(45) DEFAULT NULL,
  `installed_eqpt` varchar(45) DEFAULT NULL,
  `part` varchar(45) DEFAULT NULL,
  `serial` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `analysis_request_time` datetime DEFAULT NULL,
  `request_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`error_record_id`)
) ENGINE=InnoDB AUTO_INCREMENT=85316 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `faq_details`
--

DROP TABLE IF EXISTS `faq_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faq_details` (
  `faq_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(400) DEFAULT NULL,
  `image_url` varchar(600) DEFAULT NULL,
  `description` text,
  `permissions` text,
  PRIMARY KEY (`faq_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text,
  `feedback` text,
  `enable_flag` int(11) DEFAULT '0',
  `solution` text,
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `high_spare`
--

DROP TABLE IF EXISTS `high_spare`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `high_spare` (
  `high_spare_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` int(11) DEFAULT NULL,
  `part_name` varchar(45) DEFAULT NULL,
  `high_spare_part_name` varchar(45) DEFAULT NULL,
  `version_number` double DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`high_spare_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13237 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lab_request`
--

DROP TABLE IF EXISTS `lab_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lab_request` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `lab_resource` varchar(255) NOT NULL,
  `requested_date` varchar(255) NOT NULL,
  `start_time` varchar(255) NOT NULL,
  `end_time` varchar(2555) NOT NULL,
  `type` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `status` varchar(255) NOT NULL,
  `created_at` varchar(255) NOT NULL,
  `created_by` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lab_systems`
--

DROP TABLE IF EXISTS `lab_systems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lab_systems` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_name` varchar(255) NOT NULL,
  `product_type` varchar(255) NOT NULL,
  `ip_address` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `serial_console` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `misnomer_part_conversion`
--

DROP TABLE IF EXISTS `misnomer_part_conversion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `misnomer_part_conversion` (
  `reference_table_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` int(11) DEFAULT NULL,
  `misnomer_part_name` varchar(45) DEFAULT NULL,
  `correct_part_name` varchar(45) DEFAULT NULL,
  `version_number` double DEFAULT NULL,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`reference_table_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1376 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mtbf_bom_calculated`
--

DROP TABLE IF EXISTS `mtbf_bom_calculated`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mtbf_bom_calculated` (
  `bom_calculated_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` int(11) DEFAULT NULL,
  `part_name` varchar(45) DEFAULT NULL,
  `depot_name` varchar(45) DEFAULT NULL,
  `pon_quantity` int(11) DEFAULT NULL,
  `request_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`bom_calculated_id`)
) ENGINE=InnoDB AUTO_INCREMENT=449835 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `node`
--

DROP TABLE IF EXISTS `node`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `node` (
  `node_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` int(11) DEFAULT NULL,
  `node_name` varchar(45) DEFAULT NULL,
  `end_customer_node_belongs` varchar(100) DEFAULT NULL,
  `node_depot_belongs` varchar(100) DEFAULT NULL,
  `version_number` double DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`node_id`)
) ENGINE=InnoDB AUTO_INCREMENT=163330 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `part_cost`
--

DROP TABLE IF EXISTS `part_cost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `part_cost` (
  `part_cost_id` int(11) NOT NULL AUTO_INCREMENT,
  `part_id` int(11) DEFAULT NULL,
  `depot_name` varchar(45) DEFAULT NULL,
  `material_number` varchar(100) DEFAULT NULL,
  `standard_cost` double DEFAULT NULL,
  `source` varchar(45) DEFAULT NULL,
  `version_number` double DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`part_cost_id`)
) ENGINE=InnoDB AUTO_INCREMENT=195914 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parts`
--

DROP TABLE IF EXISTS `parts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parts` (
  `part_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` int(11) DEFAULT NULL,
  `part_number` int(11) DEFAULT NULL,
  `material_number` varchar(100) DEFAULT NULL,
  `part_name` varchar(45) DEFAULT NULL,
  `part_reliability_class` varchar(45) DEFAULT NULL,
  `spared_attribute` int(11) DEFAULT NULL,
  `version_number` double DEFAULT NULL,
  `source_part_data` varchar(45) DEFAULT NULL,
  `product_type` varchar(45) DEFAULT NULL,
  `product_family` varchar(45) DEFAULT NULL,
  `product_category` varchar(45) DEFAULT NULL,
  `item_category` varchar(45) DEFAULT NULL,
  `product_phase` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`part_id`)
) ENGINE=InnoDB AUTO_INCREMENT=252479 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prospect_details`
--

DROP TABLE IF EXISTS `prospect_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prospect_details` (
  `prospects_id` int(11) NOT NULL AUTO_INCREMENT,
  `prospects_email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`prospects_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prospect_status`
--

DROP TABLE IF EXISTS `prospect_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prospect_status` (
  `prospects_id` int(11) NOT NULL,
  `prospects_step` int(11) DEFAULT NULL,
  `analysis_request_time` datetime DEFAULT NULL,
  KEY `FK_prospects_step` (`prospects_step`),
  KEY `FK_prospects_id` (`prospects_id`),
  CONSTRAINT `FK_prospects_id` FOREIGN KEY (`prospects_id`) REFERENCES `prospect_details` (`prospects_id`),
  CONSTRAINT `FK_prospects_step` FOREIGN KEY (`prospects_step`) REFERENCES `prospect_steps` (`step_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prospect_steps`
--

DROP TABLE IF EXISTS `prospect_steps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prospect_steps` (
  `step_id` int(11) NOT NULL AUTO_INCREMENT,
  `step_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`step_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reference`
--

DROP TABLE IF EXISTS `reference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reference` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `isactive` tinyint(4) DEFAULT NULL,
  `filename` varchar(225) DEFAULT NULL,
  `user_email_id` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reliability_class`
--

DROP TABLE IF EXISTS `reliability_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reliability_class` (
  `reliability_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` int(11) DEFAULT NULL,
  `replenish_time` varchar(45) DEFAULT NULL,
  `replenish_timetable_id` int(11) DEFAULT NULL,
  `product_family` varchar(100) DEFAULT NULL,
  `1` int(11) DEFAULT NULL,
  `2` int(11) DEFAULT NULL,
  `3` int(11) DEFAULT NULL,
  `4` int(11) DEFAULT NULL,
  `5` int(11) DEFAULT NULL,
  `6` int(11) DEFAULT NULL,
  `7` int(11) DEFAULT NULL,
  `8` int(11) DEFAULT NULL,
  `9` int(11) DEFAULT NULL,
  `10` int(11) DEFAULT NULL,
  `version_number` double DEFAULT NULL,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`reliability_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2964 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `replenish_table`
--

DROP TABLE IF EXISTS `replenish_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `replenish_table` (
  `replenish_time_Id` int(11) NOT NULL AUTO_INCREMENT,
  `replenish_time_name` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`replenish_time_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=281 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `simple_bom_calculated`
--

DROP TABLE IF EXISTS `simple_bom_calculated`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `simple_bom_calculated` (
  `simple_bom_calculated_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` int(11) DEFAULT NULL,
  `part_name` varchar(45) DEFAULT NULL,
  `depot_name` varchar(45) DEFAULT NULL,
  `part_quantity` int(11) DEFAULT NULL,
  `request_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`simple_bom_calculated_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `summary`
--

DROP TABLE IF EXISTS `summary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `summary` (
  `summary_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_id` varchar(45) DEFAULT NULL,
  `request_id` int(11) DEFAULT NULL,
  `part_name` varchar(45) DEFAULT NULL,
  `depot_name` varchar(45) DEFAULT NULL,
  `material_number` varchar(45) DEFAULT NULL,
  `total_stock` int(11) DEFAULT NULL,
  `standard_cost` double DEFAULT NULL,
  `reorder_point` int(11) DEFAULT NULL,
  `shared_quantity` int(11) DEFAULT NULL,
  `high_spare` varchar(45) DEFAULT NULL,
  `net_total_stock` int(11) DEFAULT NULL,
  `net_reorder_point` int(11) DEFAULT NULL,
  `net_total_stock_cost` double DEFAULT NULL,
  `net_reorder_point_cost` double DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `customer_name` varchar(5000) DEFAULT NULL,
  `is_latest` varchar(1) DEFAULT 'Y',
  `request_type` varchar(45) DEFAULT NULL,
  `used_spare_count_total_stock` int(11) DEFAULT '0',
  `used_spare_count_reorder` int(11) DEFAULT '0',
  `High_spare_reoderpoint_cost` double DEFAULT '0',
  `High_spare_totalstock_cost` double DEFAULT '0',
  PRIMARY KEY (`summary_id`)
) ENGINE=InnoDB AUTO_INCREMENT=448299 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-20 16:06:45
