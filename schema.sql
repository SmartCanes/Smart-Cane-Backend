-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: mysql:3306
-- Generation Time: Apr 23, 2026 at 11:45 AM
-- Server version: 8.0.44
-- PHP Version: 8.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_cane_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `account_history_tbl`
--

CREATE TABLE `account_history_tbl` (
  `history_id` int NOT NULL,
  `guardian_id` int NOT NULL,
  `device_id` int DEFAULT NULL,
  `action` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `account_history_tbl`
--

INSERT INTO `account_history_tbl` (`history_id`, `guardian_id`, `device_id`, `action`, `description`, `created_at`) VALUES
(1, 1, 1, 'PAIR', 'Macy Soto paired device SC-136901', '2026-03-27 04:40:56'),
(2, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-03-27 04:41:04'),
(3, 1, 1, 'CREATE', 'Macy Soto created VIP profile for Ivan Villamora', '2026-03-27 04:42:34'),
(4, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-03-30 04:25:48'),
(5, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-03-30 04:49:43'),
(6, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-03-30 07:12:57'),
(7, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-03-31 04:24:34'),
(8, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-03-31 04:27:37'),
(9, 1, 1, 'UPDATE', 'Macy Soto updated VIP profile for Ivan Villamora', '2026-03-31 04:34:49'),
(10, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-01 02:04:19'),
(11, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-06 03:35:31'),
(12, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-12 11:29:00'),
(13, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-13 00:31:01'),
(14, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-13 10:02:42'),
(15, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-13 14:43:19'),
(16, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-13 15:13:47'),
(17, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-13 15:16:52'),
(18, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-16 06:20:42'),
(19, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-16 06:59:06'),
(20, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-16 06:59:47'),
(21, 1, 1, 'INVITE', 'Macy Soto invited africa.christine.delluta@gmail.com to monitor a device', '2026-04-16 07:57:52'),
(22, 1, 1, 'INVITE', 'Macy Soto invited christinedelluta@gmail.com to monitor a device', '2026-04-16 08:00:36'),
(23, 2, NULL, 'LOGIN', 'Guardian Christine Africa logged in.', '2026-04-16 08:02:50'),
(24, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-16 08:11:32'),
(25, 1, 1, 'REMOVE_GUARDIAN', 'Macy Soto removed Christine Africa from device 1', '2026-04-16 08:20:44'),
(26, 1, 1, 'UNPAIR', 'Macy Soto unpaired device with serial SC-136901', '2026-04-16 09:22:02'),
(27, 3, 1, 'PAIR', 'Mary Visto paired device SC-136901', '2026-04-16 09:25:44'),
(28, 3, NULL, 'LOGIN', 'Guardian Mary Visto logged in.', '2026-04-16 09:26:07'),
(29, 3, NULL, 'LOGIN', 'Guardian Mary Visto logged in.', '2026-04-16 09:42:14'),
(30, 3, 1, 'CREATE', 'Mary Visto created VIP profile for Ivan Villamora', '2026-04-16 09:43:17'),
(31, 3, NULL, 'LOGIN', 'Guardian Mary Visto logged in.', '2026-04-16 09:43:49'),
(32, 3, NULL, 'LOGIN', 'Guardian Mary Visto logged in.', '2026-04-16 09:48:00'),
(33, 3, 1, 'INVITE', 'Mary Visto invited villamora.ivanren.manguiat@gmail.com to monitor a device', '2026-04-16 11:01:44'),
(34, 1, 1, 'ACCEPT_INVITE', 'Macy Soto accepted the invitation to monitor device 1', '2026-04-16 11:02:10'),
(35, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-16 11:02:46'),
(36, 3, 1, 'UPDATE_ROLE', 'Mary Visto changed Macy Soto\'s role to secondary on device SC-136901', '2026-04-16 11:05:45'),
(37, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-17 02:19:36'),
(38, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-17 02:23:10'),
(39, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-17 02:23:22'),
(40, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-17 02:23:58'),
(41, 3, NULL, 'LOGIN', 'Guardian Mary Visto logged in.', '2026-04-17 02:26:19'),
(42, 3, 1, 'UNPAIR', 'Mary Visto unpaired device with serial SC-136901', '2026-04-17 02:26:31'),
(43, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-17 02:26:40'),
(44, 1, 1, 'PAIR', 'Macy Soto paired device SC-136901', '2026-04-17 02:27:01'),
(45, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-17 02:27:03'),
(46, 1, 2, 'PAIR', 'Macy Soto paired device SC-136902', '2026-04-17 02:29:32'),
(47, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-17 02:31:06'),
(48, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-17 02:32:14'),
(49, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-17 02:47:05'),
(50, 1, 3, 'PAIR', 'Macy Soto paired device SC-136903', '2026-04-17 03:22:54'),
(51, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-17 07:25:55'),
(52, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-17 07:39:34'),
(53, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-17 23:25:51'),
(54, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-17 23:37:11'),
(55, 1, 1, 'CREATE', 'Macy Soto created VIP profile for Ivan Villamora', '2026-04-17 23:54:04'),
(56, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-18 00:26:09'),
(57, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-18 00:26:49'),
(58, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-18 00:28:07'),
(59, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-18 01:16:46'),
(60, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-18 01:39:19'),
(61, 3, NULL, 'LOGIN', 'Guardian Mary Visto logged in.', '2026-04-20 14:07:12'),
(62, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-21 05:26:55'),
(63, 1, NULL, 'LOGIN', 'Guardian Macy Soto logged in.', '2026-04-21 05:29:35');

-- --------------------------------------------------------

--
-- Table structure for table `admin_archive_tbl`
--

CREATE TABLE `admin_archive_tbl` (
  `archive_id` int NOT NULL,
  `admin_id` int NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `middle_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) NOT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `province` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `barangay` varchar(100) DEFAULT NULL,
  `street_address` text,
  `role` varchar(50) NOT NULL,
  `profile_image_url` varchar(500) DEFAULT NULL,
  `original_created_at` timestamp NULL DEFAULT NULL,
  `archived_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `archived_by` int DEFAULT NULL,
  `archived_reason_code` varchar(50) DEFAULT NULL,
  `archived_reason_text` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `admin_audit_logs_tbl`
--

CREATE TABLE `admin_audit_logs_tbl` (
  `audit_id` int NOT NULL,
  `actor_admin_id` int NOT NULL,
  `target_admin_id` int DEFAULT NULL,
  `action_type` varchar(100) NOT NULL,
  `old_value_json` text,
  `new_value_json` text,
  `reason_code` varchar(100) DEFAULT NULL,
  `reason_text` text,
  `status` enum('success','failed') NOT NULL,
  `ip_address` varchar(64) DEFAULT NULL,
  `user_agent` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `admin_audit_log_tbl`
--

CREATE TABLE `admin_audit_log_tbl` (
  `audit_id` bigint NOT NULL,
  `actor_admin_id` int NOT NULL,
  `target_admin_id` int DEFAULT NULL,
  `target_concern_id` int DEFAULT NULL,
  `action_type` varchar(50) NOT NULL,
  `old_value_json` text,
  `new_value_json` text,
  `reason_code` varchar(50) NOT NULL,
  `reason_text` varchar(500) NOT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'success',
  `failure_message` varchar(255) DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `admin_audit_log_tbl`
--

INSERT INTO `admin_audit_log_tbl` (`audit_id`, `actor_admin_id`, `target_admin_id`, `target_concern_id`, `action_type`, `old_value_json`, `new_value_json`, `reason_code`, `reason_text`, `status`, `failure_message`, `ip_address`, `user_agent`, `created_at`) VALUES
(16, 1, NULL, NULL, 'device_create', NULL, '{\"device_id\": 6, \"device_serial_number\": \"SC-136907\"}', 'device_create', 'Device SC-136907 registered.', 'success', NULL, '127.0.0.1', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-21 07:20:58'),
(17, 1, NULL, NULL, 'device_delete', '{\"deleted_device_id\": 6, \"deleted_device_serial\": \"SC-136900\", \"is_paired\": false, \"vip_id\": null}', NULL, 'duplicate_device', 'faswedfwadwadad', 'restored', NULL, '127.0.0.1', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-21 07:21:35'),
(18, 1, NULL, NULL, 'device_update', '{\"device_serial_number\": \"SC-136905\"}', '{\"device_serial_number\": \"SC-136900121\"}', 'device_update', 'Device 5 updated.', 'success', NULL, '127.0.0.1', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-21 07:23:44'),
(19, 1, NULL, 15, 'concern_delete', NULL, NULL, 'spam', 'dfesfsfsfsfs', 'restored', NULL, '127.0.0.1', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-21 07:27:29'),
(20, 1, NULL, 17, 'concern_delete', NULL, NULL, 'spam', 'dadadawdwadadwwda', 'success', NULL, '127.0.0.1', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-21 07:31:44'),
(21, 1, NULL, NULL, 'admin_delete', '{\"deleted_admin_id\": 3, \"full_name\": \"Ivan Ren M. Villamora\", \"username\": \"ivanrenee\", \"email\": \"villamora.ivanren.manguiat@gmail.com\", \"role\": \"admin\", \"was_first_login\": true}', NULL, 'policy_violation', 'erewrwrefrrdfdregdrtdtete', 'success', NULL, '127.0.0.1', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36', '2026-04-21 07:33:48'),
(22, 1, NULL, NULL, 'admin_restore', '{\"source_audit_id\": 21, \"source_action_type\": \"admin_delete\"}', '{\"restored_action_type\": \"admin_restore\", \"restored_admin_id\": 3, \"restored_admin_email\": \"villamora.ivanren.manguiat@gmail.com\"}', 'restore_from_audit', 'Restored from audit log entry.', 'success', NULL, '127.0.0.1', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-21 07:36:49'),
(23, 1, NULL, NULL, 'login', NULL, NULL, 'admin_login', 'Admin logged in.', 'success', NULL, '127.0.0.1', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-21 07:46:04'),
(24, 1, NULL, NULL, 'concern_restore', '{\"source_audit_id\": 19, \"source_action_type\": \"concern_delete\"}', '{\"restored_action_type\": \"concern_restore\", \"restored_concern_id\": 15}', 'restore_from_audit', 'Restored from audit log entry.', 'success', NULL, '127.0.0.1', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-21 07:46:15'),
(25, 1, 3, NULL, 'admin_update', '{\"username\": \"ivanrenee\", \"email\": \"villamora.ivanren.manguiat@gmail.com\", \"first_name\": \"Ivan\", \"last_name\": \"Villamora\"}', '{\"username\": \"ivanrenee\", \"email\": \"villamora.ivanren.manguiat@gmail.com\", \"first_name\": \"Ivan\", \"last_name\": \"Villamora\"}', 'admin_update', 'Admin villamora.ivanren.manguiat@gmail.com profile updated.', 'success', NULL, '127.0.0.1', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-21 07:53:20'),
(26, 1, 3, NULL, 'admin_update', '{\"username\": \"ivanrenee\", \"email\": \"villamora.ivanren.manguiat@gmail.com\", \"first_name\": \"Ivan\", \"last_name\": \"Villamora\"}', '{\"username\": \"ivanrenee\", \"email\": \"villamora.ivanren.manguiat@gmail.com\", \"first_name\": \"Ivan\", \"last_name\": \"Villamora\"}', 'admin_update', 'Admin villamora.ivanren.manguiat@gmail.com profile updated.', 'success', NULL, '127.0.0.1', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-21 07:54:25'),
(27, 1, 3, NULL, 'admin_update', '{\"username\": \"ivanrenee\", \"email\": \"villamora.ivanren.manguiat@gmail.com\", \"first_name\": \"Ivan\", \"last_name\": \"Villamora\"}', '{\"username\": \"ivanrenee\", \"email\": \"villamora.ivanren.manguiat@gmail.com\", \"first_name\": \"Ivan\", \"last_name\": \"Villamora\"}', 'admin_update', 'Admin villamora.ivanren.manguiat@gmail.com profile updated.', 'success', NULL, '127.0.0.1', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-21 07:58:05'),
(28, 1, NULL, NULL, 'login', NULL, NULL, 'admin_login', 'Admin logged in.', 'success', NULL, '136.158.31.63', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-23 11:29:29'),
(29, 1, NULL, 18, 'concern_update', NULL, '{}', 'concern_update', 'Concern #18 updated.', 'success', NULL, '122.3.102.197', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36', '2026-04-23 11:29:34'),
(30, 1, NULL, NULL, 'device_restore', '{\"source_audit_id\": 17, \"source_action_type\": \"device_delete\"}', '{\"restored_action_type\": \"device_restore\", \"restored_device_serial\": \"SC-136900\"}', 'restore_from_audit', 'Restored from audit log entry.', 'success', NULL, '136.158.31.63', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-23 11:29:44'),
(31, 1, NULL, NULL, 'login', NULL, NULL, 'admin_login', 'Admin logged in.', 'success', NULL, '136.158.31.63', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-23 11:31:31'),
(32, 1, NULL, 19, 'concern_update', NULL, '{}', 'concern_update', 'Concern #19 updated.', 'success', NULL, '136.158.31.63', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-23 11:32:05'),
(33, 3, NULL, NULL, 'login', NULL, NULL, 'failed_login', 'Invalid password attempt.', 'failed', 'Invalid credentials.', '136.158.31.63', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-23 11:32:47'),
(34, 1, NULL, NULL, 'login', NULL, NULL, 'admin_login', 'Admin logged in.', 'success', NULL, '136.158.31.63', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-23 11:32:56'),
(35, 1, NULL, 20, 'concern_delete', NULL, NULL, 'abusive_content', 'dasdasdasd', 'restored', NULL, '112.202.252.101', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36', '2026-04-23 11:33:04'),
(36, 1, NULL, NULL, 'concern_restore', '{\"source_audit_id\": 35, \"source_action_type\": \"concern_delete\"}', '{\"restored_action_type\": \"concern_restore\", \"restored_concern_id\": 20}', 'restore_from_audit', 'Restored from audit log entry.', 'success', NULL, '112.202.252.101', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36', '2026-04-23 11:33:07'),
(37, 1, NULL, 20, 'concern_delete', NULL, NULL, 'spam', 'dfsefsfsfsefsfs', 'restored', NULL, '136.158.31.63', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-23 11:37:32'),
(38, 1, NULL, NULL, 'concern_restore', '{\"source_audit_id\": 37, \"source_action_type\": \"concern_delete\"}', '{\"restored_action_type\": \"concern_restore\", \"restored_concern_id\": 20}', 'restore_from_audit', 'Restored from audit log entry.', 'success', NULL, '136.158.31.63', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-23 11:37:43'),
(39, 1, NULL, 19, 'concern_update', NULL, '{}', 'concern_update', 'Concern #19 updated.', 'success', NULL, '122.3.102.197', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36', '2026-04-23 11:37:44'),
(40, 1, NULL, 20, 'concern_update', NULL, '{}', 'concern_update', 'Concern #20 updated.', 'success', NULL, '136.158.31.63', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-04-23 11:37:51'),
(41, 1, NULL, 20, 'concern_update', NULL, '{}', 'concern_update', 'Concern #20 updated.', 'success', NULL, '122.3.102.197', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36', '2026-04-23 11:37:59'),
(42, 1, NULL, 20, 'concern_update', NULL, '{}', 'concern_update', 'Concern #20 updated.', 'success', NULL, '122.3.102.197', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36', '2026-04-23 11:38:28'),
(43, 1, NULL, 20, 'concern_update', NULL, '{\"status\": \"resolved\"}', 'concern_update', 'Concern #20 updated.', 'success', NULL, '122.3.102.197', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36', '2026-04-23 11:38:35'),
(44, 1, NULL, 20, 'concern_update', NULL, '{}', 'concern_update', 'Concern #20 updated.', 'success', NULL, '122.3.102.197', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36', '2026-04-23 11:38:42');

-- --------------------------------------------------------

--
-- Table structure for table `admin_tbl`
--

CREATE TABLE `admin_tbl` (
  `admin_id` int NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `middle_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) NOT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `province` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `barangay` varchar(100) DEFAULT NULL,
  `street_address` text,
  `role` enum('super_admin','admin') NOT NULL DEFAULT 'admin',
  `is_first_login` tinyint(1) NOT NULL DEFAULT '1',
  `profile_image_url` varchar(500) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `admin_tbl`
--

INSERT INTO `admin_tbl` (`admin_id`, `username`, `email`, `password`, `first_name`, `middle_name`, `last_name`, `contact_number`, `province`, `city`, `barangay`, `street_address`, `role`, `is_first_login`, `profile_image_url`, `created_at`, `updated_at`) VALUES
(1, 'ivanren', 'villamoraivanren@gmail.com', '$2b$12$gIndlBovwtL8G0sHA3dIYO/orPCm/vRXtMuxHJ6HJ6LTrPlOes8sG', 'Ivan Rens', 'Manguiat', 'VIllamora', '09696273011', 'Metro Manila', 'Quezon City', 'Nagkaisang Nayon', '16  Carmencita St.', 'super_admin', 0, NULL, '2026-04-13 14:52:46', '2026-04-21 07:09:54'),
(2, 'rys1', 'ryan.casipe78@gmail.com', '$2b$12$CLMk/.9CYwIfzUsYd0g15u9hy7d7w.b/O8uwrESFyj08IO4.Cshsa', 'Ryanzs', 'Casiple', 'Casipe', '09123456789', 'asdadsa', 'asdasdasd', 'fsdfsdf', 'sadasdasd', 'super_admin', 1, NULL, '2026-04-18 00:33:44', '2026-04-21 07:02:12'),
(3, 'ivanrenee', 'villamora.ivanren.manguiat@gmail.com', '$2b$12$fte4E8BoVQZrjk..kH05.uNQ.Ug2RtxNnf6JH2vyAF9tiJsnRq9ky', 'Ivan', 'Ren M.', 'Villamora', NULL, 'Metro Manila', 'Caloocan City', NULL, 'Pechayan St.', 'admin', 1, NULL, '2026-04-18 00:34:36', '2026-04-21 07:58:05');

-- --------------------------------------------------------

--
-- Table structure for table `device_config_tbl`
--

CREATE TABLE `device_config_tbl` (
  `config_id` int NOT NULL,
  `device_id` int NOT NULL,
  `config_json` json NOT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `device_config_tbl`
--

INSERT INTO `device_config_tbl` (`config_id`, `device_id`, `config_json`, `updated_at`) VALUES
(1, 1, '{\"GPS_TRACKING\": {\"config\": {}, \"enabled\": true}, \"VOICE_ENGINE\": {\"config\": {\"muted\": false, \"volume\": 0.3, \"navigation\": {\"voice\": \"+m3\", \"volume\": 0.3, \"speechSpeed\": 150}, \"speechSpeed\": 150, \"textToSpeech\": {\"voice\": \"+m4\", \"volume\": 0.3, \"speechSpeed\": 150}, \"visualRecognition\": {\"voice\": \"+f5\", \"volume\": 0.3, \"language\": \"tagalog\", \"speechSpeed\": 150}}, \"enabled\": true}, \"EDGE_DETECTION\": {\"config\": {\"stairSafetyDistance\": 300}, \"enabled\": true}, \"FALL_DETECTION\": {\"config\": {\"fallConfirmationDelay\": 3000}, \"enabled\": true}, \"EMERGENCY_SYSTEM\": {\"config\": {\"emergencyTrigger\": 3000, \"emergencyBuzzerPattern\": 100, \"emergencyBuzzerDuration\": 60000}, \"enabled\": true}, \"OBSTACLE_DETECTION\": {\"config\": {\"obstacleFeedbackPattern\": 0, \"obstacleDistanceThreshold\": 300}, \"enabled\": true}, \"VISUAL_RECOGNITION\": {\"config\": {\"recognitionInterval\": 3000}, \"enabled\": true}}', '2026-04-18 01:30:46');

-- --------------------------------------------------------

--
-- Table structure for table `device_guardian_tbl`
--

CREATE TABLE `device_guardian_tbl` (
  `id` int NOT NULL,
  `device_id` int NOT NULL,
  `device_name` varchar(255) DEFAULT NULL,
  `relationship` varchar(100) DEFAULT NULL,
  `is_emergency_contact` tinyint(1) DEFAULT NULL,
  `role` enum('primary','secondary','guardian') NOT NULL,
  `guardian_id` int NOT NULL,
  `assigned_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `device_guardian_tbl`
--

INSERT INTO `device_guardian_tbl` (`id`, `device_id`, `device_name`, `relationship`, `is_emergency_contact`, `role`, `guardian_id`, `assigned_at`) VALUES
(5, 1, NULL, NULL, 1, 'primary', 1, '2026-04-17 02:27:01'),
(6, 2, NULL, NULL, 1, 'primary', 1, '2026-04-17 02:29:32'),
(7, 3, NULL, NULL, 1, 'primary', 1, '2026-04-17 03:22:54');

-- --------------------------------------------------------

--
-- Table structure for table `device_last_location_tbl`
--

CREATE TABLE `device_last_location_tbl` (
  `device_id` int NOT NULL,
  `lat` decimal(10,7) DEFAULT NULL,
  `lng` decimal(10,7) DEFAULT NULL,
  `sats` int DEFAULT NULL,
  `fix_status` smallint NOT NULL,
  `hdop` decimal(6,2) DEFAULT NULL,
  `gps_status` int NOT NULL,
  `recorded_at` datetime NOT NULL,
  `updated_at` timestamp NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `device_last_location_tbl`
--

INSERT INTO `device_last_location_tbl` (`device_id`, `lat`, `lng`, `sats`, `fix_status`, `hdop`, `gps_status`, `recorded_at`, `updated_at`) VALUES
(1, 14.7007428, 121.0495198, 12, 1, 0.80, 2, '2026-04-17 07:22:20', '2026-04-17 07:22:20');

-- --------------------------------------------------------

--
-- Table structure for table `device_logs_tbl`
--

CREATE TABLE `device_logs_tbl` (
  `log_id` int NOT NULL,
  `device_id` int NOT NULL,
  `guardian_id` int DEFAULT NULL,
  `activity_type` varchar(50) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `message` text NOT NULL,
  `metadata_json` json DEFAULT NULL,
  `created_at` timestamp NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `device_logs_tbl`
--

INSERT INTO `device_logs_tbl` (`log_id`, `device_id`, `guardian_id`, `activity_type`, `status`, `message`, `metadata_json`, `created_at`) VALUES
(1, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 1, 2026, 2:43 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 236473}', '2026-04-01 02:43:34'),
(2, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 6, 2026, 3:37 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 231805}', '2026-04-06 03:37:26'),
(3, 1, 1, 'route', 'active', 'Route started to selected destination', '{\"serial\": \"SC-136901\", \"status\": \"active\", \"routeId\": 1, \"deviceId\": 1, \"clearedAt\": null, \"updatedAt\": \"2026-04-13T10:31:24.000Z\", \"durationMs\": 154585, \"guardianId\": 1, \"completedAt\": null, \"destination\": {\"lat\": 14.701652, \"lng\": 121.048386, \"label\": null}, \"requestedAt\": \"2026-04-13T10:31:23.000Z\", \"routeGeoJson\": {\"type\": \"LineString\", \"coordinates\": [[121.049591, 14.700765], [121.048903, 14.70055], [121.048761, 14.701114], [121.048721, 14.701198], [121.048673, 14.701272], [121.048386, 14.701652]]}, \"distanceMeters\": 214.7, \"providerPayload\": {\"info\": {\"took\": 301, \"copyrights\": [\"GraphHopper\", \"OpenStreetMap contributors\"], \"road_data_timestamp\": \"2025-09-18T00:00:00Z\"}, \"hints\": {\"visited_nodes.sum\": 26, \"visited_nodes.average\": 26}, \"paths\": [{\"bbox\": [121.048386, 14.70055, 121.049591, 14.701652], \"legs\": [], \"time\": 154585, \"ascend\": 0, \"points\": {\"type\": \"LineString\", \"coordinates\": [[121.049591, 14.700765], [121.048903, 14.70055], [121.048761, 14.701114], [121.048721, 14.701198], [121.048673, 14.701272], [121.048386, 14.701652]]}, \"weight\": 135.200572, \"descend\": 0, \"details\": {}, \"distance\": 214.701, \"transfers\": 0, \"instructions\": [{\"sign\": 0, \"text\": \"Continue onto La Verna Street\", \"time\": 56049, \"heading\": 252.08, \"distance\": 77.846, \"interval\": [0, 1], \"street_name\": \"La Verna Street\"}, {\"sign\": 2, \"text\": \"Turn right onto Percincula Street\", \"time\": 98536, \"distance\": 136.855, \"interval\": [1, 5], \"street_name\": \"Percincula Street\"}, {\"sign\": 4, \"text\": \"Arrive at destination\", \"time\": 0, \"distance\": 0, \"interval\": [5, 5], \"street_name\": \"\", \"last_heading\": 325.0504163336186}], \"points_encoded\": false, \"snapped_waypoints\": {\"type\": \"LineString\", \"coordinates\": [[121.049591, 14.700765], [121.048386, 14.701652]]}}]}}', '2026-04-13 10:31:24'),
(4, 1, 1, 'route', 'cleared', 'Route was cleared', '{\"serial\": \"SC-136901\", \"status\": \"cleared\", \"routeId\": 1, \"deviceId\": 1, \"clearedAt\": \"2026-04-13T10:31:48.000Z\", \"updatedAt\": \"2026-04-13T10:31:48.000Z\", \"durationMs\": 154585, \"guardianId\": 1, \"completedAt\": null, \"destination\": {\"lat\": 14.701652, \"lng\": 121.048386, \"label\": null}, \"requestedAt\": \"2026-04-13T10:31:23.000Z\", \"routeGeoJson\": {\"type\": \"LineString\", \"coordinates\": [[121.049591, 14.700765], [121.048903, 14.70055], [121.048761, 14.701114], [121.048721, 14.701198], [121.048673, 14.701272], [121.048386, 14.701652]]}, \"distanceMeters\": 214.7, \"providerPayload\": {\"info\": {\"took\": 301, \"copyrights\": [\"GraphHopper\", \"OpenStreetMap contributors\"], \"road_data_timestamp\": \"2025-09-18T00:00:00Z\"}, \"hints\": {\"visited_nodes.sum\": 26, \"visited_nodes.average\": 26}, \"paths\": [{\"bbox\": [121.048386, 14.70055, 121.049591, 14.701652], \"legs\": [], \"time\": 154585, \"ascend\": 0, \"points\": {\"type\": \"LineString\", \"coordinates\": [[121.049591, 14.700765], [121.048903, 14.70055], [121.048761, 14.701114], [121.048721, 14.701198], [121.048673, 14.701272], [121.048386, 14.701652]]}, \"weight\": 135.200572, \"descend\": 0, \"details\": {}, \"distance\": 214.701, \"transfers\": 0, \"instructions\": [{\"sign\": 0, \"text\": \"Continue onto La Verna Street\", \"time\": 56049, \"heading\": 252.08, \"distance\": 77.846, \"interval\": [0, 1], \"street_name\": \"La Verna Street\"}, {\"sign\": 2, \"text\": \"Turn right onto Percincula Street\", \"time\": 98536, \"distance\": 136.855, \"interval\": [1, 5], \"street_name\": \"Percincula Street\"}, {\"sign\": 4, \"text\": \"Arrive at destination\", \"time\": 0, \"distance\": 0, \"interval\": [5, 5], \"street_name\": \"\", \"last_heading\": 325.0504163336186}], \"points_encoded\": false, \"snapped_waypoints\": {\"type\": \"LineString\", \"coordinates\": [[121.049591, 14.700765], [121.048386, 14.701652]]}}]}}', '2026-04-13 10:31:48'),
(5, 1, 1, 'route', 'active', 'Route started to selected destination', '{\"serial\": \"SC-136901\", \"status\": \"active\", \"routeId\": 3, \"deviceId\": 1, \"clearedAt\": null, \"updatedAt\": \"2026-04-13T10:31:54.000Z\", \"durationMs\": 126742, \"guardianId\": 1, \"completedAt\": null, \"destination\": {\"lat\": 14.701783, \"lng\": 121.048699, \"label\": null}, \"requestedAt\": \"2026-04-13T10:31:54.000Z\", \"routeGeoJson\": {\"type\": \"LineString\", \"coordinates\": [[121.049418, 14.700711], [121.049373, 14.700697], [121.049237, 14.701203], [121.049229, 14.701252], [121.049231, 14.701303], [121.049248, 14.701362], [121.049323, 14.701556], [121.048699, 14.701783]]}, \"distanceMeters\": 176.03, \"providerPayload\": {\"info\": {\"took\": 18, \"copyrights\": [\"GraphHopper\", \"OpenStreetMap contributors\"], \"road_data_timestamp\": \"2025-09-18T00:00:00Z\"}, \"hints\": {\"visited_nodes.sum\": 22, \"visited_nodes.average\": 22}, \"paths\": [{\"bbox\": [121.048699, 14.700697, 121.049418, 14.701783], \"legs\": [], \"time\": 126742, \"ascend\": 0, \"points\": {\"type\": \"LineString\", \"coordinates\": [[121.049418, 14.700711], [121.049373, 14.700697], [121.049237, 14.701203], [121.049229, 14.701252], [121.049231, 14.701303], [121.049248, 14.701362], [121.049323, 14.701556], [121.048699, 14.701783]]}, \"weight\": 126.131288, \"descend\": 0, \"details\": {}, \"distance\": 176.03, \"transfers\": 0, \"instructions\": [{\"sign\": 0, \"text\": \"Continue onto La Verna Street\", \"time\": 3660, \"heading\": 252.08, \"distance\": 5.083, \"interval\": [0, 1], \"street_name\": \"La Verna Street\"}, {\"sign\": 2, \"text\": \"Turn right onto Perugia Street\", \"time\": 71438, \"distance\": 99.219, \"interval\": [1, 6], \"street_name\": \"Perugia Street\"}, {\"sign\": -2, \"text\": \"Turn left onto Assisi Street\", \"time\": 51644, \"distance\": 71.727, \"interval\": [6, 7], \"street_name\": \"Assisi Street\"}, {\"sign\": 4, \"text\": \"Arrive at destination\", \"time\": 0, \"distance\": 0, \"interval\": [7, 7], \"street_name\": \"\", \"last_heading\": 290.60419369035355}], \"points_encoded\": false, \"snapped_waypoints\": {\"type\": \"LineString\", \"coordinates\": [[121.049418, 14.700711], [121.048699, 14.701783]]}}]}}', '2026-04-13 10:31:54'),
(6, 1, 1, 'route', 'cleared', 'Route was cleared', '{\"serial\": \"SC-136901\", \"status\": \"cleared\", \"routeId\": 3, \"deviceId\": 1, \"clearedAt\": \"2026-04-13T10:32:10.000Z\", \"updatedAt\": \"2026-04-13T10:32:10.000Z\", \"durationMs\": 126742, \"guardianId\": 1, \"completedAt\": null, \"destination\": {\"lat\": 14.701783, \"lng\": 121.048699, \"label\": null}, \"requestedAt\": \"2026-04-13T10:31:54.000Z\", \"routeGeoJson\": {\"type\": \"LineString\", \"coordinates\": [[121.049418, 14.700711], [121.049373, 14.700697], [121.049237, 14.701203], [121.049229, 14.701252], [121.049231, 14.701303], [121.049248, 14.701362], [121.049323, 14.701556], [121.048699, 14.701783]]}, \"distanceMeters\": 176.03, \"providerPayload\": {\"info\": {\"took\": 18, \"copyrights\": [\"GraphHopper\", \"OpenStreetMap contributors\"], \"road_data_timestamp\": \"2025-09-18T00:00:00Z\"}, \"hints\": {\"visited_nodes.sum\": 22, \"visited_nodes.average\": 22}, \"paths\": [{\"bbox\": [121.048699, 14.700697, 121.049418, 14.701783], \"legs\": [], \"time\": 126742, \"ascend\": 0, \"points\": {\"type\": \"LineString\", \"coordinates\": [[121.049418, 14.700711], [121.049373, 14.700697], [121.049237, 14.701203], [121.049229, 14.701252], [121.049231, 14.701303], [121.049248, 14.701362], [121.049323, 14.701556], [121.048699, 14.701783]]}, \"weight\": 126.131288, \"descend\": 0, \"details\": {}, \"distance\": 176.03, \"transfers\": 0, \"instructions\": [{\"sign\": 0, \"text\": \"Continue onto La Verna Street\", \"time\": 3660, \"heading\": 252.08, \"distance\": 5.083, \"interval\": [0, 1], \"street_name\": \"La Verna Street\"}, {\"sign\": 2, \"text\": \"Turn right onto Perugia Street\", \"time\": 71438, \"distance\": 99.219, \"interval\": [1, 6], \"street_name\": \"Perugia Street\"}, {\"sign\": -2, \"text\": \"Turn left onto Assisi Street\", \"time\": 51644, \"distance\": 71.727, \"interval\": [6, 7], \"street_name\": \"Assisi Street\"}, {\"sign\": 4, \"text\": \"Arrive at destination\", \"time\": 0, \"distance\": 0, \"interval\": [7, 7], \"street_name\": \"\", \"last_heading\": 290.60419369035355}], \"points_encoded\": false, \"snapped_waypoints\": {\"type\": \"LineString\", \"coordinates\": [[121.049418, 14.700711], [121.048699, 14.701783]]}}]}}', '2026-04-13 10:32:10'),
(7, 1, 1, 'route', 'active', 'Route started to selected destination', '{\"serial\": \"SC-136901\", \"status\": \"active\", \"routeId\": 5, \"deviceId\": 1, \"clearedAt\": null, \"updatedAt\": \"2026-04-13T10:32:20.000Z\", \"durationMs\": 106285, \"guardianId\": 1, \"completedAt\": null, \"destination\": {\"lat\": 14.701733, \"lng\": 121.048837, \"label\": null}, \"requestedAt\": \"2026-04-13T10:32:20.000Z\", \"routeGeoJson\": {\"type\": \"LineString\", \"coordinates\": [[121.049355, 14.700762], [121.049237, 14.701203], [121.049229, 14.701252], [121.049231, 14.701303], [121.049248, 14.701362], [121.049323, 14.701556], [121.048837, 14.701733]]}, \"distanceMeters\": 147.62, \"providerPayload\": {\"info\": {\"took\": 16, \"copyrights\": [\"GraphHopper\", \"OpenStreetMap contributors\"], \"road_data_timestamp\": \"2025-09-18T00:00:00Z\"}, \"hints\": {\"visited_nodes.sum\": 18, \"visited_nodes.average\": 18}, \"paths\": [{\"bbox\": [121.048837, 14.700762, 121.049355, 14.701733], \"legs\": [], \"time\": 106285, \"ascend\": 0, \"points\": {\"type\": \"LineString\", \"coordinates\": [[121.049355, 14.700762], [121.049237, 14.701203], [121.049229, 14.701252], [121.049231, 14.701303], [121.049248, 14.701362], [121.049323, 14.701556], [121.048837, 14.701733]]}, \"weight\": 106.285415, \"descend\": 0, \"details\": {}, \"distance\": 147.619, \"transfers\": 0, \"instructions\": [{\"sign\": 0, \"text\": \"Continue onto Perugia Street\", \"time\": 66019, \"heading\": 345.4, \"distance\": 91.693, \"interval\": [0, 5], \"street_name\": \"Perugia Street\"}, {\"sign\": -2, \"text\": \"Turn left onto Assisi Street\", \"time\": 40266, \"distance\": 55.925, \"interval\": [5, 6], \"street_name\": \"Assisi Street\"}, {\"sign\": 4, \"text\": \"Arrive at destination\", \"time\": 0, \"distance\": 0, \"interval\": [6, 6], \"street_name\": \"\", \"last_heading\": 290.60419369035355}], \"points_encoded\": false, \"snapped_waypoints\": {\"type\": \"LineString\", \"coordinates\": [[121.049355, 14.700762], [121.048837, 14.701733]]}}]}}', '2026-04-13 10:32:20'),
(8, 1, 1, 'route', 'cleared', 'Route was cleared', '{\"serial\": \"SC-136901\", \"status\": \"cleared\", \"routeId\": 5, \"deviceId\": 1, \"clearedAt\": \"2026-04-13T10:32:29.000Z\", \"updatedAt\": \"2026-04-13T10:32:29.000Z\", \"durationMs\": 106285, \"guardianId\": 1, \"completedAt\": null, \"destination\": {\"lat\": 14.701733, \"lng\": 121.048837, \"label\": null}, \"requestedAt\": \"2026-04-13T10:32:20.000Z\", \"routeGeoJson\": {\"type\": \"LineString\", \"coordinates\": [[121.049355, 14.700762], [121.049237, 14.701203], [121.049229, 14.701252], [121.049231, 14.701303], [121.049248, 14.701362], [121.049323, 14.701556], [121.048837, 14.701733]]}, \"distanceMeters\": 147.62, \"providerPayload\": {\"info\": {\"took\": 16, \"copyrights\": [\"GraphHopper\", \"OpenStreetMap contributors\"], \"road_data_timestamp\": \"2025-09-18T00:00:00Z\"}, \"hints\": {\"visited_nodes.sum\": 18, \"visited_nodes.average\": 18}, \"paths\": [{\"bbox\": [121.048837, 14.700762, 121.049355, 14.701733], \"legs\": [], \"time\": 106285, \"ascend\": 0, \"points\": {\"type\": \"LineString\", \"coordinates\": [[121.049355, 14.700762], [121.049237, 14.701203], [121.049229, 14.701252], [121.049231, 14.701303], [121.049248, 14.701362], [121.049323, 14.701556], [121.048837, 14.701733]]}, \"weight\": 106.285415, \"descend\": 0, \"details\": {}, \"distance\": 147.619, \"transfers\": 0, \"instructions\": [{\"sign\": 0, \"text\": \"Continue onto Perugia Street\", \"time\": 66019, \"heading\": 345.4, \"distance\": 91.693, \"interval\": [0, 5], \"street_name\": \"Perugia Street\"}, {\"sign\": -2, \"text\": \"Turn left onto Assisi Street\", \"time\": 40266, \"distance\": 55.925, \"interval\": [5, 6], \"street_name\": \"Assisi Street\"}, {\"sign\": 4, \"text\": \"Arrive at destination\", \"time\": 0, \"distance\": 0, \"interval\": [6, 6], \"street_name\": \"\", \"last_heading\": 290.60419369035355}], \"points_encoded\": false, \"snapped_waypoints\": {\"type\": \"LineString\", \"coordinates\": [[121.049355, 14.700762], [121.048837, 14.701733]]}}]}}', '2026-04-13 10:32:29'),
(9, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 16, 2026, 9:43 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 148384}', '2026-04-16 09:43:59'),
(10, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 16, 2026, 9:46 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 285620}', '2026-04-16 09:46:16'),
(11, 1, NULL, 'fall', 'triggered', 'Last location: Location unavailable\n Apr 16, 2026, 9:51 AM', '{\"source\": \"mpu6050\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 116834}', '2026-04-16 09:51:58'),
(12, 1, NULL, 'fall', 'triggered', 'Last location: Location unavailable\n Apr 16, 2026, 9:52 AM', '{\"source\": \"mpu6050\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 119984}', '2026-04-16 09:52:01'),
(13, 1, NULL, 'fall', 'triggered', 'Last location: Location unavailable\n Apr 16, 2026, 9:52 AM', '{\"source\": \"mpu6050\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 123153}', '2026-04-16 09:52:04'),
(14, 1, NULL, 'fall', 'triggered', 'Last location: Location unavailable\n Apr 16, 2026, 9:54 AM', '{\"source\": \"mpu6050\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 132848}', '2026-04-16 09:54:26'),
(15, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 16, 2026, 11:04 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 245851}', '2026-04-16 11:04:39'),
(16, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 16, 2026, 11:06 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 348195}', '2026-04-16 11:06:22'),
(17, 1, NULL, 'fall', 'triggered', 'Last location: Location unavailable\n Apr 16, 2026, 11:06 AM', '{\"source\": \"mpu6050\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 360578}', '2026-04-16 11:06:34'),
(18, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 16, 2026, 11:30 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 1802759}', '2026-04-16 11:30:37'),
(19, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 16, 2026, 11:30 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 1815641}', '2026-04-16 11:30:50'),
(20, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 16, 2026, 11:31 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 1836132}', '2026-04-16 11:31:10'),
(21, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 16, 2026, 11:32 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 1893436}', '2026-04-16 11:32:07'),
(22, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 16, 2026, 11:32 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 1921917}', '2026-04-16 11:32:36'),
(23, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 17, 2026, 2:40 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 86192}', '2026-04-17 02:40:31'),
(24, 1, NULL, 'emergency', 'triggered', 'Last location: 14.7226984, 121.0332273\n Apr 17, 2026, 2:42 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.7226984, \"lng\": 121.0332273, \"label\": null}, \"timestamp\": 185452}', '2026-04-17 02:42:10'),
(25, 1, NULL, 'emergency', 'triggered', 'Last location: 14.7226984, 121.0332273\n Apr 17, 2026, 2:44 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.7226984, \"lng\": 121.0332273, \"label\": null}, \"timestamp\": 351601}', '2026-04-17 02:44:57'),
(26, 1, NULL, 'emergency', 'triggered', 'Last location: 14.7226984, 121.0332273\n Apr 17, 2026, 2:45 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.7226984, \"lng\": 121.0332273, \"label\": null}, \"timestamp\": 367664}', '2026-04-17 02:45:12'),
(27, 1, NULL, 'emergency', 'triggered', 'Last location: Carmencita Road, Josefinal Village, Nagkaisang Nayon, Quezon City\n Apr 17, 2026, 7:21 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.722713, \"lng\": 121.0332053, \"label\": \"Carmencita Road, Josefinal Village, Nagkaisang Nayon, Quezon City\"}, \"timestamp\": 110643}', '2026-04-17 07:21:53'),
(28, 1, 1, 'route', 'active', 'Route started to selected destination', '{\"serial\": \"SC-136901\", \"status\": \"active\", \"routeId\": 7, \"deviceId\": 1, \"clearedAt\": null, \"updatedAt\": \"2026-04-17T07:22:11.000Z\", \"durationMs\": 131844, \"guardianId\": 1, \"completedAt\": null, \"destination\": {\"lat\": 14.701744, \"lng\": 121.048808, \"label\": null}, \"requestedAt\": \"2026-04-17T07:22:09.000Z\", \"routeGeoJson\": {\"type\": \"LineString\", \"coordinates\": [[121.049591, 14.700765], [121.049373, 14.700697], [121.049237, 14.701203], [121.049229, 14.701252], [121.049231, 14.701303], [121.049248, 14.701362], [121.049323, 14.701556], [121.048808, 14.701744]]}, \"distanceMeters\": 183.12, \"providerPayload\": {\"info\": {\"took\": 500, \"copyrights\": [\"GraphHopper\", \"OpenStreetMap contributors\"], \"road_data_timestamp\": \"2025-09-18T00:00:00Z\"}, \"hints\": {\"visited_nodes.sum\": 18, \"visited_nodes.average\": 18}, \"paths\": [{\"bbox\": [121.048808, 14.700697, 121.049591, 14.701744], \"legs\": [], \"time\": 131844, \"ascend\": 0, \"points\": {\"type\": \"LineString\", \"coordinates\": [[121.049591, 14.700765], [121.049373, 14.700697], [121.049237, 14.701203], [121.049229, 14.701252], [121.049231, 14.701303], [121.049248, 14.701362], [121.049323, 14.701556], [121.048808, 14.701744]]}, \"weight\": 128.882368, \"descend\": 0, \"details\": {}, \"distance\": 183.117, \"transfers\": 0, \"instructions\": [{\"sign\": 0, \"text\": \"Continue onto La Verna Street\", \"time\": 17770, \"heading\": 252.08, \"distance\": 24.681, \"interval\": [0, 1], \"street_name\": \"La Verna Street\"}, {\"sign\": 2, \"text\": \"Turn right onto Perugia Street\", \"time\": 71438, \"distance\": 99.219, \"interval\": [1, 6], \"street_name\": \"Perugia Street\"}, {\"sign\": -2, \"text\": \"Turn left onto Assisi Street\", \"time\": 42636, \"distance\": 59.217, \"interval\": [6, 7], \"street_name\": \"Assisi Street\"}, {\"sign\": 4, \"text\": \"Arrive at destination\", \"time\": 0, \"distance\": 0, \"interval\": [7, 7], \"street_name\": \"\", \"last_heading\": 290.60419369035355}], \"points_encoded\": false, \"snapped_waypoints\": {\"type\": \"LineString\", \"coordinates\": [[121.049591, 14.700765], [121.048808, 14.701744]]}}]}}', '2026-04-17 07:22:11'),
(29, 1, 1, 'route', 'cleared', 'Route was cleared', '{\"serial\": \"SC-136901\", \"status\": \"cleared\", \"routeId\": 7, \"deviceId\": 1, \"clearedAt\": \"2026-04-17T07:22:29.000Z\", \"updatedAt\": \"2026-04-17T07:22:29.000Z\", \"durationMs\": 131844, \"guardianId\": 1, \"completedAt\": null, \"destination\": {\"lat\": 14.701744, \"lng\": 121.048808, \"label\": null}, \"requestedAt\": \"2026-04-17T07:22:09.000Z\", \"routeGeoJson\": {\"type\": \"LineString\", \"coordinates\": [[121.049591, 14.700765], [121.049373, 14.700697], [121.049237, 14.701203], [121.049229, 14.701252], [121.049231, 14.701303], [121.049248, 14.701362], [121.049323, 14.701556], [121.048808, 14.701744]]}, \"distanceMeters\": 183.12, \"providerPayload\": {\"info\": {\"took\": 500, \"copyrights\": [\"GraphHopper\", \"OpenStreetMap contributors\"], \"road_data_timestamp\": \"2025-09-18T00:00:00Z\"}, \"hints\": {\"visited_nodes.sum\": 18, \"visited_nodes.average\": 18}, \"paths\": [{\"bbox\": [121.048808, 14.700697, 121.049591, 14.701744], \"legs\": [], \"time\": 131844, \"ascend\": 0, \"points\": {\"type\": \"LineString\", \"coordinates\": [[121.049591, 14.700765], [121.049373, 14.700697], [121.049237, 14.701203], [121.049229, 14.701252], [121.049231, 14.701303], [121.049248, 14.701362], [121.049323, 14.701556], [121.048808, 14.701744]]}, \"weight\": 128.882368, \"descend\": 0, \"details\": {}, \"distance\": 183.117, \"transfers\": 0, \"instructions\": [{\"sign\": 0, \"text\": \"Continue onto La Verna Street\", \"time\": 17770, \"heading\": 252.08, \"distance\": 24.681, \"interval\": [0, 1], \"street_name\": \"La Verna Street\"}, {\"sign\": 2, \"text\": \"Turn right onto Perugia Street\", \"time\": 71438, \"distance\": 99.219, \"interval\": [1, 6], \"street_name\": \"Perugia Street\"}, {\"sign\": -2, \"text\": \"Turn left onto Assisi Street\", \"time\": 42636, \"distance\": 59.217, \"interval\": [6, 7], \"street_name\": \"Assisi Street\"}, {\"sign\": 4, \"text\": \"Arrive at destination\", \"time\": 0, \"distance\": 0, \"interval\": [7, 7], \"street_name\": \"\", \"last_heading\": 290.60419369035355}], \"points_encoded\": false, \"snapped_waypoints\": {\"type\": \"LineString\", \"coordinates\": [[121.049591, 14.700765], [121.048808, 14.701744]]}}]}}', '2026-04-17 07:22:29'),
(30, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:23 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 194583}', '2026-04-17 07:23:17'),
(31, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:23 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 226690}', '2026-04-17 07:23:50'),
(32, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:24 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 237111}', '2026-04-17 07:24:00'),
(33, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:24 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 292909}', '2026-04-17 07:24:56'),
(34, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:26 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 361011}', '2026-04-17 07:26:04'),
(35, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:26 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 376362}', '2026-04-17 07:26:19'),
(36, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:26 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 394949}', '2026-04-17 07:26:38'),
(37, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:26 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 410417}', '2026-04-17 07:26:53'),
(38, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:27 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 420808}', '2026-04-17 07:27:04'),
(39, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:27 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 442914}', '2026-04-17 07:27:26'),
(40, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:27 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 456771}', '2026-04-17 07:27:39'),
(41, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:27 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 466247}', '2026-04-17 07:27:49'),
(42, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:32 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 750599}', '2026-04-17 07:32:34'),
(43, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:33 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 790210}', '2026-04-17 07:33:13'),
(44, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:33 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 797243}', '2026-04-17 07:33:20'),
(45, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:33 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 809020}', '2026-04-17 07:33:32'),
(46, 1, NULL, 'fall', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:35 AM', '{\"source\": \"mpu6050\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 926123}', '2026-04-17 07:35:29'),
(47, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:37 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 1024273}', '2026-04-17 07:37:07'),
(48, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:37 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 1040321}', '2026-04-17 07:37:23'),
(49, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:37 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 1063728}', '2026-04-17 07:37:47'),
(50, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:38 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 1080134}', '2026-04-17 07:38:03'),
(51, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:38 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 1085452}', '2026-04-17 07:38:08'),
(52, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:39 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 1155741}', '2026-04-17 07:39:19'),
(53, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:39 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 1186841}', '2026-04-17 07:39:50'),
(54, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:40 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 1200628}', '2026-04-17 07:40:04'),
(55, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:40 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 1221757}', '2026-04-17 07:40:25'),
(56, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:40 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 1234503}', '2026-04-17 07:40:37'),
(57, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:40 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 1247376}', '2026-04-17 07:40:50'),
(58, 1, NULL, 'emergency', 'triggered', 'Last location: La Verna Street, Saint Francis Village, Sauyo, Quezon City\n Apr 17, 2026, 7:41 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": 14.700776129832676, \"lng\": 121.04958758689465, \"label\": \"La Verna Street, Saint Francis Village, Sauyo, Quezon City\"}, \"timestamp\": 1266675}', '2026-04-17 07:41:09'),
(59, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 18, 2026, 1:29 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 78338}', '2026-04-18 01:29:17'),
(60, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 18, 2026, 1:30 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 127553}', '2026-04-18 01:30:06'),
(61, 1, NULL, 'emergency', 'triggered', 'Last location: Location unavailable\n Apr 21, 2026, 5:29 AM', '{\"source\": \"sos_button\", \"location\": {\"lat\": null, \"lng\": null, \"label\": null}, \"timestamp\": 101394}', '2026-04-21 05:29:53');

-- --------------------------------------------------------

--
-- Table structure for table `device_route_tbl`
--

CREATE TABLE `device_route_tbl` (
  `route_id` int NOT NULL,
  `device_id` int NOT NULL,
  `guardian_id` int DEFAULT NULL,
  `destination_label` varchar(255) DEFAULT NULL,
  `destination_lat` decimal(10,7) NOT NULL,
  `destination_lng` decimal(10,7) NOT NULL,
  `route_geojson` json DEFAULT NULL,
  `provider_payload` json DEFAULT NULL,
  `status` enum('pending','active','completed','cleared','failed') NOT NULL,
  `distance_meters` decimal(12,2) DEFAULT NULL,
  `duration_ms` bigint DEFAULT NULL,
  `requested_at` timestamp NOT NULL,
  `completed_at` timestamp NULL DEFAULT NULL,
  `cleared_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `device_tbl`
--

CREATE TABLE `device_tbl` (
  `device_id` int NOT NULL,
  `vip_id` int DEFAULT NULL,
  `device_serial_number` varchar(100) NOT NULL,
  `is_paired` tinyint(1) DEFAULT NULL,
  `paired_at` timestamp NULL DEFAULT NULL,
  `last_active_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `device_tbl`
--

INSERT INTO `device_tbl` (`device_id`, `vip_id`, `device_serial_number`, `is_paired`, `paired_at`, `last_active_at`, `created_at`, `updated_at`) VALUES
(1, 3, 'SC-136901', 1, '2026-04-17 02:27:01', NULL, '2026-03-27 04:39:25', '2026-04-17 23:54:04'),
(2, NULL, 'SC-136902', 1, '2026-04-17 02:29:32', NULL, '2026-03-27 04:39:25', '2026-04-17 02:29:32'),
(3, NULL, 'SC-136903', 1, '2026-04-17 03:22:54', NULL, '2026-03-27 04:39:25', '2026-04-17 03:22:54'),
(4, NULL, 'SC-136904', 0, NULL, NULL, '2026-03-27 04:39:25', '2026-03-27 04:39:25'),
(5, NULL, 'SC-136900121', 0, NULL, NULL, '2026-03-27 04:39:25', '2026-04-21 07:23:44'),
(7, NULL, 'SC-136900', 0, NULL, NULL, '2026-04-23 11:29:44', '2026-04-23 11:29:44');

-- --------------------------------------------------------

--
-- Table structure for table `guardian_concerns_tbl`
--

CREATE TABLE `guardian_concerns_tbl` (
  `concern_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `status` enum('unread','read','resolved') NOT NULL DEFAULT 'unread',
  `admin_reply` text,
  `replied_by_admin_id` int DEFAULT NULL,
  `replied_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `deleted_at` timestamp NULL DEFAULT NULL,
  `deleted_by_admin_id` int DEFAULT NULL,
  `deleted_reason_code` varchar(50) DEFAULT NULL,
  `deleted_reason_text` varchar(500) DEFAULT NULL,
  `process_stage` varchar(50) NOT NULL DEFAULT 'new',
  `resolution_remarks` text,
  `process_updated_by_admin_id` int DEFAULT NULL,
  `process_updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `guardian_concerns_tbl`
--

INSERT INTO `guardian_concerns_tbl` (`concern_id`, `name`, `email`, `message`, `status`, `admin_reply`, `replied_by_admin_id`, `replied_at`, `created_at`, `updated_at`, `is_deleted`, `deleted_at`, `deleted_by_admin_id`, `deleted_reason_code`, `deleted_reason_text`, `process_stage`, `resolution_remarks`, `process_updated_by_admin_id`, `process_updated_at`) VALUES
(14, 'rys', 'nyar.cas89@gmail.com', '[Source: guest-landing]\n\nasdasdasd', 'unread', NULL, NULL, NULL, '2026-04-21 07:13:10', '2026-04-21 07:18:32', 0, NULL, NULL, NULL, NULL, 'new', NULL, NULL, NULL),
(15, 'ivanren', 'villamora.ivanren.manguiat@gmail.com', '[Source: guardian-dashboard]\n\nhello', 'unread', NULL, NULL, NULL, '2026-04-21 07:14:56', '2026-04-21 07:46:15', 0, NULL, NULL, NULL, NULL, 'new', NULL, NULL, NULL),
(17, 'ivanren', 'villamora.ivanren.manguiat@gmail.com', '[Source: guardian-dashboard]\n\nconcern a', 'read', NULL, NULL, NULL, '2026-04-21 05:27:03', '2026-04-21 07:31:44', 1, '2026-04-21 07:31:44', 1, NULL, NULL, 'new', NULL, NULL, NULL),
(18, 'rys', 'ryan.casipe78@gmail.com', '[Source: guest-landing]\n\nasdasdasdafasd', 'unread', NULL, NULL, NULL, '2026-04-23 11:26:52', '2026-04-23 11:26:52', 0, NULL, NULL, NULL, NULL, 'new', NULL, NULL, NULL),
(19, 'Villamora, Ivan Ren M.', 'icane2026@gmail.com', '[Source: guest-landing]\n\nI have a concern', 'unread', NULL, NULL, NULL, '2026-04-23 11:31:21', '2026-04-23 11:31:21', 0, NULL, NULL, NULL, NULL, 'new', NULL, NULL, NULL),
(20, 'asdasdasd', 'jake.cyrus89@gmail.com', '[Source: guest-landing]\n\nasasdasdsad', 'resolved', NULL, NULL, NULL, '2026-04-23 11:32:44', '2026-04-23 11:38:35', 0, NULL, NULL, NULL, NULL, 'new', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `guardian_invitations`
--

CREATE TABLE `guardian_invitations` (
  `id` int NOT NULL,
  `token` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `device_id` int NOT NULL,
  `invited_by_guardian_id` int NOT NULL,
  `status` enum('pending','accepted','expired','revoked') NOT NULL,
  `expires_at` datetime NOT NULL,
  `accepted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `guardian_invitations`
--

INSERT INTO `guardian_invitations` (`id`, `token`, `email`, `device_id`, `invited_by_guardian_id`, `status`, `expires_at`, `accepted_at`) VALUES
(1, '.eJwlykEKgCAQBdC7zFqEtq66iUwzU31QA1MhortHtH7vJsuMRIF4rRD2slecDcW8Wkq98bx9wcuRyZHagFiEUpgcoQw007hccetcFVx-el5fmB9F.aeCWfw.RfVAAB2iHc6ovR0kWZ-5ePDsqB4', 'africa.christine.delluta@gmail.com', 1, 1, 'pending', '2026-04-17 07:57:52', NULL),
(2, 'eyJlbWFpbCI6ImNocmlzdGluZWRlbGx1dGFAZ21haWwuY29tIiwiZGV2aWNlX2lkIjoxLCJpbnZpdGVkX2J5X2d1YXJkaWFuX2lkIjoxfQ.aeCXIw.8FYEq9GZoqddB_hb-3NBzhZ8IAI', 'christinedelluta@gmail.com', 1, 1, 'accepted', '2026-04-17 08:00:36', '2026-04-16 08:02:23'),
(3, '.eJwdykEKgCAQBdC7zFqEaOeqm8ikg3xwRhAVIrp71Pq9m0QZlQIt1MraOnssti7mla1M8DjKV3xqSo6yLCSJyBQ2R7CFITmeVyyTewbbT_vzArEYID0.aeDBmA.QdKYdOSiiU6MNO5rFh6IeWYupc8', 'villamora.ivanren.manguiat@gmail.com', 1, 3, 'accepted', '2026-04-17 11:01:44', '2026-04-16 11:02:10');

-- --------------------------------------------------------

--
-- Table structure for table `guardian_settings_tbl`
--

CREATE TABLE `guardian_settings_tbl` (
  `settings_id` int NOT NULL,
  `guardian_id` int NOT NULL,
  `allow_location` tinyint(1) NOT NULL DEFAULT '1',
  `push_notifications` tinyint(1) NOT NULL DEFAULT '1',
  `email_notifications` tinyint(1) NOT NULL DEFAULT '1',
  `sms_alerts` tinyint(1) NOT NULL DEFAULT '0',
  `two_factor_enabled` tinyint(1) NOT NULL DEFAULT '0',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `guardian_settings_tbl`
--

INSERT INTO `guardian_settings_tbl` (`settings_id`, `guardian_id`, `allow_location`, `push_notifications`, `email_notifications`, `sms_alerts`, `two_factor_enabled`, `updated_at`) VALUES
(1, 1, 1, 1, 1, 1, 0, '2026-04-21 05:29:49');

-- --------------------------------------------------------

--
-- Table structure for table `guardian_tbl`
--

CREATE TABLE `guardian_tbl` (
  `guardian_id` int NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `middle_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `guardian_image_url` varchar(500) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `province` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `barangay` varchar(100) DEFAULT NULL,
  `village` varchar(100) DEFAULT NULL,
  `street_address` text,
  `role` varchar(50) DEFAULT NULL,
  `has_seen_tour` tinyint(1) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `guardian_tbl`
--

INSERT INTO `guardian_tbl` (`guardian_id`, `username`, `password`, `first_name`, `middle_name`, `last_name`, `guardian_image_url`, `email`, `contact_number`, `province`, `city`, `barangay`, `village`, `street_address`, `role`, `has_seen_tour`, `created_at`, `updated_at`) VALUES
(1, 'ivanren', '$2b$12$ftivFrgchI2ni8YuoaceHOP2iMchNyi.J6idNjHamtNs.sz4VFb3.', 'Macy', 'Shoshana Stout', 'Soto', NULL, 'villamora.ivanren.manguiat@gmail.com', '09916820831', 'Metro Manila', 'Quezon City', 'San Bartolome', 'Saint Francis', 'Pechayan St.', 'guardian', 1, '2026-03-27 04:40:53', '2026-03-30 04:50:41'),
(2, 'Africa01', '$2b$12$1xyQaV/3c.ybGvXJXWU2a.FT6CFYYgYFQ6/80sbJu9g/XvaHpEfxy', 'Christine', '', 'Africa', NULL, 'christinedelluta@gmail.com', '09304249141', 'Metro Manila', 'Quezon City', 'San Bartolome', 'Saint Francis', 'Lot 3', 'guardian', 1, '2026-04-16 08:02:23', '2026-04-16 08:02:58'),
(3, 'Mvisto', '$2b$12$iBKGNKizmLl56nltuK1NEe492MqXxsUcXz/gvq5oIL3naLqf8rGpu', 'Mary', NULL, 'Visto', NULL, 'christinedafrica@gmail.com', '09161380721', 'Metro Manila', 'Quezon City', 'San Bartolome', 'Saint Francis', 'Lot 4', 'guardian', 1, '2026-04-16 09:25:43', '2026-04-16 09:26:10');

-- --------------------------------------------------------

--
-- Table structure for table `login_attempts_tbl`
--

CREATE TABLE `login_attempts_tbl` (
  `id` int NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `login_attempts_tbl`
--

INSERT INTO `login_attempts_tbl` (`id`, `username`, `ip_address`, `created_at`) VALUES
(13, 'admin', '136.158.31.63', '2026-04-16 13:19:38'),
(15, 'admin', '136.158.31.63', '2026-04-16 13:20:29'),
(35, 'ivanren', '127.0.0.1', '2026-04-21 05:41:03'),
(36, 'ivanren', '127.0.0.1', '2026-04-21 05:41:07'),
(37, 'ivanren', '127.0.0.1', '2026-04-21 06:45:18'),
(38, 'ivanren', '127.0.0.1', '2026-04-21 07:46:04'),
(39, 'ivanren', '122.3.102.197', '2026-04-23 11:26:07'),
(40, 'ivanren', '136.158.31.63', '2026-04-23 11:26:23'),
(41, 'ivanren', '122.3.102.197', '2026-04-23 11:26:27'),
(42, 'ivanren', '136.158.31.63', '2026-04-23 11:29:29'),
(43, 'ivanren', '136.158.31.63', '2026-04-23 11:31:31'),
(44, 'villamora.ivanren.manguiat@gmail.com', '136.158.31.63', '2026-04-23 11:32:47'),
(45, 'ivanren', '136.158.31.63', '2026-04-23 11:32:56');

-- --------------------------------------------------------

--
-- Table structure for table `note_reminder_tbl`
--

CREATE TABLE `note_reminder_tbl` (
  `note_reminder_id` int NOT NULL,
  `guardian_id` int NOT NULL,
  `vip_id` int NOT NULL,
  `message` text NOT NULL,
  `reminder_time` time NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notifications_tbl`
--

CREATE TABLE `notifications_tbl` (
  `notification_id` int NOT NULL,
  `audience` enum('all_admins','super_admins') NOT NULL,
  `type` varchar(50) NOT NULL,
  `title` varchar(255) NOT NULL,
  `body` text,
  `link_path` varchar(255) DEFAULT NULL,
  `related_concern_id` int DEFAULT NULL,
  `related_admin_id` int DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `notifications_tbl`
--

INSERT INTO `notifications_tbl` (`notification_id`, `audience`, `type`, `title`, `body`, `link_path`, `related_concern_id`, `related_admin_id`, `created_at`) VALUES
(1, 'super_admins', 'admin_setup_completed', 'Admin completed account setup', 'Ivan Ren VIllamora finished setting up their account.', '/admins', NULL, 1, '2026-04-13 15:20:52'),
(2, 'all_admins', 'guardian_concern', 'New guardian concern', 'ivanren: [Source: guardian-dashboard]\n\nHello', '/guardian-concerns', 1, NULL, '2026-04-13 15:20:53'),
(3, 'all_admins', 'guardian_concern', 'New guardian concern', 'ivanren: [Source: guardian-dashboard]\n\nhrlloi', '/guardian-concerns', 3, NULL, '2026-04-17 23:38:44'),
(4, 'all_admins', 'guardian_concern', 'New guardian concern', 'ivanren: [Source: guardian-dashboard]\n\nhrlloi', '/guardian-concerns', 2, NULL, '2026-04-17 23:38:44'),
(5, 'all_admins', 'guardian_concern', 'New guardian concern', 'ivanren: [Source: guardian-dashboard]\n\nhrlloi', '/guardian-concerns', 4, NULL, '2026-04-17 23:39:44'),
(6, 'all_admins', 'guardian_concern', 'New guardian concern', 'ivanren: [Source: guardian-dashboard]\n\nhello', '/guardian-concerns', 6, NULL, '2026-04-17 23:42:44'),
(7, 'all_admins', 'guardian_concern', 'New guardian concern', 'ivanren: [Source: guardian-dashboard]\n\nsfds', '/guardian-concerns', 7, NULL, '2026-04-17 23:43:44'),
(8, 'all_admins', 'guardian_concern', 'New guardian concern', 'ivanren: [Source: guardian-dashboard]\n\ndsfasfea', '/guardian-concerns', 8, NULL, '2026-04-17 23:45:44'),
(9, 'all_admins', 'guardian_concern', 'New guardian concern', 'ivanren: [Source: guardian-dashboard]\n\nhello', '/guardian-concerns', 11, NULL, '2026-04-17 23:48:44'),
(10, 'all_admins', 'guardian_concern', 'New guardian concern', 'ivanren: [Source: guardian-dashboard]\n\ndsfasfea', '/guardian-concerns', 10, NULL, '2026-04-17 23:48:44'),
(11, 'all_admins', 'guardian_concern', 'New guardian concern', 'ivanren: [Source: guardian-dashboard]\n\nfesf', '/guardian-concerns', 13, NULL, '2026-04-18 00:19:44'),
(12, 'all_admins', 'guardian_concern', 'New guardian concern', 'rys: [Source: guest-landing]\n\nasdasdasd', '/guardian-concerns', 14, NULL, '2026-04-18 00:20:12'),
(13, 'all_admins', 'admin_created', 'New admin created', 'asdasd asdasd (ryan.casipe78@gmail.com) was added.', '/admins', NULL, 2, '2026-04-18 00:33:49'),
(14, 'all_admins', 'admin_created', 'New admin created', 'Ivan Villamora (villamora.ivanren.manguiat@gmail.com) was added.', '/admins', NULL, 3, '2026-04-18 00:34:40'),
(15, 'all_admins', 'guardian_concern', 'New guardian concern', 'Ivan Ren Villamora: [Source: guest-landing]\n\ndasd', '/guardian-concerns', 16, NULL, '2026-04-21 05:24:43'),
(16, 'all_admins', 'guardian_concern', 'New guardian concern', 'ivanren: [Source: guardian-dashboard]\n\nhello', '/guardian-concerns', 15, NULL, '2026-04-21 05:24:43'),
(17, 'all_admins', 'guardian_concern', 'New guardian concern', 'ivanren: [Source: guardian-dashboard]\n\nconcern a', '/guardian-concerns', 17, NULL, '2026-04-21 05:27:13'),
(18, 'all_admins', 'concern_restored', 'Guardian concern restored', 'Ivan Rens VIllamora (super admin) restored guardian concern #14.', '/guardian-concerns', NULL, 1, '2026-04-21 07:13:01'),
(19, 'all_admins', 'concern_restored', 'Guardian concern restored', 'Ivan Rens VIllamora (super admin) restored guardian concern #14.', '/guardian-concerns', NULL, 1, '2026-04-21 07:13:10'),
(20, 'all_admins', 'concern_restored', 'Guardian concern restored', 'Ivan Rens VIllamora (super admin) restored guardian concern #15.', '/guardian-concerns', NULL, 1, '2026-04-21 07:14:56'),
(21, 'all_admins', 'concern_restored', 'Guardian concern restored', 'Ivan Rens VIllamora (super admin) restored guardian concern #17.', '/guardian-concerns', NULL, 1, '2026-04-21 07:18:30'),
(22, 'all_admins', 'concern_restored', 'Guardian concern restored', 'Ivan Rens VIllamora (super admin) restored guardian concern #14.', '/guardian-concerns', NULL, 1, '2026-04-21 07:18:32'),
(23, 'all_admins', 'concern_restored', 'Guardian concern restored', 'Ivan Rens VIllamora (super admin) restored guardian concern #15.', '/guardian-concerns', NULL, 1, '2026-04-21 07:18:34'),
(24, 'all_admins', 'device_created', 'New device added', 'Ivan Rens VIllamora (Super Admin) added device SC-136907.', '/devices', NULL, 1, '2026-04-21 07:20:58'),
(25, 'all_admins', 'device_deleted', 'Device deleted', 'Ivan Rens VIllamora (Super Admin) deleted device SC-136900.', '/devices', NULL, 1, '2026-04-21 07:21:35'),
(26, 'all_admins', 'admin_deleted', 'Admin account deleted', 'Ivan Rens VIllamora (Super Admin) deleted admin account Ivan Ren M. Villamora (villamora.ivanren.manguiat@gmail.com).', '/admins', NULL, 1, '2026-04-21 07:33:48'),
(27, 'all_admins', 'admin_restored', 'Admin account restored', 'Ivan Rens VIllamora (super admin) restored admin account villamora.ivanren.manguiat@gmail.com.', '/admins', NULL, 1, '2026-04-21 07:36:49'),
(28, 'all_admins', 'concern_restored', 'Guardian concern restored', 'Ivan Rens VIllamora (super admin) restored guardian concern #15.', '/guardian-concerns', NULL, 1, '2026-04-21 07:46:15'),
(29, 'all_admins', 'guardian_concern', 'New guardian concern', 'rys: [Source: guest-landing]\n\nasdasdasdafasd', '/guardian-concerns', 18, NULL, '2026-04-23 11:26:58'),
(30, 'all_admins', 'device_restored', 'Device restored', 'Ivan Rens VIllamora (super admin) restored device SC-136900.', '/devices', NULL, 1, '2026-04-23 11:29:44'),
(31, 'all_admins', 'guardian_concern', 'New guardian concern', 'Villamora, Ivan Ren M.: [Source: guest-landing]\n\nI have a concern', '/guardian-concerns', 19, NULL, '2026-04-23 11:31:31'),
(32, 'all_admins', 'guardian_concern', 'New guardian concern', 'asdasdasd: [Source: guest-landing]\n\nasasdasdsad', '/guardian-concerns', 20, NULL, '2026-04-23 11:32:56'),
(33, 'all_admins', 'concern_restored', 'Guardian concern restored', 'Ivan Rens VIllamora (super admin) restored guardian concern #20.', '/guardian-concerns', NULL, 1, '2026-04-23 11:33:07'),
(34, 'all_admins', 'concern_restored', 'Guardian concern restored', 'Ivan Rens VIllamora (super admin) restored guardian concern #20.', '/guardian-concerns', NULL, 1, '2026-04-23 11:37:43');

-- --------------------------------------------------------

--
-- Table structure for table `notification_reads_tbl`
--

CREATE TABLE `notification_reads_tbl` (
  `id` int NOT NULL,
  `notification_id` int NOT NULL,
  `admin_id` int NOT NULL,
  `read_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `notification_reads_tbl`
--

INSERT INTO `notification_reads_tbl` (`id`, `notification_id`, `admin_id`, `read_at`) VALUES
(1, 2, 1, '2026-04-13 15:22:28'),
(2, 1, 1, '2026-04-18 00:26:01'),
(3, 3, 1, '2026-04-18 00:26:01'),
(4, 4, 1, '2026-04-18 00:26:01'),
(5, 5, 1, '2026-04-18 00:26:01'),
(6, 6, 1, '2026-04-18 00:26:01'),
(7, 7, 1, '2026-04-18 00:26:01'),
(8, 8, 1, '2026-04-18 00:26:01'),
(9, 9, 1, '2026-04-18 00:26:01'),
(10, 10, 1, '2026-04-18 00:26:01'),
(11, 11, 1, '2026-04-18 00:26:01'),
(12, 12, 1, '2026-04-18 00:26:01'),
(13, 14, 1, '2026-04-18 00:37:35'),
(14, 13, 1, '2026-04-21 05:44:05'),
(15, 15, 1, '2026-04-21 05:44:05'),
(16, 16, 1, '2026-04-21 05:44:05'),
(17, 17, 1, '2026-04-21 05:44:05'),
(18, 32, 1, '2026-04-23 11:38:35'),
(19, 18, 1, '2026-04-23 11:38:50'),
(20, 19, 1, '2026-04-23 11:38:50'),
(21, 20, 1, '2026-04-23 11:38:50'),
(22, 21, 1, '2026-04-23 11:38:50'),
(23, 22, 1, '2026-04-23 11:38:50'),
(24, 23, 1, '2026-04-23 11:38:50'),
(25, 24, 1, '2026-04-23 11:38:50'),
(26, 25, 1, '2026-04-23 11:38:50'),
(27, 26, 1, '2026-04-23 11:38:50'),
(28, 27, 1, '2026-04-23 11:38:50'),
(29, 28, 1, '2026-04-23 11:38:50'),
(30, 29, 1, '2026-04-23 11:38:50'),
(31, 30, 1, '2026-04-23 11:38:50'),
(32, 31, 1, '2026-04-23 11:38:50'),
(33, 33, 1, '2026-04-23 11:38:50'),
(34, 34, 1, '2026-04-23 11:38:50');

-- --------------------------------------------------------

--
-- Table structure for table `otp_tbl`
--

CREATE TABLE `otp_tbl` (
  `id` int NOT NULL,
  `email` varchar(255) NOT NULL,
  `otp_code` varchar(255) NOT NULL,
  `is_used` tinyint(1) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `expires_at` datetime NOT NULL,
  `used_at` timestamp NULL DEFAULT NULL,
  `purpose` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `otp_tbl`
--

INSERT INTO `otp_tbl` (`id`, `email`, `otp_code`, `is_used`, `created_at`, `expires_at`, `used_at`, `purpose`) VALUES
(1, 'villamora.ivanren.manguiat@gmail.com', '497016', 1, '2026-03-27 04:40:18', '2026-03-27 04:50:18', '2026-03-27 04:40:53', 'general'),
(2, 'villamoraivanren@gmail.com', '397913', 1, '2026-04-13 15:18:23', '2026-04-13 15:23:23', '2026-04-13 15:18:49', 'first_login'),
(3, 'christinedafrica@gmail.com', '181556', 1, '2026-04-16 09:25:01', '2026-04-16 09:35:01', '2026-04-16 09:25:43', 'general'),
(4, 'villamora.ivanren.manguiat@gmail.com', '608091', 1, '2026-04-17 02:32:14', '2026-04-17 02:42:14', '2026-04-17 02:32:32', 'general');

-- --------------------------------------------------------

--
-- Table structure for table `push_subscription_tbl`
--

CREATE TABLE `push_subscription_tbl` (
  `subscription_id` int NOT NULL,
  `guardian_id` int NOT NULL,
  `endpoint` text NOT NULL,
  `p256dh` text NOT NULL,
  `auth` text NOT NULL,
  `user_agent` text,
  `created_at` timestamp NOT NULL,
  `updated_at` timestamp NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reason_catalog_tbl`
--

CREATE TABLE `reason_catalog_tbl` (
  `reason_id` int NOT NULL,
  `action_type` varchar(50) NOT NULL,
  `reason_code` varchar(50) NOT NULL,
  `reason_label` varchar(120) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `reason_catalog_tbl`
--

INSERT INTO `reason_catalog_tbl` (`reason_id`, `action_type`, `reason_code`, `reason_label`, `is_active`) VALUES
(1, 'admin_delete', 'policy_violation', 'Policy Violation', 1),
(2, 'admin_delete', 'duplicate_account', 'Duplicate Account', 1),
(3, 'admin_delete', 'security_incident', 'Security Incident', 1),
(4, 'admin_delete', 'resigned', 'Resigned', 1),
(5, 'admin_delete', 'inactive', 'Inactive Account', 1),
(6, 'admin_delete', 'other', 'Other', 1),
(7, 'concern_delete', 'spam', 'Spam', 1),
(8, 'concern_delete', 'abusive_content', 'Abusive Content', 1),
(9, 'concern_delete', 'duplicate_concern', 'Duplicate Concern', 1),
(10, 'concern_delete', 'pii_exposure', 'Contains Sensitive PII', 1),
(11, 'concern_delete', 'legal_request', 'Legal/Compliance Request', 1),
(12, 'concern_delete', 'other', 'Other', 1),
(13, 'role_change', 'least_privilege', 'Least Privilege Enforcement', 1),
(14, 'role_change', 'policy_violation', 'Policy Violation', 1),
(15, 'role_change', 'security_incident', 'Security Incident', 1),
(16, 'role_change', 'assignment_change', 'Assignment/Org Change', 1),
(17, 'role_change', 'user_request', 'User Request', 1),
(18, 'role_change', 'other', 'Other', 1),
(19, 'device_delete', 'duplicate_device', 'Duplicate Device', 1),
(20, 'device_delete', 'provisioning_error', 'Provisioning Error', 1),
(21, 'device_delete', 'hardware_replacement', 'Hardware Replacement', 1),
(22, 'device_delete', 'inventory_cleanup', 'Inventory Cleanup', 1),
(23, 'device_delete', 'other', 'Other', 1);

-- --------------------------------------------------------

--
-- Table structure for table `vip_tbl`
--

CREATE TABLE `vip_tbl` (
  `vip_id` int NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `middle_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `vip_image_url` varchar(500) DEFAULT NULL,
  `province` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `barangay` varchar(100) DEFAULT NULL,
  `street_address` text,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `vip_tbl`
--

INSERT INTO `vip_tbl` (`vip_id`, `first_name`, `middle_name`, `last_name`, `vip_image_url`, `province`, `city`, `barangay`, `street_address`, `created_at`, `updated_at`) VALUES
(3, 'Ivan', 'Magnuiat', 'Villamora', '', 'Metro Manila', 'Quezon City', 'San Bartolome', 'Pechayan St.', '2026-04-17 23:54:04', '2026-04-17 23:54:04');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account_history_tbl`
--
ALTER TABLE `account_history_tbl`
  ADD PRIMARY KEY (`history_id`),
  ADD KEY `guardian_id` (`guardian_id`),
  ADD KEY `device_id` (`device_id`);

--
-- Indexes for table `admin_archive_tbl`
--
ALTER TABLE `admin_archive_tbl`
  ADD PRIMARY KEY (`archive_id`);

--
-- Indexes for table `admin_audit_logs_tbl`
--
ALTER TABLE `admin_audit_logs_tbl`
  ADD PRIMARY KEY (`audit_id`),
  ADD KEY `ix_smart_cane_db_admin_audit_logs_tbl_status` (`status`),
  ADD KEY `ix_smart_cane_db_admin_audit_logs_tbl_target_admin_id` (`target_admin_id`),
  ADD KEY `ix_smart_cane_db_admin_audit_logs_tbl_actor_admin_id` (`actor_admin_id`),
  ADD KEY `ix_smart_cane_db_admin_audit_logs_tbl_created_at` (`created_at`),
  ADD KEY `ix_smart_cane_db_admin_audit_logs_tbl_action_type` (`action_type`);

--
-- Indexes for table `admin_audit_log_tbl`
--
ALTER TABLE `admin_audit_log_tbl`
  ADD PRIMARY KEY (`audit_id`),
  ADD KEY `fk_audit_actor_admin` (`actor_admin_id`),
  ADD KEY `fk_audit_target_admin` (`target_admin_id`),
  ADD KEY `fk_audit_target_concern` (`target_concern_id`);

--
-- Indexes for table `admin_tbl`
--
ALTER TABLE `admin_tbl`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `device_config_tbl`
--
ALTER TABLE `device_config_tbl`
  ADD PRIMARY KEY (`config_id`),
  ADD UNIQUE KEY `device_id` (`device_id`);

--
-- Indexes for table `device_guardian_tbl`
--
ALTER TABLE `device_guardian_tbl`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `_device_guardian_uc` (`device_id`,`guardian_id`),
  ADD KEY `guardian_id` (`guardian_id`);

--
-- Indexes for table `device_last_location_tbl`
--
ALTER TABLE `device_last_location_tbl`
  ADD PRIMARY KEY (`device_id`);

--
-- Indexes for table `device_logs_tbl`
--
ALTER TABLE `device_logs_tbl`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `ix_smart_cane_db_device_logs_tbl_guardian_id` (`guardian_id`),
  ADD KEY `ix_smart_cane_db_device_logs_tbl_device_id` (`device_id`),
  ADD KEY `ix_smart_cane_db_device_logs_tbl_created_at` (`created_at`);

--
-- Indexes for table `device_route_tbl`
--
ALTER TABLE `device_route_tbl`
  ADD PRIMARY KEY (`route_id`),
  ADD UNIQUE KEY `device_id` (`device_id`),
  ADD KEY `guardian_id` (`guardian_id`);

--
-- Indexes for table `device_tbl`
--
ALTER TABLE `device_tbl`
  ADD PRIMARY KEY (`device_id`),
  ADD UNIQUE KEY `device_serial_number` (`device_serial_number`),
  ADD KEY `vip_id` (`vip_id`);

--
-- Indexes for table `guardian_concerns_tbl`
--
ALTER TABLE `guardian_concerns_tbl`
  ADD PRIMARY KEY (`concern_id`),
  ADD KEY `fk_concern_replied_by_admin` (`replied_by_admin_id`),
  ADD KEY `fk_concern_deleted_by_admin` (`deleted_by_admin_id`),
  ADD KEY `idx_guardian_concerns_email` (`email`),
  ADD KEY `idx_guardian_concerns_status` (`status`),
  ADD KEY `idx_guardian_concerns_created` (`created_at`),
  ADD KEY `idx_guardian_concerns_deleted` (`is_deleted`);

--
-- Indexes for table `guardian_invitations`
--
ALTER TABLE `guardian_invitations`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_smart_cane_db_guardian_invitations_token` (`token`),
  ADD KEY `device_id` (`device_id`),
  ADD KEY `invited_by_guardian_id` (`invited_by_guardian_id`);

--
-- Indexes for table `guardian_settings_tbl`
--
ALTER TABLE `guardian_settings_tbl`
  ADD PRIMARY KEY (`settings_id`),
  ADD UNIQUE KEY `uq_guardian_settings_guardian` (`guardian_id`);

--
-- Indexes for table `guardian_tbl`
--
ALTER TABLE `guardian_tbl`
  ADD PRIMARY KEY (`guardian_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `login_attempts_tbl`
--
ALTER TABLE `login_attempts_tbl`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `note_reminder_tbl`
--
ALTER TABLE `note_reminder_tbl`
  ADD PRIMARY KEY (`note_reminder_id`),
  ADD KEY `guardian_id` (`guardian_id`),
  ADD KEY `vip_id` (`vip_id`);

--
-- Indexes for table `notifications_tbl`
--
ALTER TABLE `notifications_tbl`
  ADD PRIMARY KEY (`notification_id`),
  ADD KEY `idx_notifications_audience` (`audience`),
  ADD KEY `idx_notifications_type` (`type`),
  ADD KEY `idx_notifications_related_concern` (`related_concern_id`),
  ADD KEY `idx_notifications_related_admin` (`related_admin_id`),
  ADD KEY `idx_notifications_created` (`created_at`);

--
-- Indexes for table `notification_reads_tbl`
--
ALTER TABLE `notification_reads_tbl`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_notification_read_notification_admin` (`notification_id`,`admin_id`),
  ADD KEY `idx_notification_reads_notification` (`notification_id`),
  ADD KEY `idx_notification_reads_admin` (`admin_id`),
  ADD KEY `idx_notification_reads_read_at` (`read_at`);

--
-- Indexes for table `otp_tbl`
--
ALTER TABLE `otp_tbl`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_smart_cane_db_otp_tbl_email` (`email`);

--
-- Indexes for table `push_subscription_tbl`
--
ALTER TABLE `push_subscription_tbl`
  ADD PRIMARY KEY (`subscription_id`),
  ADD KEY `ix_smart_cane_db_push_subscription_tbl_guardian_id` (`guardian_id`);

--
-- Indexes for table `reason_catalog_tbl`
--
ALTER TABLE `reason_catalog_tbl`
  ADD PRIMARY KEY (`reason_id`),
  ADD UNIQUE KEY `uq_reason_action_code` (`action_type`,`reason_code`);

--
-- Indexes for table `vip_tbl`
--
ALTER TABLE `vip_tbl`
  ADD PRIMARY KEY (`vip_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account_history_tbl`
--
ALTER TABLE `account_history_tbl`
  MODIFY `history_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT for table `admin_archive_tbl`
--
ALTER TABLE `admin_archive_tbl`
  MODIFY `archive_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `admin_audit_logs_tbl`
--
ALTER TABLE `admin_audit_logs_tbl`
  MODIFY `audit_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `admin_audit_log_tbl`
--
ALTER TABLE `admin_audit_log_tbl`
  MODIFY `audit_id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `admin_tbl`
--
ALTER TABLE `admin_tbl`
  MODIFY `admin_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `device_config_tbl`
--
ALTER TABLE `device_config_tbl`
  MODIFY `config_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=684;

--
-- AUTO_INCREMENT for table `device_guardian_tbl`
--
ALTER TABLE `device_guardian_tbl`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `device_logs_tbl`
--
ALTER TABLE `device_logs_tbl`
  MODIFY `log_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- AUTO_INCREMENT for table `device_route_tbl`
--
ALTER TABLE `device_route_tbl`
  MODIFY `route_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `device_tbl`
--
ALTER TABLE `device_tbl`
  MODIFY `device_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `guardian_concerns_tbl`
--
ALTER TABLE `guardian_concerns_tbl`
  MODIFY `concern_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `guardian_invitations`
--
ALTER TABLE `guardian_invitations`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `guardian_settings_tbl`
--
ALTER TABLE `guardian_settings_tbl`
  MODIFY `settings_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `guardian_tbl`
--
ALTER TABLE `guardian_tbl`
  MODIFY `guardian_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `login_attempts_tbl`
--
ALTER TABLE `login_attempts_tbl`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `note_reminder_tbl`
--
ALTER TABLE `note_reminder_tbl`
  MODIFY `note_reminder_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notifications_tbl`
--
ALTER TABLE `notifications_tbl`
  MODIFY `notification_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `notification_reads_tbl`
--
ALTER TABLE `notification_reads_tbl`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `otp_tbl`
--
ALTER TABLE `otp_tbl`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `push_subscription_tbl`
--
ALTER TABLE `push_subscription_tbl`
  MODIFY `subscription_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reason_catalog_tbl`
--
ALTER TABLE `reason_catalog_tbl`
  MODIFY `reason_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `vip_tbl`
--
ALTER TABLE `vip_tbl`
  MODIFY `vip_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `account_history_tbl`
--
ALTER TABLE `account_history_tbl`
  ADD CONSTRAINT `account_history_tbl_ibfk_1` FOREIGN KEY (`guardian_id`) REFERENCES `guardian_tbl` (`guardian_id`),
  ADD CONSTRAINT `account_history_tbl_ibfk_2` FOREIGN KEY (`device_id`) REFERENCES `device_tbl` (`device_id`);

--
-- Constraints for table `admin_audit_logs_tbl`
--
ALTER TABLE `admin_audit_logs_tbl`
  ADD CONSTRAINT `admin_audit_logs_tbl_ibfk_1` FOREIGN KEY (`actor_admin_id`) REFERENCES `admin_tbl` (`admin_id`),
  ADD CONSTRAINT `admin_audit_logs_tbl_ibfk_2` FOREIGN KEY (`target_admin_id`) REFERENCES `admin_tbl` (`admin_id`);

--
-- Constraints for table `admin_audit_log_tbl`
--
ALTER TABLE `admin_audit_log_tbl`
  ADD CONSTRAINT `fk_audit_actor_admin` FOREIGN KEY (`actor_admin_id`) REFERENCES `admin_tbl` (`admin_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_audit_target_admin` FOREIGN KEY (`target_admin_id`) REFERENCES `admin_tbl` (`admin_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_audit_target_concern` FOREIGN KEY (`target_concern_id`) REFERENCES `guardian_concerns_tbl` (`concern_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `device_config_tbl`
--
ALTER TABLE `device_config_tbl`
  ADD CONSTRAINT `device_config_tbl_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device_tbl` (`device_id`);

--
-- Constraints for table `device_guardian_tbl`
--
ALTER TABLE `device_guardian_tbl`
  ADD CONSTRAINT `device_guardian_tbl_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device_tbl` (`device_id`),
  ADD CONSTRAINT `device_guardian_tbl_ibfk_2` FOREIGN KEY (`guardian_id`) REFERENCES `guardian_tbl` (`guardian_id`);

--
-- Constraints for table `device_last_location_tbl`
--
ALTER TABLE `device_last_location_tbl`
  ADD CONSTRAINT `device_last_location_tbl_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device_tbl` (`device_id`);

--
-- Constraints for table `device_logs_tbl`
--
ALTER TABLE `device_logs_tbl`
  ADD CONSTRAINT `device_logs_tbl_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device_tbl` (`device_id`),
  ADD CONSTRAINT `device_logs_tbl_ibfk_2` FOREIGN KEY (`guardian_id`) REFERENCES `guardian_tbl` (`guardian_id`);

--
-- Constraints for table `device_route_tbl`
--
ALTER TABLE `device_route_tbl`
  ADD CONSTRAINT `device_route_tbl_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device_tbl` (`device_id`),
  ADD CONSTRAINT `device_route_tbl_ibfk_2` FOREIGN KEY (`guardian_id`) REFERENCES `guardian_tbl` (`guardian_id`);

--
-- Constraints for table `device_tbl`
--
ALTER TABLE `device_tbl`
  ADD CONSTRAINT `device_tbl_ibfk_1` FOREIGN KEY (`vip_id`) REFERENCES `vip_tbl` (`vip_id`);

--
-- Constraints for table `guardian_concerns_tbl`
--
ALTER TABLE `guardian_concerns_tbl`
  ADD CONSTRAINT `fk_concern_deleted_by_admin` FOREIGN KEY (`deleted_by_admin_id`) REFERENCES `admin_tbl` (`admin_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_concern_replied_by_admin` FOREIGN KEY (`replied_by_admin_id`) REFERENCES `admin_tbl` (`admin_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `guardian_invitations`
--
ALTER TABLE `guardian_invitations`
  ADD CONSTRAINT `guardian_invitations_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device_tbl` (`device_id`),
  ADD CONSTRAINT `guardian_invitations_ibfk_2` FOREIGN KEY (`invited_by_guardian_id`) REFERENCES `guardian_tbl` (`guardian_id`);

--
-- Constraints for table `guardian_settings_tbl`
--
ALTER TABLE `guardian_settings_tbl`
  ADD CONSTRAINT `fk_guardian_settings_guardian` FOREIGN KEY (`guardian_id`) REFERENCES `guardian_tbl` (`guardian_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `note_reminder_tbl`
--
ALTER TABLE `note_reminder_tbl`
  ADD CONSTRAINT `note_reminder_tbl_ibfk_1` FOREIGN KEY (`guardian_id`) REFERENCES `guardian_tbl` (`guardian_id`),
  ADD CONSTRAINT `note_reminder_tbl_ibfk_2` FOREIGN KEY (`vip_id`) REFERENCES `vip_tbl` (`vip_id`);

--
-- Constraints for table `notification_reads_tbl`
--
ALTER TABLE `notification_reads_tbl`
  ADD CONSTRAINT `fk_notification_reads_admin` FOREIGN KEY (`admin_id`) REFERENCES `admin_tbl` (`admin_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_notification_reads_notification` FOREIGN KEY (`notification_id`) REFERENCES `notifications_tbl` (`notification_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `push_subscription_tbl`
--
ALTER TABLE `push_subscription_tbl`
  ADD CONSTRAINT `push_subscription_tbl_ibfk_1` FOREIGN KEY (`guardian_id`) REFERENCES `guardian_tbl` (`guardian_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- =========================================================================================
-- SCHEMA vs CODE ANALYSIS  (auto-generated 2026-04-23)
-- Cross-reference: schema.sql  <->  app/models.py  <->  app/routes/*
-- =========================================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- ISSUE 1 ▸ GHOST TABLE — exists in DB but has NO model class and is never used
-- ─────────────────────────────────────────────────────────────────────────────
-- TABLE: admin_audit_logs_tbl  (plural — different from admin_audit_log_tbl)
--   • The live DB contains BOTH tables:
--       admin_audit_log_tbl    ← used by the app (has model AdminAuditLog, restore.py, etc.)
--       admin_audit_logs_tbl   ← ghost table, no model, no route references it
--   • The ghost table uses slightly different column types (status ENUM vs VARCHAR,
--     no target_concern_id, no failure_message, no reason_code NOT NULL).
--   • ACTION: Safe to DROP admin_audit_logs_tbl; it is never read or written by the app.
--
-- DROP TABLE IF EXISTS `admin_audit_logs_tbl`;   -- run manually after verifying it is truly unused


-- ─────────────────────────────────────────────────────────────────────────────
-- ISSUE 2 ▸ SCHEMA HAS COLUMNS MISSING FROM models.py (GuardianConcern)
-- ─────────────────────────────────────────────────────────────────────────────
-- TABLE: guardian_concerns_tbl
-- The live schema contains 4 columns that were NOT declared in the GuardianConcern
-- SQLAlchemy model. This caused SQLAlchemy to silently ignore them on reads/writes.
--
--   Column                        Schema type           Was in model?
--   ─────────────────────────────────────────────────────────────────
--   process_stage                 VARCHAR(50) NOT NULL  ✗ MISSING → FIXED in models.py
--   resolution_remarks            TEXT NULL             ✗ MISSING → FIXED in models.py
--   process_updated_by_admin_id   INT NULL              ✗ MISSING → FIXED in models.py
--   process_updated_at            TIMESTAMP NULL        ✗ MISSING → FIXED in models.py
--
-- STATUS: Fixed — models.py now declares all 4 columns and to_dict() exposes them.
-- No schema migration needed (columns already exist in DB).


-- ─────────────────────────────────────────────────────────────────────────────
-- ISSUE 3 ▸ COLUMNS THE MODEL USES BUT SCHEMA LACKED (already existed in DB, just not in this file)
-- ─────────────────────────────────────────────────────────────────────────────
-- The original canonical schema.sql (before the phpMyAdmin dump replaced it) was
-- missing the concern-process columns. The dump now includes them. No action needed.


-- ─────────────────────────────────────────────────────────────────────────────
-- ISSUE 4 ▸ admin_archive_tbl — NO FOREIGN KEY on admin_id (by design)
-- ─────────────────────────────────────────────────────────────────────────────
-- admin_archive_tbl.admin_id stores the original PK of the deleted admin row.
-- There is intentionally NO FK constraint on this column because the admin row
-- has been removed from admin_tbl. This is correct behaviour.


-- ─────────────────────────────────────────────────────────────────────────────
-- ISSUE 5 ▸ guardian_concerns_tbl — process_stage FK to admin_tbl missing
-- ─────────────────────────────────────────────────────────────────────────────
-- process_updated_by_admin_id references an admin but has no FK constraint in the
-- live schema. If data integrity matters, add:
--
-- ALTER TABLE `guardian_concerns_tbl`
--   ADD CONSTRAINT `fk_concern_process_updated_by`
--     FOREIGN KEY (`process_updated_by_admin_id`) REFERENCES `admin_tbl`(`admin_id`)
--     ON DELETE SET NULL ON UPDATE CASCADE;


-- ─────────────────────────────────────────────────────────────────────────────
-- ISSUE 6 ▸ admin_archive_tbl — TWO COLUMNS IN SCHEMA MISSING FROM MODEL
-- ─────────────────────────────────────────────────────────────────────────────
-- The DB schema has archived_reason_code and archived_reason_text columns in
-- admin_archive_tbl, but the AdminArchive SQLAlchemy model did NOT declare them.
-- This meant SQLAlchemy silently ignored writing reason data to the archive.
--
--   Column               Schema type      Was in model?
--   ────────────────────────────────────────────────────
--   archived_reason_code VARCHAR(50)      ✗ MISSING → FIXED in models.py
--   archived_reason_text VARCHAR(500)     ✗ MISSING → FIXED in models.py
--
-- STATUS: Fixed — models.py AdminArchive now declares both columns.
-- Also fixed: delete_admin in admin.py now passes reason_code/reason_text to AdminArchive.
-- No schema migration needed (columns already exist in DB).


-- ─────────────────────────────────────────────────────────────────────────────
-- ISSUE 7 ▸ AUDIT LOG NOT RECORDED FOR SUPERADMIN DELETIONS (BUG FIX)
-- ─────────────────────────────────────────────────────────────────────────────
-- Root cause: When deleting an admin or device, the audit log INSERT and the
-- DELETE were batched in the same db.session.commit(). If the DELETE failed
-- (e.g. due to unhandled FK constraints on child tables), the entire transaction
-- was rolled back — including the audit log entry. Result: no audit record.
--
-- Additionally, device_tbl child rows (device_config_tbl, device_last_location_tbl,
-- device_route_tbl, device_logs_tbl) do NOT have ON DELETE CASCADE in the schema,
-- so deleting a device with any of these child rows would raise an FK violation
-- and silently roll back the whole transaction.
--
-- Fix applied (2026-04-23):
--   • admin.py  delete_admin:  audit log + archive committed FIRST, then admin deleted.
--   • device.py delete_device: audit log committed FIRST, then child rows are
--     explicitly deleted (DeviceConfig, DeviceLastLocation, DeviceRoute, DeviceLog),
--     then the device row is deleted.
--
-- Optional DB-level fix (alternative to code fix for device deletes):
-- ALTER TABLE `device_config_tbl`
--   DROP FOREIGN KEY `device_config_tbl_ibfk_1`,
--   ADD CONSTRAINT `device_config_tbl_ibfk_1`
--     FOREIGN KEY (`device_id`) REFERENCES `device_tbl`(`device_id`) ON DELETE CASCADE;
--
-- ALTER TABLE `device_last_location_tbl`
--   DROP FOREIGN KEY `device_last_location_tbl_ibfk_1`,
--   ADD CONSTRAINT `device_last_location_tbl_ibfk_1`
--     FOREIGN KEY (`device_id`) REFERENCES `device_tbl`(`device_id`) ON DELETE CASCADE;
--
-- ALTER TABLE `device_route_tbl`
--   DROP FOREIGN KEY `device_route_tbl_ibfk_1`,
--   ADD CONSTRAINT `device_route_tbl_ibfk_1`
--     FOREIGN KEY (`device_id`) REFERENCES `device_tbl`(`device_id`) ON DELETE CASCADE;
--
-- ALTER TABLE `device_logs_tbl`
--   DROP FOREIGN KEY `device_logs_tbl_ibfk_1`,
--   ADD CONSTRAINT `device_logs_tbl_ibfk_1`
--     FOREIGN KEY (`device_id`) REFERENCES `device_tbl`(`device_id`) ON DELETE CASCADE;


-- ─────────────────────────────────────────────────────────────────────────────
-- FULL COLUMN COVERAGE TABLE  (schema  ↔  model  ↔  route usage)
-- ─────────────────────────────────────────────────────────────────────────────
--
-- TABLE              | COLUMN                        | SCHEMA | MODEL | ROUTE USES
-- ───────────────────────────────────────────────────────────────────────────────
-- admin_tbl          | all columns                   |  ✓     |  ✓    |  ✓
-- admin_archive_tbl  | archived_reason_code          |  ✓     |  ✓*   |  ✓*  ← FIXED
--                    | archived_reason_text          |  ✓     |  ✓*   |  ✓*  ← FIXED
--                    | all other columns             |  ✓     |  ✓    |  ✓
-- admin_audit_log_tbl| all columns                   |  ✓     |  ✓    |  ✓
-- admin_audit_logs_tbl (ghost)                        |  ✓     |  ✗    |  ✗  ← drop
-- device_tbl         | all columns                   |  ✓     |  ✓    |  ✓
-- device_guardian_tbl| all columns                   |  ✓     |  ✓    |  ✓
-- device_config_tbl  | all columns                   |  ✓     |  ✓    |  ✓
-- device_last_loc_tbl| all columns                   |  ✓     |  ✓    |  ✓
-- device_route_tbl   | all columns                   |  ✓     |  ✓    |  ✓
-- device_logs_tbl    | all columns                   |  ✓     |  ✓    |  ✓
-- guardian_tbl       | all columns                   |  ✓     |  ✓    |  ✓
-- guardian_concerns_tbl | is_deleted, deleted_at     |  ✓     |  ✓    |  ✓
--                    | deleted_by_admin_id           |  ✓     |  ✓    |  ✓
--                    | process_stage                 |  ✓     |  ✓*   |  ✗ (not yet used in route)
--                    | resolution_remarks            |  ✓     |  ✓*   |  ✗
--                    | process_updated_by_admin_id   |  ✓     |  ✓*   |  ✗
--                    | process_updated_at            |  ✓     |  ✓*   |  ✗
-- guardian_invitations| all columns                  |  ✓     |  ✓    |  ✓
-- guardian_settings_tbl| all columns                 |  ✓     |  ✗    |  ✗  ← model missing (not used yet)
-- notifications_tbl  | all columns                   |  ✓     |  ✓    |  ✓
-- notification_reads_tbl| all columns                |  ✓     |  ✓    |  ✓
-- otp_tbl            | all columns                   |  ✓     |  ✓    |  ✓
-- login_attempts_tbl | all columns                   |  ✓     |  ✓    |  ✓
-- push_subscription_tbl| all columns                 |  ✓     |  ✓    |  ✓
-- vip_tbl            | all columns                   |  ✓     |  ✓    |  ✓
-- note_reminder_tbl  | all columns                   |  ✓     |  ✓    |  ✓
-- reason_catalog_tbl | all columns                   |  ✓     |  ✗    |  ✗  ← model missing (not used yet)
-- account_history_tbl| all columns                   |  ✓     |  ✓    |  ✓
--
--  * Fixed in this session — columns added to models.py AdminArchive / GuardianConcern.

-- =========================================================================================



-- Drop the old RESTRICT constraint
ALTER TABLE admin_audit_log_tbl DROP FOREIGN KEY fk_audit_actor_admin;
-- Make the column nullable (required for SET NULL to work)

ALTER TABLE admin_audit_log_tbl MODIFY COLUMN actor_admin_id INT NULL;
-- Re-add with SET NULL (audit history is preserved, actor ID becomes NULL)

ALTER TABLE admin_audit_log_tbl
  ADD CONSTRAINT fk_audit_actor_admin
  
    FOREIGN KEY (actor_admin_id) REFERENCES admin_tbl(admin_id)
    ON DELETE SET NULL ON UPDATE CASCADE;